import os
import json
import time
import logging
import logging.config
import configparser
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import pandas as pd
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.callbacks.manager import get_openai_callback
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.schema import Document

# Setup logging
os.makedirs('logs', exist_ok=True)
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('chatbot')

# Performance metrics class
class QueryMetrics:
    def __init__(self):
        self.start_time = time.time()
        self.total_tokens = 0
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.cost = 0.0
    
    def record_token_usage(self, cb):
        self.total_tokens = cb.total_tokens
        self.prompt_tokens = cb.prompt_tokens
        self.completion_tokens = cb.completion_tokens
        self.cost = cb.total_cost
    
    def get_response_time(self):
        return time.time() - self.start_time
    
    def to_dict(self):
        return {
            "response_time": f"{self.get_response_time():.2f}s",
            "total_tokens": self.total_tokens,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "cost": f"${self.cost:.4f}"
        }

# Initialize FastAPI app
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Load configuration
config = configparser.ConfigParser()
config.read('config.properties')
OPENAI_API_KEY = config.get('DEFAULT', 'apikey')
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Log startup information
logger.info("Starting IT Support Assistant application")
logger.debug("Configuration loaded successfully")

# Initialize vector store
embeddings = OpenAIEmbeddings()
persist_directory = 'vectordb'

class ChatMessage(BaseModel):
    message: str

def prepare_incident_text(row):
    """Convert incident row to searchable text with ITIL-focused structure and semantic markers"""
    
    # Calculate resolution time if available
    resolution_time = ""
    try:
        if row['Resolved At'] and row['Opened At']:
            opened = pd.to_datetime(row['Opened At'])
            resolved = pd.to_datetime(row['Resolved At'])
            resolution_time = f"\nResolution Time: {(resolved - opened).total_seconds() / 3600:.2f} hours"
    except:
        resolution_time = "\nResolution Time: Not available"
    
    # Determine incident severity
    severity = "High" if row['Priority'] in ['1 - Critical', '2 - High'] else \
               "Medium" if row['Priority'] == '3 - Moderate' else "Low"
    
    return f"""
    === Incident Details ===
    Incident Number: {row['Number']}
    Status: {row['State']}
    
    === Classification ===
    Category: {row['Category']}
    Subcategory: {row['Subcategory']}
    
    === Priority Assessment ===
    Impact: {row['Impact']}
    Urgency: {row['Urgency']}
    Priority: {row['Priority']}
    Overall Severity: {severity}
    
    === Timeline ===
    Opened: {row['Opened At']}
    Resolved: {row['Resolved At']}{resolution_time}
    
    === Support Details ===
    Assignment Group: {row['Assignment Group']}
    Assigned To: {row['Assigned To']}
    
    === Description ===
    Summary: {row['Short Description']}
    
    === Detailed Notes ===
    {row['Notes']}
    """

def initialize_vectorstore():
    """Initialize or load the vector store with incident data"""
    df = pd.read_csv('Snow_Incidents.csv')
    
    # Process incidents with enhanced metadata and relationships
    documents = []
    metadata = []
    
    # First pass: Create basic documents and metadata
    for _, row in df.iterrows():
        text = prepare_incident_text(row)
        
        # Calculate severity
        severity = "High" if row['Priority'] in ['1 - Critical', '2 - High'] else \
                  "Medium" if row['Priority'] == '3 - Moderate' else "Low"
        
        # Calculate resolution time with better error handling
        resolution_hours = None
        try:
            if pd.notna(row['Resolved At']) and pd.notna(row['Opened At']):
                opened = pd.to_datetime(row['Opened At'])
                resolved = pd.to_datetime(row['Resolved At'])
                resolution_hours = (resolved - opened).total_seconds() / 3600
        except (ValueError, TypeError) as e:
            logger.warning(f"Error calculating resolution time for incident {row['Number']}: {e}")
            pass
        
        # Create focused metadata optimized for efficient querying
        opened_dt = pd.to_datetime(row['Opened At'])
        
        meta = {
            # Primary identifiers
            'incident_id': row['Number'],
            
            # Core categorization (for filtering and grouping)
            'category': row['Category'],
            'subcategory': row['Subcategory'],
            
            # Priority and impact (for severity-based queries)
            'priority_level': row['Priority'].split(' - ')[0],  # Just the number
            'severity': severity,
            
            # Operational status
            'state': row['State'],
            'team': row['Assignment Group'],
            
            # Temporal attributes (for time-based queries)
            'timestamp': opened_dt.timestamp(),  # Unix timestamp for efficient range queries
            'year_month': opened_dt.strftime('%Y-%m'),  # For monthly aggregations
            'year': str(opened_dt.year),  # For yearly aggregations
            
            # Resolution metrics (if available)
            'is_resolved': bool(pd.notna(row['Resolved At'])),
            'resolution_hours': resolution_hours if resolution_hours is not None else -1,
        }
        
        documents.append(text)
        metadata.append(meta)
    
    # Convert to LangChain documents with optimized metadata
    texts = [
        Document(page_content=doc, metadata=meta)
        for doc, meta in zip(documents, metadata)
    ]
    
    # Create or load vector store
    if os.path.exists(persist_directory):
        vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    else:
        vectorstore = Chroma.from_documents(
            documents=texts,
            embedding=embeddings,
            persist_directory=persist_directory
        )
    
    return vectorstore

