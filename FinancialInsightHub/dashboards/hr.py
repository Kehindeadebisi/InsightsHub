import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

def show_dashboard(data):
    st.title("HR Dashboard")
    st.image("https://images.unsplash.com/photo-1509475826633-fed577a2c71b", width=400, caption="HR Analytics")
    
    st.markdown("""
    This dashboard provides insights into Fincra's human resources metrics, including:
    - Headcount and turnover trends
    - Leave statistics
    - Department distribution
    - Onboarding efficiency
    """)
    
    # Get the latest month
    latest_month = data['Month'].max()
    latest_data = data[data['Month'] == latest_month]
    
    # Summary metrics
    total_headcount = latest_data['Headcount'].sum()
    avg_turnover = latest_data['Turnover_Rate'].mean() * 100  # Convert to percentage
    total_new_hires = latest_data['New_Hires'].sum()
    avg_onboarding = latest_data['Avg_Onboarding_Days'].mean()
    
    # Create metrics row
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Headcount", f"{total_headcount}")
    col2.metric("Avg. Turnover Rate", f"{avg_turnover:.1f}%")
    col3.metric("New Hires (Latest Month)", f"{total_new_hires}")
    col4.metric("Avg. Onboarding Time", f"{avg_onboarding:.1f} days")
    
    # Add tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Headcount & Turnover", "Leave Analytics", "Location & Onboarding"])
    
    with tab1:
        st.subheader("Headcount by Department")
        
        # Create pie chart for headcount distribution
        fig = px.pie(
            latest_data, 
            values='Headcount', 
            names='Department',
            title='Current Headcount Distribution',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Headcount trend over time
        st.subheader("Headcount Trends")
        
        # Group by month
        headcount_trend = data.groupby(['Month', 'Department'])['Headcount'].sum().reset_index()
        
        # Create line chart
        fig = px.line(
            headcount_trend,
            x='Month',
            y='Headcount',
            color='Department',
            title='Headcount Trend by Department',
            labels={'Headcount': 'Number of Employees', 'Month': 'Month'},
            height=400
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Turnover analysis
        st.subheader("Turnover Analysis")
        
        # Convert turnover to percentage for display
        data_pct = data.copy()
        data_pct['Turnover_Rate'] = data_pct['Turnover_Rate'] * 100
        
        # Group by month
        turnover_trend = data_pct.groupby('Month')['Turnover_Rate'].mean().reset_index()
        
        # Create line chart
        fig = px.line(
            turnover_trend,
            x='Month',
            y='Turnover_Rate',
            title='Average Turnover Rate Trend',
            labels={'Turnover_Rate': 'Turnover Rate (%)', 'Month': 'Month'},
            height=350,
            markers=True
        )
        fig.update_layout(xaxis_tickangle=-45)
        fig.update_traces(line_color='red')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Leave Analytics")
        
        # Group by department for leave stats
        leave_data = latest_data.groupby('Department')[['Avg_Leave_Days', 'Sick_Days', 'Headcount']].sum().reset_index()
        leave_data['Avg_Sick_Days_Per_Employee'] = leave_data['Sick_Days'] / leave_data['Headcount']
        
        # Create combined bar chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=leave_data['Department'],
            y=leave_data['Avg_Leave_Days'],
            name='Avg Leave Days',
            marker_color='teal'
        ))
        
        fig.add_trace(go.Bar(
            x=leave_data['Department'],
            y=leave_data['Avg_Sick_Days_Per_Employee'],
            name='Avg Sick Days',
            marker_color='coral'
        ))
        
        fig.update_layout(
            title='Leave and Sick Days by Department',
            xaxis_title='Department',
            yaxis_title='Average Days per Employee',
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Leave trends over time
        st.subheader("Leave Trends Over Time")
        
        # Group by month for all departments
        leave_trend = data.groupby('Month')[['Avg_Leave_Days', 'Sick_Days', 'Headcount']].sum().reset_index()
        leave_trend['Avg_Sick_Days_Per_Employee'] = leave_trend['Sick_Days'] / leave_trend['Headcount']
        
        # Create line chart
        fig = px.line(
            leave_trend,
            x='Month',
            y=['Avg_Leave_Days', 'Avg_Sick_Days_Per_Employee'],
            title='Leave Trends Over Time',
            labels={
                'value': 'Average Days per Employee',
                'Month': 'Month',
                'variable': 'Metric'
            },
            height=400
        )
        fig.update_layout(
            xaxis_tickangle=-45,
            legend_title_text='Metric',
            yaxis_title='Average Days'
        )
        
        # Rename the legend items
        newnames = {'Avg_Leave_Days': 'Avg Leave Days', 'Avg_Sick_Days_Per_Employee': 'Avg Sick Days'}
        fig.for_each_trace(lambda t: t.update(name = newnames[t.name]))
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # Split layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Employee Distribution by Location")
            
            # Group by location
            location_data = latest_data.groupby('Location')['Headcount'].sum().reset_index()
            
            # Create bar chart
            fig = px.bar(
                location_data,
                x='Location',
                y='Headcount',
                color='Location',
                title='Employee Distribution by Location',
                labels={'Headcount': 'Number of Employees', 'Location': 'Location'},
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Remote vs. In-Office Ratio")
            
            # Calculate remote vs in-office
            remote_count = latest_data[latest_data['Location'] == 'Remote']['Headcount'].sum()
            in_office_count = latest_data[latest_data['Location'] != 'Remote']['Headcount'].sum()
            
            # Create pie chart
            fig = px.pie(
                values=[remote_count, in_office_count],
                names=['Remote', 'In-Office'],
                title='Remote vs. In-Office Employees',
                hole=0.4,
                color_discrete_sequence=['#636EFA', '#EF553B']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Onboarding Efficiency Analysis")
        
        # Group by department for onboarding
        onboarding_data = data.sort_values('Month').copy()
        
        # Calculate rolling average onboarding time by department
        dept_onboarding = onboarding_data.groupby(['Month', 'Department'])['Avg_Onboarding_Days'].mean().reset_index()
        
        # Create line chart
        fig = px.line(
            dept_onboarding,
            x='Month',
            y='Avg_Onboarding_Days',
            color='Department',
            title='Onboarding Time Trends by Department',
            labels={'Avg_Onboarding_Days': 'Average Days to Onboard', 'Month': 'Month'},
            height=400
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Department rankings
        st.subheader("Department Onboarding Efficiency Ranking")
        
        # Latest month onboarding metrics
        latest_onboarding = latest_data[['Department', 'Avg_Onboarding_Days']].sort_values('Avg_Onboarding_Days')
        
        # Create horizontal bar chart
        fig = px.bar(
            latest_onboarding,
            y='Department',
            x='Avg_Onboarding_Days',
            color='Avg_Onboarding_Days',
            orientation='h',
            title='Departments Ranked by Onboarding Efficiency (Lower is Better)',
            labels={'Avg_Onboarding_Days': 'Average Days to Onboard', 'Department': 'Department'},
            height=400,
            color_continuous_scale='RdYlGn_r'  # Reversed scale (red is higher/worse)
        )
        st.plotly_chart(fig, use_container_width=True)
