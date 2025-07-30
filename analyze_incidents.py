import configparser
import pandas as pd
from langchain_openai import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.callbacks import get_openai_callback

def load_config():
    """Load OpenAI API key from config file"""
    config = configparser.ConfigParser()
    config.read('config.properties')
    return config.get('DEFAULT', 'api_key')

def setup_llm():
    """Initialize OpenAI LLM"""
    api_key = load_config()
    return OpenAI(
        openai_api_key=api_key,
        model_name="gpt-3.5-turbo",
        temperature=0.7
    )

def create_incident_analysis_chain():
    """Create a LangChain for analyzing incidents"""
    template = """
    Analyze the following IT support incident and provide insights:
    
    Incident Number: {incident_number}
    Category: {category}
    Subcategory: {subcategory}
    Impact: {impact}
    Urgency: {urgency}
    Priority: {priority}
    State: {state}
    Description: {description}
    
    Please provide:
    1. Root cause analysis
    2. Suggested resolution steps
    3. Prevention recommendations
    """
    
    prompt = PromptTemplate(
        input_variables=["incident_number", "category", "subcategory", 
                        "impact", "urgency", "priority", "state", "description"],
        template=template
    )
    
    llm = setup_llm()
    return LLMChain(llm=llm, prompt=prompt)

def analyze_incidents(incident_file='Snow_Incidents.csv'):
    """Analyze IT support incidents using LangChain"""
    # Read incidents data
    df = pd.read_csv(incident_file)
    
    # Create analysis chain
    analysis_chain = create_incident_analysis_chain()
    
    # Analyze a sample incident (first one in this case)
    sample_incident = df.iloc[0]
    
    analysis = analysis_chain.run(
        incident_number=sample_incident['Number'],
        category=sample_incident['Category'],
        subcategory=sample_incident['Subcategory'],
        impact=sample_incident['Impact'],
        urgency=sample_incident['Urgency'],
        priority=sample_incident['Priority'],
        state=sample_incident['State'],
        description=sample_incident['Short Description']
    )
    
    print("=== Incident Analysis ===")
    print(analysis)

if __name__ == "__main__":
    analyze_incidents()
