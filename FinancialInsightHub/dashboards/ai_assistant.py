import streamlit as st
import pandas as pd
from utils.openai_helper import query_openai

def show_assistant(data):
    """Display AI assistant interface"""
    st.title("🤖 AI Insights Assistant")
    
    # Descriptive text
    st.markdown("""
    <div style='background-color: #e5f0ff; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
        <h3 style='color: #2563eb; margin-top: 0;'>Ask Questions About Your Data</h3>
        <p>Use natural language to query your business data across all departments.</p>
        <p><small>Powered by OpenAI GPT-4o</small></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Suggested prompts
    st.markdown("### Example Questions")
    example_questions = [
        "What's our current FX exposure for USD?",
        "Which payment channel has the highest transaction volume?",
        "What's the turnover rate for the Engineering department?",
        "Show me the trend of API latency over time",
        "Which KPIs are below their target values?"
    ]
    
    # Display example questions as buttons
    cols = st.columns(3)
    chosen_question = None
    for i, question in enumerate(example_questions):
        if cols[i % 3].button(question, key=f"q_{i}"):
            chosen_question = question
    
    # Input area
    user_question = st.text_area("Enter your question:", value=chosen_question if chosen_question else "", height=100)
    
    # The OpenAI API key is already set in environment variables
    
    # Submit button
    if st.button("Submit Question", type="primary"):
        if user_question:
            with st.spinner("Getting insights..."):
                # Call OpenAI API
                response = query_openai(user_question, data)
                
                # Display response
                st.markdown("### Answer")
                st.markdown(f"""
                <div style='background-color: #FFFFFF; padding: 1.5rem; border-radius: 8px; 
                border-left: 4px solid #2563eb; margin-top: 0.5rem;'>
                    {response}
                </div>
                """, unsafe_allow_html=True)
                
                # Display data sources
                st.markdown("### Data Sources")
                st.markdown("This answer was generated using data from:")
                data_sources = []
                if 'finance' in data and not data['finance'].empty:
                    data_sources.append("Finance Department")
                if 'hr' in data and not data['hr'].empty:
                    data_sources.append("HR Department")
                if 'payments' in data and not data['payments'].empty:
                    data_sources.append("Payments Department")
                if 'engineering' in data and not data['engineering'].empty:
                    data_sources.append("Engineering Department")
                if 'strategy' in data and not data['strategy'].empty:
                    data_sources.append("Strategy Department")
                
                # Display data sources as pills
                cols = st.columns(len(data_sources))
                for i, source in enumerate(data_sources):
                    cols[i].markdown(f"""
                    <div style='background-color: rgba(37, 99, 235, 0.1); color: #2563eb; 
                    padding: 0.5rem; border-radius: 16px; text-align: center;'>
                        {source}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("Please enter a question.")
            
    # Help section
    with st.expander("Tips for asking good questions"):
        st.markdown("""
        - **Be specific** - Ask about particular metrics, departments, or time periods
        - **Compare data** - Ask about trends or comparisons between different metrics
        - **Ask for insights** - Ask "why" questions to get deeper analysis
        - **Complex questions** - You can ask multi-part questions that combine different data types
        """)
        
        st.markdown("#### Available Data Fields")
        st.markdown("""
        - **Finance**: Date, Currency, FX Rate, Exposure, Inflow, Outflow, Net Position, Country
        - **HR**: Month, Department, Headcount, New Hires, Terminations, Turnover Rate, Leave Days, Location
        - **Payments**: Date, Channel, Country, Transaction Volume, Success Rate, Processing Time, Errors
        - **Engineering**: Timestamp, Service, Environment, CPU/Memory Usage, API Latency, Error Rate
        - **Strategy**: Period, KPI Category, KPI Name, Value, Target, YoY Growth
        """)