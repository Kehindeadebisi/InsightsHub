import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Fincra color palette
FINCRA_COLORS = {
    "blue": "#005C3E",  # Deep Green
    "green": "#007A3E",  # Vibrant Green
    "light_green": "#D9EBE2",  # Light Gray
    "dark_gray": "#3D3935",
    "white": "#FFFFFF",
    "chart_green": "#17A16C",  # Lighter green for better chart visibility
    "chart_red": "#E74C3C",  # Red for negative values/outflows
    "chart_blue": "#2E86C1"  # Blue for neutral indicators
}

def show_dashboard(data):
    # Header with stylized subtitle
    st.markdown(f"""
    <h1>Finance Dashboard</h1>
    <p style='font-size: 1.2rem; color: {FINCRA_COLORS["dark_gray"]}; margin-bottom: 1.5rem;'>
        Real-time Asset Liability Management (ALM)
    </p>
    """, unsafe_allow_html=True)
    
    # Modern finance image with better styling
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"""
        <div style='background-color: {FINCRA_COLORS["light_green"]}; padding: 1.5rem; border-radius: 10px;'>
            <h3 style='color: {FINCRA_COLORS["blue"]}; margin-top: 0;'>Financial Analytics</h3>
            <p>
                This dashboard provides insights into Fincra's financial operations, including:
            </p>
            <ul>
                <li><b>FX Exposure Monitoring:</b> Track currency risk and exposure in real-time</li>
                <li><b>Cash Flow Analysis:</b> Monitor inflows, outflows, and net positions</li>
                <li><b>Geographic Distribution:</b> View financial activity across markets</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.image("https://images.unsplash.com/photo-1560472354-b33ff0c44a43", 
                 caption="Real-time financial metrics")
    
    # Summary metrics
    latest_date = data['Date'].max()
    latest_data = data[data['Date'] == latest_date]
    
    total_exposure = latest_data['Exposure'].sum()
    net_cash_position = latest_data['Net_Position'].sum()
    total_inflow = latest_data['Inflow'].sum()
    total_outflow = latest_data['Outflow'].sum()
    
    # Enhanced date display for context
    st.markdown(f"""
    <div style='margin-top: 1rem; margin-bottom: 1rem; text-align: right;'>
        <span style='background-color: {FINCRA_COLORS["blue"]}; color: white; padding: 0.4rem 0.8rem; border-radius: 20px; font-size: 0.9rem;'>
            <b>Latest Data:</b> {latest_date}
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Create improved metrics row with better styling
    st.markdown("<div class='metrics-container'>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    # Improved metric displays with icons and color indicators
    with col1:
        st.markdown(f"""
        <div style='background-color: {FINCRA_COLORS["light_green"]}; padding: 1rem; border-radius: 10px; 
        border-left: 5px solid {FINCRA_COLORS["blue"]}; height: 100%;'>
            <h4 style='margin: 0; color: {FINCRA_COLORS["dark_gray"]}; font-size: 1rem;'>Total FX Exposure</h4>
            <p style='font-size: 1.8rem; font-weight: 600; margin: 0.5rem 0 0 0; color: {FINCRA_COLORS["blue"]};'>
                ${total_exposure:,.0f}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Determine color for net position (green for positive, red for negative)
        position_color = FINCRA_COLORS["chart_green"] if net_cash_position >= 0 else FINCRA_COLORS["chart_red"]
        position_sign = "+" if net_cash_position > 0 else ""
        
        st.markdown(f"""
        <div style='background-color: {FINCRA_COLORS["light_green"]}; padding: 1rem; border-radius: 10px; 
        border-left: 5px solid {position_color}; height: 100%;'>
            <h4 style='margin: 0; color: {FINCRA_COLORS["dark_gray"]}; font-size: 1rem;'>Net Cash Position</h4>
            <p style='font-size: 1.8rem; font-weight: 600; margin: 0.5rem 0 0 0; color: {position_color};'>
                {position_sign}${net_cash_position:,.0f}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style='background-color: {FINCRA_COLORS["light_green"]}; padding: 1rem; border-radius: 10px; 
        border-left: 5px solid {FINCRA_COLORS["chart_green"]}; height: 100%;'>
            <h4 style='margin: 0; color: {FINCRA_COLORS["dark_gray"]}; font-size: 1rem;'>Total Inflow (Today)</h4>
            <p style='font-size: 1.8rem; font-weight: 600; margin: 0.5rem 0 0 0; color: {FINCRA_COLORS["chart_green"]};'>
                ${total_inflow:,.0f}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style='background-color: {FINCRA_COLORS["light_green"]}; padding: 1rem; border-radius: 10px; 
        border-left: 5px solid {FINCRA_COLORS["chart_red"]}; height: 100%;'>
            <h4 style='margin: 0; color: {FINCRA_COLORS["dark_gray"]}; font-size: 1rem;'>Total Outflow (Today)</h4>
            <p style='font-size: 1.8rem; font-weight: 600; margin: 0.5rem 0 0 0; color: {FINCRA_COLORS["chart_red"]};'>
                ${total_outflow:,.0f}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Add visually enhanced tabs for different sections
    st.markdown("<br>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📊 FX Exposure", "💰 Cash Flow Analysis", "🌎 Geographic Distribution"])
    
    with tab1:
        # Section title with better styling
        st.markdown(f"""
        <h3 style='color: {FINCRA_COLORS["blue"]}; margin-bottom: 1rem;'>Currency Exposure Analysis</h3>
        """, unsafe_allow_html=True)
        
        # Two-column layout for charts
        fx_col1, fx_col2 = st.columns([3, 2])
        
        with fx_col1:
            # Prepare data
            currency_exposure = latest_data.groupby('Currency')[['Exposure']].sum().reset_index()
            
            # Create enhanced bar chart with Fincra branding colors
            fig = px.bar(
                currency_exposure,
                x='Currency',
                y='Exposure',
                color='Currency',
                title='FX Exposure by Currency',
                labels={'Exposure': 'Exposure Amount (USD)', 'Currency': 'Currency'},
                height=400,
                color_discrete_sequence=px.colors.sequential.Greens_r  # Green color palette to match Fincra
            )
            
            # Improve chart styling
            fig.update_layout(
                plot_bgcolor=FINCRA_COLORS["white"],
                paper_bgcolor=FINCRA_COLORS["white"],
                title_font=dict(size=18, color=FINCRA_COLORS["blue"]),
                title_x=0.5,  # Center the title
                xaxis=dict(
                    title_font=dict(size=14),
                    tickfont=dict(size=12),
                    gridcolor=FINCRA_COLORS["light_green"]
                ),
                yaxis=dict(
                    title_font=dict(size=14),
                    tickfont=dict(size=12),
                    gridcolor=FINCRA_COLORS["light_green"],
                    tickformat="$,.0f"  # Format y-axis values as currency
                ),
                legend_title_font=dict(size=12),
                legend_font=dict(size=10)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with fx_col2:
            # Create a pie chart to better visualize the exposure distribution
            fig = px.pie(
                currency_exposure,
                values='Exposure',
                names='Currency',
                title='Exposure Distribution (%)',
                hole=0.4,  # Create a donut chart
                color_discrete_sequence=px.colors.sequential.Greens_r
            )
            
            # Improve chart styling
            fig.update_layout(
                plot_bgcolor=FINCRA_COLORS["white"],
                paper_bgcolor=FINCRA_COLORS["white"],
                title_font=dict(size=18, color=FINCRA_COLORS["blue"]),
                title_x=0.5,  # Center the title
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # FX Rate Trends over time with enhanced styling
        st.markdown(f"""
        <h3 style='color: {FINCRA_COLORS["blue"]}; margin-top: 1.5rem; margin-bottom: 1rem;'>FX Rate Trends</h3>
        """, unsafe_allow_html=True)
        
        # Filter for specific currencies with improved select box
        selected_currencies = st.multiselect(
            "Select Currencies to Compare", 
            options=data['Currency'].unique(),
            default=['USD', 'EUR', 'GBP', 'NGN']
        )
        
        if selected_currencies:
            # Filter data
            filtered_data = data[data['Currency'].isin(selected_currencies)]
            
            # Create enhanced line chart
            fig = px.line(
                filtered_data,
                x='Date',
                y='FX_Rate',
                color='Currency',
                title='FX Rate Trends Over Time',
                labels={'FX_Rate': 'Exchange Rate', 'Date': 'Date', 'Currency': 'Currency'},
                height=450,
                color_discrete_sequence=[FINCRA_COLORS["blue"], FINCRA_COLORS["chart_green"], 
                                        FINCRA_COLORS["chart_blue"], FINCRA_COLORS["chart_red"]]
            )
            
            # Add markers to make the lines more readable
            fig.update_traces(mode='lines+markers', marker=dict(size=6))
            
            # Improve chart styling for better readability
            fig.update_layout(
                plot_bgcolor=FINCRA_COLORS["white"],
                paper_bgcolor=FINCRA_COLORS["white"],
                title_font=dict(size=18, color=FINCRA_COLORS["blue"]),
                title_x=0.5,
                xaxis=dict(
                    title_font=dict(size=14),
                    tickfont=dict(size=12),
                    gridcolor=FINCRA_COLORS["light_green"],
                    tickangle=-45
                ),
                yaxis=dict(
                    title_font=dict(size=14),
                    tickfont=dict(size=12),
                    gridcolor=FINCRA_COLORS["light_green"]
                ),
                legend_title_font=dict(size=12),
                legend_font=dict(size=10),
                hovermode="x unified"  # Show all values at the same x position
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Add an explanation box with insights
            st.markdown(f"""
            <div style='background-color: {FINCRA_COLORS["light_green"]}; padding: 1rem; border-radius: 8px; margin-top: 1rem;'>
                <h4 style='margin-top: 0; color: {FINCRA_COLORS["blue"]};'>FX Rate Insights</h4>
                <p>
                    This chart shows the exchange rate trends for the selected currencies against USD.
                    Track daily fluctuations to better manage FX exposure and optimize timing for currency conversions.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Please select at least one currency to view FX rate trends.")
    
    with tab2:
        # Section title with better styling
        st.markdown(f"""
        <h3 style='color: {FINCRA_COLORS["blue"]}; margin-bottom: 1rem;'>Cash Flow Analysis</h3>
        <p>Monitor daily cash flows and track inflows vs. outflows over time</p>
        """, unsafe_allow_html=True)
        
        # Aggregating data by date
        daily_cash_flow = data.groupby('Date')[['Inflow', 'Outflow', 'Net_Position']].sum().reset_index()
        
        # Creating enhanced combined chart
        fig = go.Figure()
        
        # Add bar charts for inflow and outflow with improved colors
        fig.add_trace(go.Bar(
            x=daily_cash_flow['Date'],
            y=daily_cash_flow['Inflow'],
            name='Inflow',
            marker_color=FINCRA_COLORS["chart_green"]
        ))
        
        fig.add_trace(go.Bar(
            x=daily_cash_flow['Date'],
            y=daily_cash_flow['Outflow'],
            name='Outflow',
            marker_color=FINCRA_COLORS["chart_red"]
        ))
        
        # Add line for net position
        fig.add_trace(go.Scatter(
            x=daily_cash_flow['Date'],
            y=daily_cash_flow['Net_Position'],
            name='Net Position',
            line=dict(color=FINCRA_COLORS["blue"], width=3),
            mode='lines+markers'
        ))
        
        # Update layout with improved styling
        fig.update_layout(
            title='Daily Cash Flow Analysis',
            title_font=dict(size=18, color=FINCRA_COLORS["blue"]),
            title_x=0.5,
            xaxis_title='Date',
            yaxis_title='Amount (USD)',
            barmode='group',
            height=500,
            plot_bgcolor=FINCRA_COLORS["white"],
            paper_bgcolor=FINCRA_COLORS["white"],
            xaxis=dict(
                tickangle=-45,
                tickmode='auto',
                nticks=10,
                gridcolor=FINCRA_COLORS["light_green"],
                title_font=dict(size=14),
                tickfont=dict(size=12)
            ),
            yaxis=dict(
                gridcolor=FINCRA_COLORS["light_green"],
                title_font=dict(size=14),
                tickfont=dict(size=12),
                tickformat="$,.0f"  # Format y-axis values as currency
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            hovermode="x unified"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add a metrics row for cash flow statistics
        cash_flow_metrics = st.columns(4)
        
        # Calculate metrics for the displayed period
        avg_inflow = daily_cash_flow['Inflow'].mean()
        avg_outflow = daily_cash_flow['Outflow'].mean()
        avg_net = daily_cash_flow['Net_Position'].mean()
        total_net = daily_cash_flow['Net_Position'].sum()
        
        # Display enhanced metrics
        with cash_flow_metrics[0]:
            st.markdown(f"""
            <div style='text-align: center; padding: 0.5rem; background-color: {FINCRA_COLORS["light_green"]}; border-radius: 8px;'>
                <p style='margin: 0; font-size: 0.9rem; color: {FINCRA_COLORS["dark_gray"]};'>Avg. Daily Inflow</p>
                <p style='margin: 0; font-size: 1.4rem; font-weight: 600; color: {FINCRA_COLORS["chart_green"]};'>${avg_inflow:,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with cash_flow_metrics[1]:
            st.markdown(f"""
            <div style='text-align: center; padding: 0.5rem; background-color: {FINCRA_COLORS["light_green"]}; border-radius: 8px;'>
                <p style='margin: 0; font-size: 0.9rem; color: {FINCRA_COLORS["dark_gray"]};'>Avg. Daily Outflow</p>
                <p style='margin: 0; font-size: 1.4rem; font-weight: 600; color: {FINCRA_COLORS["chart_red"]};'>${avg_outflow:,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
            
        with cash_flow_metrics[2]:
            net_color = FINCRA_COLORS["chart_green"] if avg_net >= 0 else FINCRA_COLORS["chart_red"]
            net_sign = "+" if avg_net > 0 else ""
            st.markdown(f"""
            <div style='text-align: center; padding: 0.5rem; background-color: {FINCRA_COLORS["light_green"]}; border-radius: 8px;'>
                <p style='margin: 0; font-size: 0.9rem; color: {FINCRA_COLORS["dark_gray"]};'>Avg. Daily Net</p>
                <p style='margin: 0; font-size: 1.4rem; font-weight: 600; color: {net_color};'>{net_sign}${avg_net:,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
            
        with cash_flow_metrics[3]:
            total_net_color = FINCRA_COLORS["chart_green"] if total_net >= 0 else FINCRA_COLORS["chart_red"]
            total_net_sign = "+" if total_net > 0 else ""
            st.markdown(f"""
            <div style='text-align: center; padding: 0.5rem; background-color: {FINCRA_COLORS["light_green"]}; border-radius: 8px;'>
                <p style='margin: 0; font-size: 0.9rem; color: {FINCRA_COLORS["dark_gray"]};'>Total Net Position</p>
                <p style='margin: 0; font-size: 1.4rem; font-weight: 600; color: {total_net_color};'>{total_net_sign}${total_net:,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Currency breakdown with improved visualization
        st.markdown(f"""
        <h3 style='color: {FINCRA_COLORS["blue"]}; margin-top: 2rem; margin-bottom: 1rem;'>Currency Breakdown</h3>
        <p>Inflow and outflow analysis by currency</p>
        """, unsafe_allow_html=True)
        
        # Group by currency
        currency_flow = data.groupby('Currency')[['Inflow', 'Outflow']].sum().reset_index()
        currency_flow['Net'] = currency_flow['Inflow'] - currency_flow['Outflow']
        
        # Create enhanced stacked bar chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=currency_flow['Currency'],
            y=currency_flow['Inflow'],
            name='Inflow',
            marker_color=FINCRA_COLORS["chart_green"]
        ))
        
        fig.add_trace(go.Bar(
            x=currency_flow['Currency'],
            y=currency_flow['Outflow'],
            name='Outflow',
            marker_color=FINCRA_COLORS["chart_red"]
        ))
        
        # Add net position as a line
        fig.add_trace(go.Scatter(
            x=currency_flow['Currency'],
            y=currency_flow['Net'],
            name='Net Position',
            mode='markers+lines',
            marker=dict(size=10, symbol='circle', color=FINCRA_COLORS["blue"]),
            line=dict(width=3, color=FINCRA_COLORS["blue"])
        ))
        
        # Improve chart styling
        fig.update_layout(
            title='Inflow and Outflow by Currency',
            title_font=dict(size=18, color=FINCRA_COLORS["blue"]),
            title_x=0.5,
            xaxis_title='Currency',
            yaxis_title='Amount (USD)',
            barmode='group',
            height=450,
            plot_bgcolor=FINCRA_COLORS["white"],
            paper_bgcolor=FINCRA_COLORS["white"],
            xaxis=dict(
                title_font=dict(size=14),
                tickfont=dict(size=12),
                gridcolor=FINCRA_COLORS["light_green"]
            ),
            yaxis=dict(
                title_font=dict(size=14),
                tickfont=dict(size=12),
                gridcolor=FINCRA_COLORS["light_green"],
                tickformat="$,.0f"  # Format y-axis values as currency
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # Section title with better styling
        st.markdown(f"""
        <h3 style='color: {FINCRA_COLORS["blue"]}; margin-bottom: 1rem;'>Geographic Distribution</h3>
        <p>Financial activity across markets</p>
        """, unsafe_allow_html=True)
        
        # Group by country
        country_data = latest_data.groupby('Country')[['Exposure', 'Inflow', 'Outflow']].sum().reset_index()
        country_data['Net_Position'] = country_data['Inflow'] - country_data['Outflow']
        
        # Create enhanced choropleth map
        fig = px.choropleth(
            country_data,
            locations='Country',
            locationmode='country names',
            color='Exposure',
            hover_name='Country',
            hover_data={
                'Exposure': ':$,.0f',
                'Inflow': ':$,.0f',
                'Outflow': ':$,.0f',
                'Net_Position': ':$,.0f'
            },
            title='FX Exposure by Country',
            color_continuous_scale='Greens',  # Green color palette to match Fincra
            height=450,
            projection='natural earth'  # More natural looking map
        )
        
        # Improve map styling
        fig.update_layout(
            title_font=dict(size=18, color=FINCRA_COLORS["blue"]),
            title_x=0.5,  # Center the title
            plot_bgcolor=FINCRA_COLORS["white"],
            paper_bgcolor=FINCRA_COLORS["white"],
            margin=dict(l=0, r=0, t=50, b=0),
            coloraxis_colorbar=dict(
                title="Exposure (USD)",
                tickformat="$,.0f"
            )
        )
        
        # Add enhanced hover template
        fig.update_traces(
            hovertemplate='<b>%{hovertext}</b><br>Exposure: %{customdata[0]}<br>Inflow: %{customdata[1]}<br>Outflow: %{customdata[2]}<br>Net Position: %{customdata[3]}'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Country comparison with enhanced visualization
        st.markdown(f"""
        <h3 style='color: {FINCRA_COLORS["blue"]}; margin-top: 1.5rem; margin-bottom: 1rem;'>Country Financial Summary</h3>
        """, unsafe_allow_html=True)
        
        # Create two columns for different views
        country_col1, country_col2 = st.columns([1, 1])
        
        with country_col1:
            # Enhanced bar chart for country comparison
            fig = px.bar(
                country_data.sort_values('Exposure', ascending=True),
                y='Country',
                x='Exposure',
                orientation='h',
                title='FX Exposure by Country',
                color='Exposure',
                color_continuous_scale='Greens',
                height=400,
                text_auto='.2s'  # Add text labels
            )
            
            # Improve styling
            fig.update_layout(
                title_font=dict(size=16, color=FINCRA_COLORS["blue"]),
                title_x=0.5,
                plot_bgcolor=FINCRA_COLORS["white"],
                paper_bgcolor=FINCRA_COLORS["white"],
                xaxis=dict(
                    title='Exposure (USD)',
                    title_font=dict(size=14),
                    tickfont=dict(size=12),
                    gridcolor=FINCRA_COLORS["light_green"],
                    tickformat="$,.0f"
                ),
                yaxis=dict(
                    title='',
                    title_font=dict(size=14),
                    tickfont=dict(size=12)
                ),
                coloraxis_showscale=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        with country_col2:
            # Add net position by country
            fig = px.bar(
                country_data.sort_values('Net_Position'),
                y='Country',
                x='Net_Position',
                orientation='h',
                title='Net Position by Country',
                color='Net_Position',
                color_continuous_scale='RdYlGn',  # Red for negative, green for positive
                height=400,
                text_auto='.2s'  # Add text labels
            )
            
            # Improve styling
            fig.update_layout(
                title_font=dict(size=16, color=FINCRA_COLORS["blue"]),
                title_x=0.5,
                plot_bgcolor=FINCRA_COLORS["white"],
                paper_bgcolor=FINCRA_COLORS["white"],
                xaxis=dict(
                    title='Net Position (USD)',
                    title_font=dict(size=14),
                    tickfont=dict(size=12),
                    gridcolor=FINCRA_COLORS["light_green"],
                    tickformat="$,.0f"
                ),
                yaxis=dict(
                    title='',
                    title_font=dict(size=14),
                    tickfont=dict(size=12)
                ),
                coloraxis_showscale=False
            )
            
            # Add a vertical line at x=0 to highlight positive vs negative
            fig.add_vline(x=0, line_width=1, line_dash="dash", line_color="gray")
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Interactive data table with improved styling
        st.markdown(f"""
        <h4 style='color: {FINCRA_COLORS["blue"]}; margin-top: 1rem; margin-bottom: 1rem;'>Detailed Country Data</h4>
        """, unsafe_allow_html=True)
        
        # Add a new calculated column for percentage of total exposure
        country_data['Percentage_of_Total'] = (country_data['Exposure'] / country_data['Exposure'].sum()) * 100
        
        # Reformat the dataframe for better display
        country_display = country_data.copy()
        country_display['Exposure'] = country_display['Exposure'].map('${:,.0f}'.format)
        country_display['Inflow'] = country_display['Inflow'].map('${:,.0f}'.format)
        country_display['Outflow'] = country_display['Outflow'].map('${:,.0f}'.format)
        country_display['Net_Position'] = country_display['Net_Position'].map('${:,.0f}'.format)
        country_display['Percentage_of_Total'] = country_display['Percentage_of_Total'].map('{:.1f}%'.format)
        
        # Rename columns for better display
        country_display.rename(columns={
            'Exposure': 'FX Exposure',
            'Inflow': 'Total Inflow',
            'Outflow': 'Total Outflow',
            'Net_Position': 'Net Position',
            'Percentage_of_Total': '% of Total Exposure'
        }, inplace=True)
        
        st.dataframe(
            country_display.sort_values('FX Exposure', ascending=False),
            hide_index=True,
            use_container_width=True
        )
