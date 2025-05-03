import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

def show_dashboard(data):
    st.title("Engineering Dashboard")
    st.image("https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3", width=400, caption="Engineering Analytics")
    
    st.markdown("""
    This dashboard provides insights into Fincra's engineering metrics, including:
    - Application performance monitoring
    - Service uptime and reliability
    - Error rates and alerts
    - Resource utilization metrics
    """)
    
    # Get the latest timestamp data
    latest_timestamp = data['Timestamp'].max()
    latest_data = data[data['Timestamp'] == latest_timestamp]
    
    # Calculate summary metrics for Production environment only
    prod_data = latest_data[latest_data['Environment'] == 'Production']
    avg_cpu = prod_data['CPU_Usage'].mean()
    avg_memory = prod_data['Memory_Usage'].mean()
    avg_latency = prod_data['API_Latency_ms'].mean()
    active_alerts = len(prod_data[prod_data['Alert'] != 'None'])
    
    # Create metrics row
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Avg CPU Usage", f"{avg_cpu:.1f}%")
    col2.metric("Avg Memory Usage", f"{avg_memory:.1f}%")
    col3.metric("Avg API Latency", f"{avg_latency:.1f} ms")
    col4.metric("Active Alerts", f"{active_alerts}")
    
    # Environment filter
    selected_env = st.radio(
        "Select Environment",
        options=['Production', 'Staging', 'Development'],
        horizontal=True,
        index=0
    )
    
    # Filter data by selected environment
    env_data = data[data['Environment'] == selected_env]
    
    # Add tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Performance Metrics", "Alerts & Errors", "Service Health"])
    
    with tab1:
        st.subheader("CPU & Memory Usage Over Time")
        
        # Select service for detailed view
        selected_service = st.selectbox(
            "Select Service",
            options=env_data['Service'].unique(),
            key="perf_metrics_service"
        )
        
        # Filter for selected service
        service_data = env_data[env_data['Service'] == selected_service]
        
        # Create dual-axis line chart
        fig = go.Figure()
        
        # Add CPU line
        fig.add_trace(go.Scatter(
            x=service_data['Timestamp'],
            y=service_data['CPU_Usage'],
            name='CPU Usage (%)',
            line=dict(color='#636EFA')
        ))
        
        # Add Memory line
        fig.add_trace(go.Scatter(
            x=service_data['Timestamp'],
            y=service_data['Memory_Usage'],
            name='Memory Usage (%)',
            line=dict(color='#EF553B')
        ))
        
        # Update layout
        fig.update_layout(
            title=f'CPU & Memory Usage for {selected_service} ({selected_env})',
            xaxis_title='Timestamp',
            yaxis_title='Usage (%)',
            height=400,
            legend=dict(
                x=0.01,
                y=0.99,
                bgcolor='rgba(255, 255, 255, 0.7)'
            )
        )
        
        # Add threshold line at 80%
        fig.add_hline(y=80, line_dash="dash", line_color="red", annotation_text="Critical Threshold (80%)")
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("API Latency & Throughput")
        
        # Create dual-axis line chart
        fig = go.Figure()
        
        # Add Latency line
        fig.add_trace(go.Scatter(
            x=service_data['Timestamp'],
            y=service_data['API_Latency_ms'],
            name='API Latency (ms)',
            line=dict(color='#00CC96')
        ))
        
        # Add Throughput line
        fig.add_trace(go.Scatter(
            x=service_data['Timestamp'],
            y=service_data['Throughput_rps'],
            name='Throughput (req/s)',
            yaxis='y2',
            line=dict(color='#AB63FA')
        ))
        
        # Update layout with secondary y-axis
        fig.update_layout(
            title=f'API Latency & Throughput for {selected_service} ({selected_env})',
            xaxis_title='Timestamp',
            yaxis=dict(
                title='Latency (ms)',
                side='left'
            ),
            yaxis2=dict(
                title='Throughput (req/s)',
                side='right',
                overlaying='y'
            ),
            legend=dict(
                x=0.01,
                y=0.99,
                bgcolor='rgba(255, 255, 255, 0.7)'
            ),
            height=400
        )
        
        # Add latency threshold line
        fig.add_hline(y=300, line_dash="dash", line_color="red", annotation_text="Latency Threshold (300ms)")
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Service Comparison")
        
        # Aggregate data by service
        service_comparison = latest_data[latest_data['Environment'] == selected_env].groupby('Service')[
            ['CPU_Usage', 'Memory_Usage', 'API_Latency_ms', 'Throughput_rps']
        ].mean().reset_index()
        
        # Select metric for comparison
        selected_metric = st.selectbox(
            "Select Metric for Comparison",
            options=['CPU_Usage', 'Memory_Usage', 'API_Latency_ms', 'Throughput_rps'],
            format_func=lambda x: {
                'CPU_Usage': 'CPU Usage (%)',
                'Memory_Usage': 'Memory Usage (%)',
                'API_Latency_ms': 'API Latency (ms)',
                'Throughput_rps': 'Throughput (req/s)'
            }[x]
        )
        
        # Create bar chart
        fig = px.bar(
            service_comparison,
            x='Service',
            y=selected_metric,
            color='Service',
            title=f'Service Comparison - {selected_metric.replace("_", " ")}',
            labels={selected_metric: selected_metric.replace("_", " ")},
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Alert Distribution")
        
        # Filter for alerts
        alert_data = env_data[env_data['Alert'] != 'None']
        
        if alert_data.empty:
            st.info(f"No alerts detected in the {selected_env} environment.")
        else:
            # Count alerts by type
            alert_counts = alert_data.groupby('Alert').size().reset_index(name='Count')
            
            # Create pie chart
            fig = px.pie(
                alert_counts,
                values='Count',
                names='Alert',
                title=f'Alert Distribution in {selected_env}',
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.Reds_r
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Error Rate Trends")
        
        # Select service for error analysis
        selected_service = st.selectbox(
            "Select Service",
            options=env_data['Service'].unique(),
            key="error_analysis_service"
        )
        
        # Filter for selected service
        service_error_data = env_data[env_data['Service'] == selected_service]
        
        # Create line chart
        fig = px.line(
            service_error_data,
            x='Timestamp',
            y='Error_Rate',
            title=f'Error Rate Trend for {selected_service} ({selected_env})',
            labels={'Error_Rate': 'Error Rate', 'Timestamp': 'Timestamp'},
            height=400
        )
        
        # Add threshold line at 0.05 (5%)
        fig.add_hline(y=0.05, line_dash="dash", line_color="red", annotation_text="Error Threshold (5%)")
        
        fig.update_traces(line_color='red', line_width=2)
        st.plotly_chart(fig, use_container_width=True)
        
        # Alert timeline
        st.subheader("Alert Timeline")
        
        if alert_data.empty:
            st.info(f"No alerts detected in the {selected_env} environment.")
        else:
            # Create timeline chart
            fig = px.scatter(
                alert_data,
                x='Timestamp',
                y='Service',
                color='Alert',
                size='CPU_Usage',  # Use CPU as size indicator
                hover_data=['Memory_Usage', 'API_Latency_ms', 'Error_Rate'],
                title=f'Alert Timeline in {selected_env}',
                height=400
            )
            
            fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Service Uptime")
        
        # Group by service
        uptime_data = env_data.groupby('Service')['Uptime_Percent'].mean().reset_index()
        uptime_data = uptime_data.sort_values('Uptime_Percent', ascending=True)
        
        # Create horizontal bar chart
        fig = px.bar(
            uptime_data,
            y='Service',
            x='Uptime_Percent',
            color='Uptime_Percent',
            orientation='h',
            title=f'Service Uptime in {selected_env}',
            labels={'Uptime_Percent': 'Uptime (%)', 'Service': 'Service'},
            height=400,
            color_continuous_scale='RdYlGn',
            range_color=[95, 100]  # Adjusted to highlight differences in high uptime values
        )
        
        # Add SLA line at 99.9%
        fig.add_vline(x=99.9, line_dash="dash", line_color="red", annotation_text="SLA (99.9%)")
        
        # Format x-axis to show narrow range clearly
        fig.update_layout(xaxis_range=[95, 100.1])
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Service Health Score")
        
        # Calculate a health score based on multiple metrics
        # Score formula: 100 - (CPU% * 0.3) - (Memory% * 0.2) - (Error_Rate * 100 * 0.3) - ((100 - Uptime_Percent) * 5)
        latest_service_data = latest_data[latest_data['Environment'] == selected_env].copy()
        latest_service_data['Health_Score'] = (
            100 
            - (latest_service_data['CPU_Usage'] * 0.3) 
            - (latest_service_data['Memory_Usage'] * 0.2) 
            - (latest_service_data['Error_Rate'] * 100 * 0.3) 
            - ((100 - latest_service_data['Uptime_Percent']) * 5)
        )
        
        # Cap score at 100 and floor at 0
        latest_service_data['Health_Score'] = latest_service_data['Health_Score'].clip(0, 100)
        
        # Group by service and calculate average
        health_data = latest_service_data.groupby('Service')['Health_Score'].mean().reset_index()
        health_data = health_data.sort_values('Health_Score', ascending=True)
        
        # Create horizontal gauge charts for each service
        for _, row in health_data.iterrows():
            service_name = row['Service']
            health_score = row['Health_Score']
            
            # Determine color based on score
            if health_score >= 90:
                color = "green"
            elif health_score >= 70:
                color = "orange"
            else:
                color = "red"
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = health_score,
                title = {'text': service_name},
                gauge = {
                    'axis': {'range': [0, 100]},
                    'bar': {'color': color},
                    'steps': [
                        {'range': [0, 50], 'color': "#FF4B4B"},
                        {'range': [50, 70], 'color': "#FFBB4B"},
                        {'range': [70, 90], 'color': "#BBFF4B"},
                        {'range': [90, 100], 'color': "#4BFF4B"}
                    ],
                    'threshold': {
                        'line': {'color': "black", 'width': 2},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            
            fig.update_layout(height=200, margin=dict(l=20, r=20, t=50, b=20))
            st.plotly_chart(fig, use_container_width=True)
