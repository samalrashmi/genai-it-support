# Enterprise RAG IT Support Assistant

A sophisticated Retrieval-Augmented Generation (RAG) system designed for enterprise IT support operations, leveraging ServiceNow incident data to provide intelligent assistance with root cause analysis, incident patterns, and ITIL-compliant resolution guidance.

## 🏗️ Architecture Overview

This application implements a state-of-the-art RAG architecture combining semantic search, conversational AI, and enterprise-grade incident management expertise.

```
┌─────────────────────────────────────────────────────────────────┐
│                     Enterprise RAG Architecture                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────────┐    │
│  │   FastAPI   │    │   LangChain  │    │   OpenAI GPT    │    │
│  │  Web Layer  │◄──►│   RAG Chain  │◄──►│   4o Mini       │    │
│  └─────────────┘    └──────────────┘    └─────────────────┘    │
│         │                   │                       │          │
│         ▼                   ▼                       ▼          │
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────────┐    │
│  │  HTML/JS    │    │   ChromaDB   │    │  OpenAI Embed   │    │
│  │  Frontend   │    │ Vector Store │    │   Text-Ada-002  │    │
│  └─────────────┘    └──────────────┘    └─────────────────┘    │
│                             │                                  │
│                             ▼                                  │
│                    ┌──────────────┐                           │
│                    │ ServiceNow   │                           │
│                    │ Incident CSV │                           │
│                    └──────────────┘                           │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 RAG Process Flow

The RAG system follows a sophisticated multi-stage process for intelligent incident analysis:

### 1. Data Ingestion & Preprocessing

```mermaid
graph TD
    A[ServiceNow CSV Data] --> B[Data Preprocessing]
    B --> C[ITIL Structure Mapping]
    C --> D[Metadata Extraction]
    D --> E[Text Embedding Generation]
    E --> F[ChromaDB Vector Storage]
    
    B --> B1[Priority Classification]
    B --> B2[Resolution Time Calculation]
    B --> B3[Category Standardization]
    
    D --> D1[Temporal Attributes]
    D --> D2[Priority Levels]
    D --> D3[Team Assignments]
```

### 2. Query Processing & Retrieval

```mermaid
sequenceDiagram
    participant U as User
    participant API as FastAPI
    participant QP as Query Processor
    participant VS as Vector Store
    participant LLM as GPT-4o Mini
    
    U->>API: Submit Query
    API->>QP: Analyze Query Type
    QP->>QP: Determine Retrieval Strategy
    QP->>VS: Semantic Search (k=20-100)
    VS->>QP: Return Relevant Documents
    QP->>LLM: Generate Response with Context
    LLM->>API: ITIL-Compliant Response
    API->>U: Formatted JSON Response