def create_qa_chain(vectorstore):
    """Create an enhanced conversational QA chain with dynamic prompting and retrieval"""
    template = """You are an ITIL-certified Production Support Expert specializing in ServiceNow incident analysis and resolution.
    Your role is to provide expert analysis of incidents, root cause analysis (RCA), and actionable solutions.
    
    Key Responsibilities:
    - Analyze incident patterns and trends
    - Identify root causes and systemic issues
    - Provide data-driven recommendations
    - Ensure compliance with ITIL practices
    
    Knowledge Base Context:
    - You have access to historical incident data
    - Each incident includes detailed metadata
    - Time-based patterns are important
    - Priority and severity correlations matter

    Guidelines for your responses:
    1. For analytical queries (patterns, trends, statistics):
       - Present data in HTML tables with clear headers
       - Use proper formatting: <table><tr><th>Header</th></tr><tr><td>Data</td></tr></table>
       - Include relevant metrics and percentages
       - Maximum of 10 rows unless specifically asked for more

    2. For RCA and solution queries:
       - Structure your response in clear sections
       - Keep responses concise (max 300 words)
       - Include: Root Cause, Impact, Resolution Steps, Prevention Measures
       - Highlight critical information

    3. For time-based analysis:
       - Clearly specify the time period analyzed
       - Show trends and patterns
       - Use proper date comparisons

    4. Response Format:
       - Use bullet points for lists
       - Keep paragraphs short (2-3 sentences)
       - Use HTML formatting for emphasis when needed
       - If providing steps, number them clearly

    Current Context: {context}
    Previous Conversation: {chat_history}
    Current Question: {question}

    Provide your expert analysis based on the above guidelines.
    Answer: """

    PROMPT = PromptTemplate(
        input_variables=["context", "chat_history", "question"],
        template=template
    )

    # Use GPT-4o Mini with large context window (128k tokens) at lower cost
    llm = ChatOpenAI(
        model="gpt-4o-mini",  # GPT-4o Mini with 128k context window
        temperature=0.7,
        max_tokens=4096  # Allow up to 4k tokens for response, leaving ~124k for input
    )
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    # Create retriever with only supported parameters
    retriever = vectorstore.as_retriever()
    retriever.search_kwargs = {"k": 20}  # Increased default for larger context window
    
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": PROMPT}
    )
    
    return qa_chain

# Initialize vector store and QA chain
vectorstore = initialize_vectorstore()
qa_chain = create_qa_chain(vectorstore)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/chat")
async def chat(message: ChatMessage):
    metrics = QueryMetrics()
    logger.info(f"Received question: {message.message}")
    
    try:
        # Preprocess the question to identify query type
        question = message.message.lower()
        
        # Enhanced query type detection and parameter adjustment
        k = 20  # default number of documents to retrieve (increased for GPT-4)
        search_type = "default"
        
        # Define optimized query patterns with metadata filters
        query_patterns = {
            'analytical': {
                'patterns': ['pattern', 'trend', 'all', 'how many', 'count', 'list', 'analyze', 'summarize'],
                'k': 50,
                'description': 'Analytical query for patterns and trends'
            },
            'temporal': {
                'patterns': ['between', 'from', 'to', 'during', 'within', 'time frame'],
                'k': 100,
                'description': 'Temporal analysis query'
            },
            'category': {
                'patterns': ['category', 'type of', 'similar to', 'like this'],
                'k': 25,
                'description': 'Category-based similarity query'
            },
            'priority': {
                'patterns': ['critical', 'high priority', 'urgent', 'severity'],
                'k': 30,
                'description': 'Priority-based query'
            },
            'resolution': {
                'patterns': ['resolved', 'resolution time', 'how long', 'duration'],
                'k': 40,
                'description': 'Resolution time analysis'
            },
            'team': {
                'patterns': ['team', 'group', 'assigned to', 'handled by'],
                'k': 30,
                'description': 'Team-based analysis'
            }
        }
        
        # Determine query type and adjust retrieval strategy
        for query_type, config in query_patterns.items():
            if any(pattern in question for pattern in config['patterns']):
                k = config['k']
                search_type = query_type
                logger.debug(f"{config['description']} detected, adjusting retrieval strategy: k={k}")
                break
            
        logger.info(f"Query type: {search_type}, Parameters: k={k}")
        
        # Update retriever with optimized parameters (only ChromaDB compatible params)
        qa_chain.retriever.search_kwargs.update({
            'k': k
        })
        
        # Get response from QA chain with token tracking
        with get_openai_callback() as cb:
            response = qa_chain.invoke({"question": message.message})
            metrics.record_token_usage(cb)
        
        # Post-process response for better formatting
        answer = response["answer"]
        
        # If response contains a table, ensure proper HTML formatting
        if '<table>' in answer:
            logger.debug("Table response detected, preserving HTML formatting")
            formatted_answer = answer
        else:
            # For text responses, add basic HTML formatting
            logger.debug("Text response detected, adding HTML formatting")
            formatted_answer = answer.replace('\n\n', '<br><br>')
            formatted_answer = formatted_answer.replace('•', '<br>•')
            for i in range(1, 10):
                formatted_answer = formatted_answer.replace(f"{i}.", f"<br>{i}.")
        
        # Log performance metrics
        perf_metrics = metrics.to_dict()
        logger.info("Query processed successfully", extra={
            'metrics': perf_metrics,
            'query_type': 'table' if '<table>' in answer else 'text',
            'retrieved_docs': k
        })
        
        # Log detailed metrics for analysis
        logger.debug(f"Performance metrics: {json.dumps(perf_metrics, indent=2)}")
        
        return {
            "response": formatted_answer,
            "metrics": perf_metrics
        }
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error processing query: {error_msg}", exc_info=True)
        return {
            "response": f"Error: {error_msg}",
            "metrics": metrics.to_dict()
        }
