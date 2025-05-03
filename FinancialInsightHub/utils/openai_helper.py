import os
import json
from openai import OpenAI

# Get OpenAI API key from environment variables
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_system_prompt(data_context):
    """Generate system prompt with context about the available data"""
    return f"""You are an AI assistant for Fincra, a payment solutions company.
You can answer questions about the company's data across multiple departments.
Here's the data context that you have access to:

{data_context}

Provide concise, accurate responses based on the data provided.
For numerical answers, include the specific values and trends when relevant.
If you're asked to make predictions or recommendations, clearly state the data-driven basis.
If you can't answer with the available data, say so clearly and suggest what additional data might help.
"""

def get_data_context(data):
    """Create a context summary of the available data for the AI"""
    context = []
    
    if 'finance' in data and not data['finance'].empty:
        sample = data['finance'].head(2)
        context.append("Finance data includes: Date, Currency, FX_Rate, Exposure, Inflow, Outflow, Net_Position, and Country.")
        context.append(f"Sample: {sample.to_string()}")
    
    if 'hr' in data and not data['hr'].empty:
        sample = data['hr'].head(2)
        context.append("HR data includes: Month, Department, Headcount, New_Hires, Terminations, Turnover_Rate, Avg_Leave_Days, Sick_Days, Location, and Avg_Onboarding_Days.")
        context.append(f"Sample: {sample.to_string()}")
    
    if 'payments' in data and not data['payments'].empty:
        sample = data['payments'].head(2)
        context.append("Payments data includes: Date, Channel, Country, Transaction_Volume, Successful_Transactions, Failed_Transactions, Success_Rate, Avg_Processing_Time_Sec, Retry_Count, and Primary_Error.")
        context.append(f"Sample: {sample.to_string()}")
    
    if 'engineering' in data and not data['engineering'].empty:
        sample = data['engineering'].head(2)
        context.append("Engineering data includes: Timestamp, Service, Environment, CPU_Usage, Memory_Usage, API_Latency_ms, Throughput_rps, Error_Rate, Alert, and Uptime_Percent.")
        context.append(f"Sample: {sample.to_string()}")
    
    if 'strategy' in data and not data['strategy'].empty:
        sample = data['strategy'].head(2)
        context.append("Strategy data includes: Period, KPI_Category, KPI_Name, Value, Target, and YoY_Growth.")
        context.append(f"Sample: {sample.to_string()}")
    
    return "\n\n".join(context)

def query_openai(question, data):
    """Query OpenAI with the user's question and data context"""
    try:
        # Prepare data context
        data_context = get_data_context(data)
        
        # Generate system prompt
        system_prompt = generate_system_prompt(data_context)
        
        # Make the API call to OpenAI
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error querying OpenAI: {str(e)}"