import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

def show_dashboard(data):
    # Extract strategy data
    strategy_data = data['strategy']
    
    st.title("Strategy Dashboard")
    st.image("https://images.unsplash.com/photo-1600267165477-6d4cc741b379", width=400, caption="Strategic Insights")
    
    st.markdown("""
    This dashboard provides cross-functional strategic insights across Fincra, including:
    - Company-wide KPI tracking
    - Performance against targets
    - Growth metrics and trends
    - Comparative analysis across departments
    """)
    
    # Get the latest period
    latest_period = strategy_data['Period'].max()
    
    # Summary cards for latest period data
    st.subheader(f"Current Performance ({latest_period})")
    
    # Get financial KPIs
    financial_kpis = strategy_data[(strategy_data['Period'] == latest_period) & 
                               (strategy_data['KPI_Category'] == 'Financial')]
    
    # Get customer KPIs
    customer_kpis = strategy_data[(strategy_data['Period'] == latest_period) & 
                              (strategy_data['KPI_Category'] == 'Customer')]
    
    # Get operations KPIs
    operations_kpis = strategy_data[(strategy_data['Period'] == latest_period) & 
                                (strategy_data['KPI_Category'] == 'Operations')]
    
    # Create a grid of metrics
    col1, col2, col3, col4 = st.columns(4)
    
    # Financial KPIs
    with col1:
        st.markdown("### Financial")
        for _, row in financial_kpis.iterrows():
            if row['KPI_Name'] == 'Total Revenue':
                value = f"${row['Value']:,.0f}"
                st.metric(
                    row['KPI_Name'],
                    value,
                    f"{row['YoY_Growth']*100:.1f}% YoY"
                )
            else:
                value = f"{row['Value']*100:.1f}%" if row['Value'] < 1 else f"{row['Value']:.1f}"
                st.metric(
                    row['KPI_Name'],
                    value,
                    f"{row['YoY_Growth']*100:.1f}% YoY"
                )
    
    # Customer KPIs
    with col2:
        st.markdown("### Customer")
        for _, row in customer_kpis.iterrows():
            if row['KPI_Name'] == 'Active Users':
                value = f"{row['Value']:,.0f}"
            elif row['KPI_Name'] == 'Customer Satisfaction':
                value = f"{row['Value']:.1f}"
            else:
                value = f"{row['Value']:.1f}"
            
            st.metric(
                row['KPI_Name'],
                value,
                f"{row['YoY_Growth']*100:.1f}% YoY"
            )
    
    # Operations KPIs
    with col3:
        st.markdown("### Operations")
        for _, row in operations_kpis.iterrows():
            if row['KPI_Name'] == 'Transaction Volume':
                value = f"{row['Value']:,.0f}"
            elif row['KPI_Name'] == 'Transaction Success Rate':
                value = f"{row['Value']:.2f}%"
            else:
                value = f"{row['Value']:.1f}"
            
            st.metric(
                row['KPI_Name'],
                value,
                f"{row['YoY_Growth']*100:.1f}% YoY"
            )
    
    # Growth KPIs
    with col4:
        st.markdown("### Growth")
        growth_kpis = strategy_data[(strategy_data['Period'] == latest_period) & 
                               (strategy_data['KPI_Category'] == 'Growth')]
        
        for _, row in growth_kpis.iterrows():
            if row['KPI_Name'] == 'New Market Entry':
                value = f"{int(row['Value'])}"
            elif row['KPI_Name'] == 'Product Adoption Rate':
                value = f"{row['Value']*100:.1f}%"
            else:
                value = f"{row['Value']:.1f}"
            
            st.metric(
                row['KPI_Name'],
                value,
                f"{row['YoY_Growth']*100:.1f}% YoY"
            )
    
    # Add tabs for different analyses
    tab1, tab2, tab3 = st.tabs(["KPI Trends", "Target Achievement", "Cross-Department Analysis"])
    
    with tab1:
        st.subheader("KPI Trends Over Time")
        
        # Select KPI Category
        kpi_category = st.selectbox(
            "Select KPI Category",
            options=strategy_data['KPI_Category'].unique()
        )
        
        # Filter data by category
        category_data = strategy_data[strategy_data['KPI_Category'] == kpi_category]
        
        # Select specific KPI
        kpi_name = st.selectbox(
            "Select KPI",
            options=category_data['KPI_Name'].unique()
        )
        
        # Filter data by KPI name
        kpi_data = category_data[category_data['KPI_Name'] == kpi_name]
        
        # Create line chart
        fig = go.Figure()
        
        # Add value line
        fig.add_trace(go.Scatter(
            x=kpi_data['Period'],
            y=kpi_data['Value'],
            name='Actual Value',
            line=dict(color='blue', width=3)
        ))
        
        # Add target line
        fig.add_trace(go.Scatter(
            x=kpi_data['Period'],
            y=kpi_data['Target'],
            name='Target',
            line=dict(color='red', width=2, dash='dash')
        ))
        
        # Update layout
        title_text = f'{kpi_name} Trend Over Time'
        y_title = 'Value'
        
        # Format based on KPI type
        sample_value = kpi_data['Value'].iloc[0]
        if kpi_name in ['Total Revenue', 'Transaction Volume']:
            # Format large numbers
            fig.update_layout(yaxis=dict(tickformat=",.0f"))
        elif 0 <= sample_value <= 1:
            # Format as percentage
            fig.update_layout(yaxis=dict(tickformat=".1%"))
            y_title = 'Percentage'
        
        fig.update_layout(
            title=title_text,
            xaxis_title='Period',
            yaxis_title=y_title,
            height=400,
            legend=dict(
                x=0.01,
                y=0.99,
                bgcolor='rgba(255, 255, 255, 0.7)'
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # YoY growth chart
        st.subheader("Year-over-Year Growth")
        
        # Create bar chart for YoY growth
        fig = px.bar(
            kpi_data,
            x='Period',
            y='YoY_Growth',
            title=f'{kpi_name} YoY Growth Rate',
            labels={'YoY_Growth': 'YoY Growth Rate', 'Period': 'Period'},
            height=350,
            color='YoY_Growth',
            color_continuous_scale='Blues'
        )
        
        # Format y-axis as percentage
        fig.update_layout(yaxis=dict(tickformat=".1%"))
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Target Achievement Analysis")
        
        # Calculate achievement rate
        target_data = strategy_data.copy()
        target_data['Achievement_Rate'] = target_data['Value'] / target_data['Target']
        
        # Filter for latest period
        latest_achievement = target_data[target_data['Period'] == latest_period].copy()
        
        # Create achievement rate chart
        fig = px.bar(
            latest_achievement,
            x='KPI_Name',
            y='Achievement_Rate',
            color='Achievement_Rate',
            facet_col='KPI_Category',
            facet_col_wrap=2,
            title=f'KPI Target Achievement Rate ({latest_period})',
            labels={'Achievement_Rate': 'Achievement Rate', 'KPI_Name': 'KPI'},
            height=500,
            color_continuous_scale='RdYlGn',
            range_color=[0, 1.2]
        )
        
        # Add reference line at 100% achievement
        fig.add_hline(y=1, line_dash="dash", line_color="black", annotation_text="Target (100%)")
        
        # Format y-axis as percentage
        fig.update_layout(yaxis=dict(tickformat=".0%"))
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Target achievement over time
        st.subheader("Target Achievement Trends")
        
        # Select KPI for detailed view
        selected_kpi = st.selectbox(
            "Select KPI to Track Achievement Over Time",
            options=target_data['KPI_Name'].unique()
        )
        
        # Filter data for selected KPI
        kpi_achievement = target_data[target_data['KPI_Name'] == selected_kpi]
        
        # Create line chart
        fig = px.line(
            kpi_achievement,
            x='Period',
            y='Achievement_Rate',
            title=f'{selected_kpi} - Target Achievement Rate Over Time',
            labels={'Achievement_Rate': 'Achievement Rate', 'Period': 'Period'},
            height=350,
            markers=True
        )
        
        # Add reference line at 100% achievement
        fig.add_hline(y=1, line_dash="dash", line_color="black", annotation_text="Target (100%)")
        
        # Format y-axis as percentage
        fig.update_layout(yaxis=dict(tickformat=".0%"))
        
        # Color line based on achievement (green if >= 100%, orange if >= 80%, red otherwise)
        fig.update_traces(
            line=dict(
                color='green' if kpi_achievement['Achievement_Rate'].iloc[-1] >= 1 else
                      'orange' if kpi_achievement['Achievement_Rate'].iloc[-1] >= 0.8 else
                      'red',
                width=3
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Cross-Department Analysis")
        
        # Create integrated analysis using data from multiple departments
        
        # HR and Finance correlation
        st.write("### HR Costs vs. Financial Performance")
        
        # Extract relevant data
        hr_data = data['hr']
        finance_data = data['finance']
        
        # Aggregate HR data by month
        hr_monthly = hr_data.groupby('Month')['Headcount'].sum().reset_index()
        hr_monthly.columns = ['Month', 'Total_Headcount']
        
        # Aggregate Finance data by month
        # Extract month from Date for joining
        finance_data['Month'] = pd.to_datetime(finance_data['Date']).dt.strftime('%Y-%m')
        finance_monthly = finance_data.groupby('Month')[['Inflow', 'Outflow']].sum().reset_index()
        
        # Merge data
        cross_data = pd.merge(hr_monthly, finance_monthly, on='Month', how='inner')
        
        # Calculate revenue per employee
        cross_data['Revenue_Per_Employee'] = cross_data['Inflow'] / cross_data['Total_Headcount']
        
        # Create scatter plot
        fig = px.scatter(
            cross_data,
            x='Total_Headcount',
            y='Inflow',
            size='Revenue_Per_Employee',
            color='Revenue_Per_Employee',
            hover_data=['Month', 'Outflow'],
            title='Headcount vs. Revenue Relationship',
            labels={
                'Total_Headcount': 'Total Headcount',
                'Inflow': 'Total Revenue',
                'Revenue_Per_Employee': 'Revenue per Employee'
            },
            height=400,
            color_continuous_scale='Viridis'
        )
        
        # Add trendline
        fig.update_layout(
            xaxis_title="Total Headcount",
            yaxis_title="Total Revenue",
        )
        
        # Format y-axis
        fig.update_layout(yaxis=dict(tickformat=",.0f"))
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Payments and Engineering correlation
        st.write("### Transaction Success Rate vs. System Performance")
        
        # Extract relevant data
        payments_data = data['payments']
        engineering_data = data['engineering']
        
        # Convert dates to common format
        payments_data['Date_Time'] = pd.to_datetime(payments_data['Date']).dt.strftime('%Y-%m-%d')
        engineering_data['Date_Time'] = pd.to_datetime(engineering_data['Timestamp']).dt.strftime('%Y-%m-%d')
        
        # Aggregate payments data by date
        payments_daily = payments_data.groupby('Date_Time').agg({
            'Transaction_Volume': 'sum',
            'Successful_Transactions': 'sum'
        }).reset_index()
        
        payments_daily['Success_Rate'] = payments_daily['Successful_Transactions'] / payments_daily['Transaction_Volume']
        
        # Filter engineering data for Production and aggregate by date
        eng_daily = engineering_data[engineering_data['Environment'] == 'Production'].groupby('Date_Time').agg({
            'CPU_Usage': 'mean',
            'Memory_Usage': 'mean',
            'API_Latency_ms': 'mean',
            'Error_Rate': 'mean'
        }).reset_index()
        
        # Merge data
        perf_data = pd.merge(payments_daily, eng_daily, on='Date_Time', how='inner')
        
        # Create scatter plot matrix
        fig = px.scatter_matrix(
            perf_data,
            dimensions=['Success_Rate', 'API_Latency_ms', 'CPU_Usage', 'Error_Rate'],
            color='Success_Rate',
            title='Correlation Between System Performance and Transaction Success',
            height=600,
            color_continuous_scale='RdYlGn'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Overall business health dashboard
        st.write("### Business Health Dashboard")
        
        # Calculate key health metrics from all departments
        # 1. Latest financial data
        latest_finance = finance_data[finance_data['Date'] == finance_data['Date'].max()]
        fx_exposure = latest_finance['Exposure'].sum()
        net_position = latest_finance['Net_Position'].sum()
        
        # 2. Latest HR data
        latest_hr_month = hr_data['Month'].max()
        latest_hr = hr_data[hr_data['Month'] == latest_hr_month]
        headcount = latest_hr['Headcount'].sum()
        turnover = latest_hr['Turnover_Rate'].mean() * 100
        
        # 3. Latest payments data
        latest_payment_date = payments_data['Date'].max()
        latest_payments = payments_data[payments_data['Date'] == latest_payment_date]
        tx_volume = latest_payments['Transaction_Volume'].sum()
        success_rate = latest_payments['Successful_Transactions'].sum() / tx_volume * 100
        
        # 4. Latest engineering data
        latest_eng_time = engineering_data['Timestamp'].max()
        latest_eng = engineering_data[
            (engineering_data['Timestamp'] == latest_eng_time) & 
            (engineering_data['Environment'] == 'Production')
        ]
        avg_latency = latest_eng['API_Latency_ms'].mean()
        error_rate = latest_eng['Error_Rate'].mean() * 100
        
        # Create gauge charts for overall health
        col1, col2 = st.columns(2)
        
        with col1:
            # Financial Health (based on net position and revenue targets)
            revenue_target = strategy_data[
                (strategy_data['Period'] == latest_period) & 
                (strategy_data['KPI_Name'] == 'Total Revenue')
            ]['Target'].values[0]
            
            revenue_actual = strategy_data[
                (strategy_data['Period'] == latest_period) & 
                (strategy_data['KPI_Name'] == 'Total Revenue')
            ]['Value'].values[0]
            
            financial_health = min(100, (revenue_actual / revenue_target) * 100)
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = financial_health,
                title = {'text': "Financial Health"},
                gauge = {
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "green" if financial_health >= 90 else "orange" if financial_health >= 70 else "red"},
                    'steps': [
                        {'range': [0, 60], 'color': "#FF4B4B"},
                        {'range': [60, 80], 'color': "#FFBB4B"},
                        {'range': [80, 90], 'color': "#BBFF4B"},
                        {'range': [90, 100], 'color': "#4BFF4B"}
                    ],
                    'threshold': {
                        'line': {'color': "black", 'width': 2},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            
            fig.update_layout(height=250)
            st.plotly_chart(fig, use_container_width=True)
            
            # Operational Health (based on transaction success rate and system performance)
            operational_health = (success_rate * 0.6) + ((100 - error_rate * 10) * 0.4)
            operational_health = min(100, max(0, operational_health))
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = operational_health,
                title = {'text': "Operational Health"},
                gauge = {
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "green" if operational_health >= 90 else "orange" if operational_health >= 80 else "red"},
                    'steps': [
                        {'range': [0, 70], 'color': "#FF4B4B"},
                        {'range': [70, 85], 'color': "#FFBB4B"},
                        {'range': [85, 95], 'color': "#BBFF4B"},
                        {'range': [95, 100], 'color': "#4BFF4B"}
                    ],
                    'threshold': {
                        'line': {'color': "black", 'width': 2},
                        'thickness': 0.75,
                        'value': 95
                    }
                }
            ))
            
            fig.update_layout(height=250)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # HR Health (based on turnover and headcount growth)
            hr_health = 100 - turnover * 2  # Lower turnover is better
            hr_health = min(100, max(0, hr_health))
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = hr_health,
                title = {'text': "HR Health"},
                gauge = {
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "green" if hr_health >= 90 else "orange" if hr_health >= 75 else "red"},
                    'steps': [
                        {'range': [0, 60], 'color': "#FF4B4B"},
                        {'range': [60, 75], 'color': "#FFBB4B"},
                        {'range': [75, 90], 'color': "#BBFF4B"},
                        {'range': [90, 100], 'color': "#4BFF4B"}
                    ],
                    'threshold': {
                        'line': {'color': "black", 'width': 2},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            
            fig.update_layout(height=250)
            st.plotly_chart(fig, use_container_width=True)
            
            # Technical Health (based on latency and CPU/memory usage)
            system_health = 100 - (avg_latency / 10) - (latest_eng['CPU_Usage'].mean() / 10)
            system_health = min(100, max(0, system_health))
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = system_health,
                title = {'text': "Technical Health"},
                gauge = {
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "green" if system_health >= 90 else "orange" if system_health >= 75 else "red"},
                    'steps': [
                        {'range': [0, 60], 'color': "#FF4B4B"},
                        {'range': [60, 75], 'color': "#FFBB4B"},
                        {'range': [75, 90], 'color': "#BBFF4B"},
                        {'range': [90, 100], 'color': "#4BFF4B"}
                    ],
                    'threshold': {
                        'line': {'color': "black", 'width': 2},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            
            fig.update_layout(height=250)
            st.plotly_chart(fig, use_container_width=True)
