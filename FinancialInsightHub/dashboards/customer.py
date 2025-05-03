import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def show_dashboard(data):
    """Display customer-facing transaction dashboard"""
    st.title("🧾 Your Transaction Dashboard")
    
    # Introduction text
    st.markdown("""
    <div style='background-color: #e5f0ff; padding: 1rem; border-radius: 8px; margin-bottom: 2rem;'>
        <p style='margin: 0; font-size: 1.1rem;'>
            Welcome to your personal transaction dashboard. Here you can monitor your payment activity,
            track transaction status, and analyze your financial flows with Fincra.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Simulate customer-specific data from the payments dataset
    if 'payments' in data and not data['payments'].empty:
        # For this demo, we'll filter to just show specific channels that would belong to one customer
        customer_tx_data = filter_customer_data(data['payments'])
        
        # Display metrics
        show_transaction_metrics(customer_tx_data)
        
        # Show transaction history
        show_transaction_history(customer_tx_data)
        
        # Show success rate over time
        show_success_rate_chart(customer_tx_data)
        
        # Show payment channels breakdown
        show_channel_breakdown(customer_tx_data)
        
        # Show geographical distribution
        show_geo_distribution(customer_tx_data)
        
    else:
        st.warning("No transaction data is available at the moment. Please try again later.")


def filter_customer_data(payments_data):
    """
    Filter the payments data to simulate a view for a specific customer.
    In a real implementation, this would use actual customer IDs and filters.
    """
    # In a real system, filter by customer_id
    # Here we'll just take a subset to simulate a customer's transactions
    
    # Get transactions from the last 30 days (assuming the data is sorted)
    recent_data = payments_data.sort_values('date', ascending=False).head(50)
    
    # Simulate some filtering - in reality this would filter by customer ID
    # Here we'll just take a random sample to simulate a customer's view
    customer_data = recent_data.sample(frac=0.4, random_state=42)
    
    return customer_data


def show_transaction_metrics(customer_data):
    """Display key transaction metrics"""
    # Calculate metrics
    total_volume = customer_data['transaction_volume'].sum()
    success_rate = (customer_data['successful_transactions'].sum() / 
                   customer_data['transaction_volume'].sum() * 100)
    avg_processing = customer_data['avg_processing_time_sec'].mean()
    
    # Create columns for metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Transactions", f"{int(total_volume):,}")
    
    with col2:
        st.metric("Success Rate", f"{success_rate:.1f}%")
    
    with col3:
        st.metric("Avg. Processing Time", f"{avg_processing:.2f} sec")


def show_transaction_history(customer_data):
    """Show table of recent transactions"""
    st.subheader("Recent Transactions")
    
    # Create a cleaner view for the transaction history
    history_view = customer_data[['date', 'channel', 'country', 
                                 'transaction_volume', 'successful_transactions',
                                 'failed_transactions', 'success_rate',
                                 'primary_error']].copy()
    
    # Rename columns for better readability
    history_view = history_view.rename(columns={
        'date': 'Date',
        'channel': 'Channel',
        'country': 'Country',
        'transaction_volume': 'Volume',
        'successful_transactions': 'Successful',
        'failed_transactions': 'Failed',
        'success_rate': 'Success Rate (%)',
        'primary_error': 'Primary Error'
    })
    
    # Sort by date descending
    history_view = history_view.sort_values('Date', ascending=False)
    
    # Format the success rate
    history_view['Success Rate (%)'] = history_view['Success Rate (%)'].apply(lambda x: f"{x:.1f}%")
    
    # Show the table
    st.dataframe(history_view)


def show_success_rate_chart(customer_data):
    """Show chart of success rates over time"""
    st.subheader("Transaction Success Rate Over Time")
    
    # Group by date
    success_by_date = customer_data.groupby('date').agg({
        'transaction_volume': 'sum',
        'successful_transactions': 'sum'
    }).reset_index()
    
    # Calculate success rate
    success_by_date['success_rate'] = (success_by_date['successful_transactions'] / 
                                      success_by_date['transaction_volume'] * 100)
    
    # Create the chart
    fig = px.line(success_by_date, x='date', y='success_rate',
                 labels={'date': 'Date', 'success_rate': 'Success Rate (%)'},
                 title='Transaction Success Rate Trend')
    
    # Update layout
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Success Rate (%)',
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    # Add a target line at 98%
    fig.add_hline(y=98, line_dash="dash", line_color="#ff9700",
                 annotation_text="Target (98%)", 
                 annotation_position="bottom right")
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)


def show_channel_breakdown(customer_data):
    """Show breakdown of transactions by payment channel"""
    st.subheader("Payment Channel Distribution")
    
    # Group by channel
    channel_data = customer_data.groupby('channel').agg({
        'transaction_volume': 'sum',
        'successful_transactions': 'sum',
        'failed_transactions': 'sum'
    }).reset_index()
    
    # Calculate success rate
    channel_data['success_rate'] = (channel_data['successful_transactions'] / 
                                   channel_data['transaction_volume'] * 100)
    
    # Sort by volume
    channel_data = channel_data.sort_values('transaction_volume', ascending=False)
    
    # Create the chart
    fig = px.bar(channel_data, x='channel', y='transaction_volume',
                color='success_rate', color_continuous_scale='Blues',
                labels={'channel': 'Payment Channel', 
                        'transaction_volume': 'Transaction Volume',
                        'success_rate': 'Success Rate (%)'},
                title='Transaction Volume by Payment Channel')
    
    # Update layout
    fig.update_layout(
        xaxis_title='Payment Channel',
        yaxis_title='Transaction Volume',
        coloraxis_colorbar_title='Success Rate (%)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)


def show_geo_distribution(customer_data):
    """Show geographical distribution of transactions"""
    st.subheader("Geographical Transaction Distribution")
    
    # Group by country
    geo_data = customer_data.groupby('country').agg({
        'transaction_volume': 'sum',
        'successful_transactions': 'sum'
    }).reset_index()
    
    # Calculate success rate
    geo_data['success_rate'] = (geo_data['successful_transactions'] / 
                               geo_data['transaction_volume'] * 100)
    
    # Create the chart
    fig = px.choropleth(geo_data, 
                       locations='country', 
                       locationmode='country names',
                       color='transaction_volume',
                       hover_name='country',
                       color_continuous_scale='Blues',
                       labels={'transaction_volume': 'Transaction Volume'},
                       title='Transaction Volume by Country')
    
    # Update layout
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth'
        ),
        coloraxis_colorbar_title='Transaction Volume',
        height=500,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)