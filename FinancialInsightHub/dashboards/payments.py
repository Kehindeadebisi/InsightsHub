import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

def show_dashboard(data):
    st.title("Payments & Operations Dashboard")
    st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71", width=400, caption="Payments Analytics")
    
    st.markdown("""
    This dashboard provides insights into Fincra's payment operations, including:
    - Transaction success and failure rates
    - Processing time analysis
    - Error monitoring and retries
    - Payment channel performance
    """)
    
    # Get the latest date
    latest_date = data['Date'].max()
    latest_data = data[data['Date'] == latest_date]
    
    # Calculate summary metrics
    total_volume = latest_data['Transaction_Volume'].sum()
    success_rate = (latest_data['Successful_Transactions'].sum() / total_volume * 100) if total_volume > 0 else 0
    avg_processing = latest_data['Avg_Processing_Time_Sec'].mean()
    total_retries = latest_data['Retry_Count'].sum()
    
    # Create metrics row
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Today's Transaction Volume", f"{total_volume:,}")
    col2.metric("Success Rate", f"{success_rate:.2f}%")
    col3.metric("Avg. Processing Time", f"{avg_processing:.2f} sec")
    col4.metric("Total Retries", f"{total_retries:,}")
    
    # Add tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Transaction Analytics", "Error Analysis", "Channel Performance"])
    
    with tab1:
        st.subheader("Transaction Success Rate Over Time")
        
        # Calculate daily success rates
        daily_stats = data.groupby('Date')[['Transaction_Volume', 'Successful_Transactions']].sum().reset_index()
        daily_stats['Success_Rate'] = daily_stats['Successful_Transactions'] / daily_stats['Transaction_Volume'] * 100
        
        # Create line chart
        fig = px.line(
            daily_stats,
            x='Date',
            y='Success_Rate',
            title='Daily Transaction Success Rate (%)',
            labels={'Success_Rate': 'Success Rate (%)', 'Date': 'Date'},
            height=400
        )
        fig.update_layout(yaxis_range=[80, 100])  # Set y-axis range for better visualization
        fig.update_traces(line_color='green', line_width=3)
        
        # Add target line at 99.5%
        fig.add_hline(y=99.5, line_dash="dash", line_color="red", annotation_text="Target (99.5%)")
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Transaction Volume Trends")
        
        # Create bar chart for transaction volume
        fig = px.bar(
            daily_stats,
            x='Date',
            y=['Successful_Transactions', 'Transaction_Volume'],
            title='Daily Transaction Volume',
            labels={
                'value': 'Number of Transactions',
                'Date': 'Date',
                'variable': 'Transaction Type'
            },
            barmode='overlay',
            height=400,
            color_discrete_map={
                'Successful_Transactions': 'green',
                'Transaction_Volume': 'lightgrey'
            }
        )
        
        # Rename the legend items
        newnames = {'Successful_Transactions': 'Successful', 'Transaction_Volume': 'Total Volume'}
        fig.for_each_trace(lambda t: t.update(name = newnames[t.name]))
        
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Processing Time Analysis")
        
        # Group by date and channel
        processing_data = data.groupby(['Date', 'Channel'])['Avg_Processing_Time_Sec'].mean().reset_index()
        
        # Create line chart
        fig = px.line(
            processing_data,
            x='Date',
            y='Avg_Processing_Time_Sec',
            color='Channel',
            title='Average Processing Time by Channel',
            labels={'Avg_Processing_Time_Sec': 'Processing Time (seconds)', 'Date': 'Date'},
            height=400
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Transaction Error Analysis")
        
        # Calculate total errors by type
        error_data = data[data['Primary_Error'] != 'None'].groupby('Primary_Error')['Failed_Transactions'].sum().reset_index()
        error_data = error_data.sort_values('Failed_Transactions', ascending=False)
        
        # Create pie chart
        fig = px.pie(
            error_data,
            values='Failed_Transactions',
            names='Primary_Error',
            title='Distribution of Transaction Errors',
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Error trends over time
        st.subheader("Error Trends Over Time")
        
        # Group by date and error type
        error_trend = data[data['Primary_Error'] != 'None'].groupby(['Date', 'Primary_Error'])['Failed_Transactions'].sum().reset_index()
        
        # Create line chart
        fig = px.line(
            error_trend,
            x='Date',
            y='Failed_Transactions',
            color='Primary_Error',
            title='Transaction Errors Over Time',
            labels={'Failed_Transactions': 'Number of Failed Transactions', 'Date': 'Date'},
            height=400
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Error by country
        st.subheader("Transaction Errors by Country")
        
        # Group by country
        country_errors = data.groupby('Country')[['Failed_Transactions', 'Transaction_Volume']].sum().reset_index()
        country_errors['Failure_Rate'] = country_errors['Failed_Transactions'] / country_errors['Transaction_Volume'] * 100
        country_errors = country_errors.sort_values('Failure_Rate', ascending=False)
        
        # Create bar chart
        fig = px.bar(
            country_errors,
            x='Country',
            y='Failure_Rate',
            color='Failure_Rate',
            title='Transaction Failure Rate by Country (%)',
            labels={'Failure_Rate': 'Failure Rate (%)', 'Country': 'Country'},
            height=400,
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Payment Channel Performance")
        
        # Group by channel
        channel_data = data.groupby('Channel')[['Transaction_Volume', 'Successful_Transactions', 'Failed_Transactions']].sum().reset_index()
        channel_data['Success_Rate'] = channel_data['Successful_Transactions'] / channel_data['Transaction_Volume'] * 100
        channel_data = channel_data.sort_values('Transaction_Volume', ascending=False)
        
        # Create combo chart
        fig = go.Figure()
        
        # Add bars for transaction volume
        fig.add_trace(go.Bar(
            x=channel_data['Channel'],
            y=channel_data['Transaction_Volume'],
            name='Transaction Volume',
            marker_color='lightblue'
        ))
        
        # Add line for success rate
        fig.add_trace(go.Scatter(
            x=channel_data['Channel'],
            y=channel_data['Success_Rate'],
            name='Success Rate (%)',
            yaxis='y2',
            line=dict(color='green', width=3),
            mode='lines+markers'
        ))
        
        # Update layout with secondary y-axis
        fig.update_layout(
            title='Payment Channel Performance',
            xaxis_title='Channel',
            yaxis=dict(
                title='Transaction Volume',
                side='left'
            ),
            yaxis2=dict(
                title='Success Rate (%)',
                side='right',
                overlaying='y',
                range=[85, 100]
            ),
            legend=dict(
                x=0.01,
                y=0.99,
                bgcolor='rgba(255, 255, 255, 0.7)'
            ),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Channel by country
        st.subheader("Channel Usage by Country")
        
        # Select country for analysis
        selected_country = st.selectbox(
            "Select Country",
            options=data['Country'].unique()
        )
        
        # Filter data for selected country
        country_channel_data = data[data['Country'] == selected_country].groupby('Channel')['Transaction_Volume'].sum().reset_index()
        country_channel_data = country_channel_data.sort_values('Transaction_Volume', ascending=False)
        
        # Create bar chart
        fig = px.bar(
            country_channel_data,
            x='Channel',
            y='Transaction_Volume',
            color='Channel',
            title=f'Payment Channel Usage in {selected_country}',
            labels={'Transaction_Volume': 'Transaction Volume', 'Channel': 'Payment Channel'},
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Retry analysis
        st.subheader("Transaction Retry Analysis")
        
        # Group by channel
        retry_data = data.groupby('Channel')[['Retry_Count', 'Failed_Transactions']].sum().reset_index()
        retry_data['Retries_per_Failure'] = retry_data['Retry_Count'] / retry_data['Failed_Transactions'].replace(0, 1)
        retry_data = retry_data.sort_values('Retries_per_Failure', ascending=False)
        
        # Create bar chart
        fig = px.bar(
            retry_data,
            x='Channel',
            y='Retries_per_Failure',
            color='Channel',
            title='Average Retries per Failed Transaction by Channel',
            labels={'Retries_per_Failure': 'Avg. Retries per Failure', 'Channel': 'Payment Channel'},
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