```

### 3. Intelligent Query Classification

The system automatically detects query types and optimizes retrieval accordingly:

| Query Type | Patterns | Documents Retrieved | Use Case |
|------------|----------|-------------------|----------|
| **Analytical** | `pattern`, `trend`, `how many`, `count` | k=50 | Statistical analysis, reporting |
| **Temporal** | `between`, `within`, `time frame` | k=100 | Time-based incident analysis |
| **Category** | `similar to`, `type of`, `like this` | k=25 | Incident classification queries |
| **Priority** | `critical`, `urgent`, `severity` | k=30 | Priority-based filtering |
| **Resolution** | `resolved`, `resolution time`, `duration` | k=40 | Performance metrics analysis |
| **Team** | `assigned to`, `team`, `group` | k=30 | Team performance analysis |

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- OpenAI API Key
- Git
- 4GB+ RAM (for vector storage)

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/samalrashmi/genai-it-support.git
   cd genai-it-support
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure OpenAI API Key**
   
   Create `config.properties` file:
   ```ini
   [DEFAULT]
   apikey = your_openai_api_key_here
   ```

5. **Setup Logging Configuration**
   
   Create `logging.conf` file:
   ```ini
   [loggers]
   keys=root,chatbot

   [handlers]
   keys=consoleHandler,fileHandler

   [formatters]
   keys=simpleFormatter

   [logger_root]
   level=DEBUG
   handlers=consoleHandler

   [logger_chatbot]
   level=DEBUG
   handlers=consoleHandler,fileHandler
   qualname=chatbot
   propagate=0

   [handler_consoleHandler]
   class=StreamHandler
   level=INFO
   formatter=simpleFormatter
   args=(sys.stdout,)

   [handler_fileHandler]
   class=FileHandler
   level=DEBUG
   formatter=simpleFormatter
   args=('logs/chatbot.log',)

   [formatter_simpleFormatter]
   format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
   ```

6. **Create HTML Template**
   
   Create `templates/chat.html`:
   ```html
   <!DOCTYPE html>
   <html>
   <head>
       <title>IT Support Assistant</title>
       <style>
           body { font-family: Arial, sans-serif; margin: 20px; }
           .chat-container { max-width: 800px; margin: 0 auto; }
           .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
           .user { background-color: #e3f2fd; text-align: right; }
           .assistant { background-color: #f5f5f5; }
           .metrics { font-size: 0.8em; color: #666; margin-top: 5px; }
           input[type="text"] { width: 70%; padding: 10px; }
           button { padding: 10px 20px; }
       </style>
   </head>
   <body>
       <div class="chat-container">
           <h1>🔧 Enterprise IT Support Assistant</h1>
           <div id="chat-messages"></div>
           <div>
               <input type="text" id="message-input" placeholder="Ask about incidents, patterns, or troubleshooting...">
               <button onclick="sendMessage()">Send</button>
           </div>
       </div>
       
       <script>
           async function sendMessage() {
               const input = document.getElementById('message-input');
               const message = input.value.trim();
               if (!message) return;
               
               addMessage(message, 'user');
               input.value = '';
               
               try {
                   const response = await fetch('/chat', {
                       method: 'POST',
                       headers: {'Content-Type': 'application/json'},
                       body: JSON.stringify({message: message})
                   });
                   
                   const data = await response.json();
                   addMessage(data.response, 'assistant', data.metrics);
               } catch (error) {
                   addMessage('Error: ' + error.message, 'assistant');
               }
           }
           
           function addMessage(text, sender, metrics = null) {
               const container = document.getElementById('chat-messages');
               const div = document.createElement('div');
               div.className = `message ${sender}`;
               div.innerHTML = text;
               
               if (metrics) {
                   const metricsDiv = document.createElement('div');
                   metricsDiv.className = 'metrics';
                   metricsDiv.innerHTML = `
                       ⏱️ ${metrics.response_time} | 
                       🔢 ${metrics.total_tokens} tokens | 
                       💰 ${metrics.cost}
                   `;
                   div.appendChild(metricsDiv);
               }
               
               container.appendChild(div);
               container.scrollTop = container.scrollHeight;
           }
           
           document.getElementById('message-input').addEventListener('keypress', function(e) {
               if (e.key === 'Enter') sendMessage();
           });
       </script>
   </body>
   </html>
   ```

7. **Prepare Incident Data**
   
   Ensure your `Snow_Incidents.csv` file contains the following columns:
   ```
   Number, State, Category, Subcategory, Impact, Urgency, Priority, 
   Opened At, Resolved At, Assignment Group, Assigned To, 
   Short Description, Notes
   ```

### Running the Application

1. **Start the Server**
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Access the Application**
   - **Web Interface:** http://localhost:8000
   - **API Documentation:** http://localhost:8000/docs
   - **Chat Endpoint:** `POST http://localhost:8000/chat`

### API Usage Examples

**Using cURL:**
```bash
# Analytical Query
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "How many incidents were resolved within 24 hours?"}'

# Pattern Analysis
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the patterns in Critical priority Network incidents?"}'

# RCA Query
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me the RCA for incident INC0012347"}'
```

## 🔧 Technical Details

### Core Components

#### 1. Vector Store Implementation
```python
# ChromaDB with OpenAI Embeddings
embeddings = OpenAIEmbeddings()
vectorstore = Chroma(
    persist_directory='vectordb',
    embedding_function=embeddings
)
```

#### 2. Dynamic Query Processing
```python
# Intelligent retrieval based on query type
query_patterns = {
    'analytical': {'k': 50, 'patterns': ['pattern', 'trend', 'how many']},
    'temporal': {'k': 100, 'patterns': ['between', 'within', 'time frame']},
    'category': {'k': 25, 'patterns': ['similar to', 'type of']}
}
```

#### 3. ITIL-Compliant Response Generation
```python
# GPT-4o Mini with optimized prompting
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    max_tokens=4096
)
```

### Data Processing Pipeline

#### 1. Incident Text Preparation
Each incident is transformed into a structured format:
```
=== Incident Details ===
Incident Number: INC0012347
Status: Resolved

=== Classification ===
Category: Hardware
Subcategory: Printer

=== Priority Assessment ===
Impact: Medium
Urgency: High
Priority: 2 - High
Overall Severity: High
```

#### 2. Metadata Optimization
Optimized metadata structure for efficient querying:
```python
metadata = {
    'incident_id': 'INC0012347',
    'category': 'Hardware',
    'subcategory': 'Printer',
    'priority_level': '2',
    'severity': 'High',
    'state': 'Resolved',
    'team': 'Desktop Support',
    'timestamp': 1721970000.0,
    'year_month': '2025-07',
    'resolution_hours': 5.5
}
```

### Performance Optimizations

1. **Context Window Management**: 128k token capacity with GPT-4o Mini
2. **Dynamic Document Retrieval**: Adjusts k parameter based on query complexity
3. **Intelligent Caching**: ChromaDB persistence for fast startup
4. **Cost Optimization**: 98.5% cost reduction vs GPT-4 (~$0.003 per query)

## 📊 System Capabilities

### Query Types Supported

1. **Root Cause Analysis (RCA)**
   - `"Show me the RCA for incident INC0012347"`
   - Provides structured analysis with impact, resolution steps, and prevention measures

2. **Pattern Analysis**
   - `"What are the patterns in Critical priority incidents?"`
   - Generates HTML tables with statistical breakdowns

3. **Temporal Analysis**
   - `"How many incidents were resolved within 24 hours between July 1-15?"`
   - Time-based filtering and trend analysis

4. **Category Analysis**
   - `"What incidents are similar to INC0012347?"`
   - Semantic similarity matching

5. **Performance Metrics**
   - `"What's the average resolution time for Hardware incidents?"`
   - SLA and performance reporting

### Response Formats

The system provides responses in multiple formats:

- **HTML Tables**: For analytical queries with structured data
- **ITIL Sections**: Root Cause, Impact, Resolution Steps, Prevention
- **Bullet Points**: For step-by-step procedures
- **Metrics**: Real-time token usage, cost, and performance data

## 🛠️ Development

### Project Structure
```
genai-it-support/
├── app.py                 # Main FastAPI application
├── requirements.txt       # Python dependencies
├── config.properties      # OpenAI API configuration
├── logging.conf          # Logging configuration
├── Snow_Incidents.csv    # Incident data
├── templates/
│   └── chat.html         # Web interface
├── vectordb/             # ChromaDB persistence
├── logs/                 # Application logs
└── README.md            # This file
```

### Key Dependencies
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
langchain==0.0.350
langchain-openai==0.0.5
langchain-community==0.0.10
chromadb==0.4.18
pandas==2.1.4
openai==1.3.8
jinja2==3.1.2
python-multipart==0.0.6
```

### Configuration Management

The application uses `config.properties` for environment-specific settings:
```ini
[DEFAULT]
apikey = your_openai_api_key_here

[DATABASE]
persist_directory = vectordb
chunk_size = 1000

[MODEL]
model_name = gpt-4o-mini
temperature = 0.7
max_tokens = 4096
```

## 🔍 Monitoring & Observability

### Logging Levels
- **INFO**: Query processing, performance metrics
- **DEBUG**: Detailed retrieval parameters, token usage
- **ERROR**: Exception handling and error recovery

### Performance Metrics
Real-time tracking of:
- Response time (typically 10-30 seconds)
- Token usage (input/output breakdown)
- Cost per query (~$0.003 average)
- Retrieved document count

### Health Checks
Monitor application health via:
```bash
curl http://localhost:8000/
```

## 🚀 Production Deployment

### Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables
```bash
export OPENAI_API_KEY="your_api_key_here"
export ENVIRONMENT="production"
export LOG_LEVEL="INFO"
```

### Scaling Considerations
- **Vector Store**: ChromaDB handles 100k+ documents efficiently
- **Memory**: 4GB+ recommended for large incident datasets
- **CPU**: Multi-core beneficial for concurrent requests
- **Storage**: SSD recommended for vector database persistence

## 📈 Performance Benchmarks

| Metric | Value | Notes |
|--------|-------|-------|
| **Average Response Time** | 15-25 seconds | Complex analytical queries |
| **Token Efficiency** | 15k-17k tokens | Large context utilization |
| **Cost per Query** | $0.0026-0.0029 | GPT-4o Mini optimization |
| **Context Window** | 128k tokens | Handles large document sets |
| **Throughput** | 10-20 queries/min | Single instance capacity |

## 🔒 Security & Compliance

### Data Privacy
- Incident data processed locally
- No data transmitted to third parties (except OpenAI API)
- Vector embeddings stored locally in ChromaDB

### API Security
- Input validation and sanitization
- Error handling without data exposure
- Configurable logging levels

### ITIL Compliance
- Structured incident categorization
- Standard priority and impact matrices
- Resolution tracking and metrics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-capability`
3. Commit changes: `git commit -am 'Add new capability'`
4. Push to branch: `git push origin feature/new-capability`
5. Submit a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For technical support or questions:
1. Check the logs in `logs/chatbot.log`
2. Verify OpenAI API key configuration
3. Ensure incident data format matches expected schema
4. Submit issues via GitHub Issues

---

**Built with ❤️ for Enterprise IT Operations**

*Leveraging the power of RAG, LangChain, and OpenAI to revolutionize IT support intelligence.*