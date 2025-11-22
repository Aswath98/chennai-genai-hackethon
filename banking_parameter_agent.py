#!/usr/bin/env python3
"""
Intelligent Banking Parameter Agent
Real-time data aggregation for lending decision support
Monitors climate, economic, social, and regulatory factors affecting lending
"""

import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Banking Parameter Intelligence Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

class BankingParameterAgent:
    """Intelligent agent for real-time banking parameter monitoring"""
    
    def __init__(self):
        self.location = "Tamil Nadu, India"
        self.current_time = datetime.now()
        self.data_cache = {}
        
    def get_climate_data(self):
        """Get climate and weather data affecting agricultural lending"""
        
        # Simulated climate data (in real implementation, would use weather APIs)
        climate_data = {
            'current_weather': {
                'temperature': np.random.normal(28, 5),  # Celsius
                'humidity': np.random.normal(70, 15),     # Percentage
                'rainfall_last_30_days': np.random.normal(45, 20),  # mm
                'wind_speed': np.random.normal(12, 3),    # km/h
                'uv_index': np.random.randint(6, 11)
            },
            'climate_alerts': [
                {
                    'type': 'Drought Warning',
                    'severity': 'Medium',
                    'affected_districts': ['Salem', 'Dharmapuri', 'Krishnagiri'],
                    'impact': 'Agricultural loan defaults may increase by 15-20%',
                    'validity': '2024-12-15 to 2025-02-28'
                },
                {
                    'type': 'Monsoon Delay',
                    'severity': 'High',
                    'affected_districts': ['Thanjavur', 'Tiruvarur', 'Nagapattinam'],
                    'impact': 'Rice crop loans at risk, recommend insurance verification',
                    'validity': '2024-11-20 to 2025-01-31'
                },
                {
                    'type': 'Cyclone Watch',
                    'severity': 'Low',
                    'affected_districts': ['Chennai', 'Kanchipuram', 'Tiruvallur'],
                    'impact': 'Coastal business loans may need flexible repayment terms',
                    'validity': '2024-11-25 to 2024-12-05'
                }
            ],
            'seasonal_forecast': {
                'next_3_months': 'Below normal rainfall expected',
                'crop_outlook': 'Rabi season may be affected, Kharif recovery moderate',
                'risk_level': 'Medium-High'
            }
        }
        
        return climate_data
    
    def get_economic_indicators(self):
        """Get economic indicators affecting lending decisions"""
        
        economic_data = {
            'current_indicators': {
                'repo_rate': 6.50,  # RBI Repo Rate
                'inflation_rate': 5.85,  # CPI Inflation
                'unemployment_rate': 7.2,  # Unemployment %
                'gdp_growth': 6.3,  # GDP Growth %
                'rupee_usd': 83.25,  # INR/USD
                'sensex': 66750,  # Stock Market Index
                'nifty': 19950
            },
            'policy_updates': [
                {
                    'date': '2024-11-15',
                    'type': 'RBI Policy',
                    'description': 'Repo rate held steady at 6.50%',
                    'impact': 'Lending rates remain stable, good for borrowers'
                },
                {
                    'date': '2024-11-10',
                    'type': 'Government Scheme',
                    'description': 'PM Vishwakarma Scheme extended',
                    'impact': 'Enhanced collateral-free lending for artisans'
                },
                {
                    'date': '2024-11-01',
                    'type': 'Credit Policy',
                    'description': 'Priority Sector Lending targets revised',
                    'impact': 'Increased focus on agricultural and MSME lending'
                }
            ],
            'market_sentiment': {
                'overall': 'Cautiously Optimistic',
                'banking_sector': 'Stable',
                'agriculture': 'Moderate Risk',
                'msme': 'Growing',
                'consumer_spending': 'Steady'
            }
        }
        
        return economic_data
    
    def get_regulatory_updates(self):
        """Get regulatory and compliance updates"""
        
        regulatory_data = {
            'recent_regulations': [
                {
                    'date': '2024-11-18',
                    'regulator': 'RBI',
                    'title': 'Digital Lending Guidelines Update',
                    'impact': 'Enhanced due diligence required for digital loans',
                    'compliance_date': '2024-12-31',
                    'risk_level': 'Medium'
                },
                {
                    'date': '2024-11-12',
                    'regulator': 'SEBI',
                    'title': 'Credit Rating Disclosure Norms',
                    'impact': 'More transparent credit risk assessment',
                    'compliance_date': '2025-01-15',
                    'risk_level': 'Low'
                },
                {
                    'date': '2024-11-05',
                    'regulator': 'NABARD',
                    'title': 'Rural Credit Flow Guidelines',
                    'impact': 'Modified targets for agricultural lending',
                    'compliance_date': '2024-11-30',
                    'risk_level': 'Low'
                }
            ],
            'compliance_alerts': [
                'KYC norms update effective December 2024',
                'Enhanced risk assessment for climate-sensitive sectors',
                'Digital signature requirements for loan documents',
                'Mandatory crop insurance verification for agri-loans'
            ]
        }
        
        return regulatory_data
    
    def get_social_economic_factors(self):
        """Get social and economic factors affecting lending"""
        
        social_data = {
            'demographic_trends': {
                'rural_urban_migration': 'Increasing (+12% YoY)',
                'digital_adoption': 'High (+35% mobile banking users)',
                'financial_literacy': 'Improving (+8% in rural areas)',
                'employment_patterns': 'Gig economy growth (+25%)'
            },
            'current_events': [
                {
                    'type': 'Festival Season',
                    'event': 'Diwali & Harvest Festivals',
                    'impact': 'Increased consumer spending and loan demand',
                    'timeline': 'October 2024 - January 2025',
                    'recommendation': 'Higher approval rates for consumer goods loans'
                },
                {
                    'type': 'Agricultural Season',
                    'event': 'Rabi Season Preparation',
                    'impact': 'Farmer loan applications peak',
                    'timeline': 'November 2024 - February 2025',
                    'recommendation': 'Enhanced crop loan processing'
                },
                {
                    'type': 'Economic Activity',
                    'event': 'Post-monsoon Recovery',
                    'impact': 'Rural economy stabilizing',
                    'timeline': 'September 2024 - March 2025',
                    'recommendation': 'Monitor rural loan performance closely'
                }
            ],
            'regional_factors': {
                'chennai': {'risk_level': 'Low', 'growth': 'High', 'key_factor': 'IT sector growth'},
                'coimbatore': {'risk_level': 'Medium', 'growth': 'Steady', 'key_factor': 'Textile industry'},
                'madurai': {'risk_level': 'Medium', 'growth': 'Moderate', 'key_factor': 'Agriculture dependent'},
                'salem': {'risk_level': 'High', 'growth': 'Low', 'key_factor': 'Drought conditions'},
                'tiruchirappalli': {'risk_level': 'Medium', 'growth': 'Moderate', 'key_factor': 'Mixed economy'}
            }
        }
        
        return social_data
    
    def get_technology_trends(self):
        """Get technology trends affecting banking"""
        
        tech_data = {
            'digital_trends': {
                'upi_transactions': '+28% YoY',
                'mobile_banking': '+35% new users',
                'fintech_adoption': 'High in urban, growing in rural',
                'ai_ml_usage': 'Increasing for credit scoring',
                'blockchain_readiness': 'Early adoption phase'
            },
            'cybersecurity_alerts': [
                'Phishing attacks targeting banking apps (+15%)',
                'AI-powered fraud detection recommended',
                'Enhanced customer verification protocols needed',
                'Regular security awareness training advised'
            ],
            'innovation_opportunities': [
                'Voice-based loan applications in regional languages',
                'Satellite data for crop assessment',
                'IoT-based asset monitoring for collateral',
                'Blockchain for transparent credit history'
            ]
        }
        
        return tech_data
    
    def calculate_lending_risk_score(self, climate_data, economic_data, social_data):
        """Calculate overall lending environment risk score"""
        
        # Climate risk component (0-30 points)
        climate_score = 0
        for alert in climate_data['climate_alerts']:
            if alert['severity'] == 'High':
                climate_score += 10
            elif alert['severity'] == 'Medium':
                climate_score += 5
            elif alert['severity'] == 'Low':
                climate_score += 2
        
        climate_risk = min(climate_score, 30)
        
        # Economic risk component (0-25 points)
        inflation = economic_data['current_indicators']['inflation_rate']
        unemployment = economic_data['current_indicators']['unemployment_rate']
        economic_risk = min((inflation - 4) * 2 + (unemployment - 5) * 1.5, 25)
        economic_risk = max(0, economic_risk)
        
        # Regional risk component (0-20 points)
        high_risk_regions = sum([1 for region, data in social_data['regional_factors'].items() 
                                if data['risk_level'] == 'High'])
        regional_risk = high_risk_regions * 5
        
        # Social risk component (0-15 points)
        social_risk = 5  # Base social risk
        
        # Technology risk component (0-10 points)
        tech_risk = 3  # Base technology risk
        
        total_risk = climate_risk + economic_risk + regional_risk + social_risk + tech_risk
        
        # Convert to 0-100 scale
        risk_score = min(total_risk, 100)
        
        return {
            'overall_risk_score': risk_score,
            'risk_level': 'Low' if risk_score < 30 else 'Medium' if risk_score < 60 else 'High',
            'components': {
                'climate_risk': climate_risk,
                'economic_risk': economic_risk,
                'regional_risk': regional_risk,
                'social_risk': social_risk,
                'technology_risk': tech_risk
            }
        }
    
    def generate_recommendations(self, all_data, risk_assessment):
        """Generate intelligent recommendations for lending decisions"""
        
        recommendations = {
            'immediate_actions': [],
            'policy_adjustments': [],
            'risk_mitigation': [],
            'opportunities': []
        }
        
        # Climate-based recommendations
        for alert in all_data['climate']['climate_alerts']:
            if alert['severity'] in ['High', 'Medium']:
                recommendations['immediate_actions'].append(
                    f"Monitor {alert['type']} in {', '.join(alert['affected_districts'])} - {alert['impact']}"
                )
        
        # Economic recommendations
        economic = all_data['economic']
        if economic['current_indicators']['inflation_rate'] > 6:
            recommendations['policy_adjustments'].append(
                "Consider increasing interest rates for new loans due to high inflation"
            )
        
        if economic['current_indicators']['unemployment_rate'] > 7:
            recommendations['risk_mitigation'].append(
                "Enhanced income verification required due to elevated unemployment"
            )
        
        # Regional recommendations
        for region, data in all_data['social']['regional_factors'].items():
            if data['risk_level'] == 'High':
                recommendations['risk_mitigation'].append(
                    f"Implement stricter lending criteria for {region.title()} region due to {data['key_factor']}"
                )
            elif data['growth'] == 'High':
                recommendations['opportunities'].append(
                    f"Accelerate lending in {region.title()} due to high growth potential"
                )
        
        # Technology opportunities
        recommendations['opportunities'].extend([
            "Implement AI-powered credit scoring for better risk assessment",
            "Introduce voice-based loan applications for rural customers",
            "Use satellite data for agricultural loan assessments"
        ])
        
        return recommendations

def render_header():
    """Render the main header"""
    
    st.markdown("""
    <div style="background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 1.5rem; border-radius: 10px; text-align: center; margin-bottom: 2rem;">
        <h1>🤖 Banking Parameter Intelligence Agent</h1>
        <p><strong>Real-time Environmental Intelligence for Lending Decisions</strong></p>
        <p>Climate • Economy • Regulations • Social Trends • Technology</p>
    </div>
    """, unsafe_allow_html=True)

def render_dashboard():
    """Main dashboard rendering function"""
    
    render_header()
    
    # Initialize agent
    agent = BankingParameterAgent()
    
    # Sidebar controls
    st.sidebar.title("🎛️ Agent Controls")
    st.sidebar.markdown("---")
    
    # Location selector
    location = st.sidebar.selectbox(
        "Select Region:",
        ["Tamil Nadu", "Karnataka", "Andhra Pradesh", "Kerala", "Telangana"]
    )
    
    # Update frequency
    update_freq = st.sidebar.selectbox(
        "Update Frequency:",
        ["Real-time", "Hourly", "Daily", "Weekly"]
    )
    
    # Data refresh button
    if st.sidebar.button("🔄 Refresh All Data"):
        st.experimental_rerun()
    
    # Get all data
    climate_data = agent.get_climate_data()
    economic_data = agent.get_economic_indicators()
    regulatory_data = agent.get_regulatory_updates()
    social_data = agent.get_social_economic_factors()
    tech_data = agent.get_technology_trends()
    
    # Calculate risk assessment
    risk_assessment = agent.calculate_lending_risk_score(climate_data, economic_data, social_data)
    
    # Aggregate all data
    all_data = {
        'climate': climate_data,
        'economic': economic_data,
        'regulatory': regulatory_data,
        'social': social_data,
        'technology': tech_data
    }
    
    # Generate recommendations
    recommendations = agent.generate_recommendations(all_data, risk_assessment)
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🎯 Risk Dashboard",
        "🌤️ Climate Intelligence", 
        "📈 Economic Indicators",
        "📋 Regulatory Updates",
        "👥 Social Factors",
        "💡 Recommendations"
    ])
    
    with tab1:
        render_risk_dashboard(risk_assessment, all_data)
    
    with tab2:
        render_climate_intelligence(climate_data)
    
    with tab3:
        render_economic_indicators(economic_data)
    
    with tab4:
        render_regulatory_updates(regulatory_data)
    
    with tab5:
        render_social_factors(social_data, tech_data)
    
    with tab6:
        render_recommendations(recommendations, risk_assessment)

def render_risk_dashboard(risk_assessment, all_data):
    """Render the main risk dashboard"""
    
    st.header("🎯 Overall Lending Environment Assessment")
    
    # Main risk score display
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        score = risk_assessment['overall_risk_score']
        color = "#28a745" if score < 30 else "#ffc107" if score < 60 else "#dc3545"
        st.markdown(f"""
        <div style="background-color: {color}15; border: 2px solid {color}; border-radius: 10px; padding: 1rem; text-align: center;">
            <h2 style="color: {color}; margin: 0;">{score:.0f}/100</h2>
            <p style="margin: 0; font-weight: bold;">Overall Risk Score</p>
            <p style="margin: 0; font-size: 0.9em;">{risk_assessment['risk_level']} Risk</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        climate_alerts = len([a for a in all_data['climate']['climate_alerts'] if a['severity'] in ['High', 'Medium']])
        st.metric("Active Climate Alerts", climate_alerts, "🌧️")
    
    with col3:
        inflation = all_data['economic']['current_indicators']['inflation_rate']
        st.metric("Current Inflation", f"{inflation}%", "📈")
    
    with col4:
        high_risk_regions = len([r for r, d in all_data['social']['regional_factors'].items() if d['risk_level'] == 'High'])
        st.metric("High Risk Regions", high_risk_regions, "🗺️")
    
    # Risk component breakdown
    st.subheader("📊 Risk Component Analysis")
    
    components = risk_assessment['components']
    
    fig = go.Figure(data=go.Bar(
        x=list(components.keys()),
        y=list(components.values()),
        marker_color=['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57']
    ))
    
    fig.update_layout(
        title="Risk Components Breakdown",
        xaxis_title="Risk Categories",
        yaxis_title="Risk Score (0-30 scale)",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Quick insights
    st.subheader("⚡ Quick Insights")
    
    insights = []
    
    if risk_assessment['overall_risk_score'] > 60:
        insights.append("🚨 **High Risk Environment**: Consider tightening lending criteria")
    elif risk_assessment['overall_risk_score'] < 30:
        insights.append("✅ **Favorable Conditions**: Good time for aggressive lending")
    else:
        insights.append("⚠️ **Moderate Risk**: Standard lending protocols recommended")
    
    # Climate insights
    severe_alerts = [a for a in all_data['climate']['climate_alerts'] if a['severity'] == 'High']
    if severe_alerts:
        insights.append(f"🌪️ **Climate Alert**: {len(severe_alerts)} severe weather warnings active")
    
    # Economic insights
    if all_data['economic']['current_indicators']['unemployment_rate'] > 7:
        insights.append("👥 **Employment Concern**: High unemployment may affect repayment capacity")
    
    for insight in insights:
        st.markdown(insight)

def render_climate_intelligence(climate_data):
    """Render climate intelligence tab"""
    
    st.header("🌤️ Climate Intelligence for Agricultural Lending")
    
    # Current weather
    st.subheader("🌡️ Current Weather Conditions")
    
    weather = climate_data['current_weather']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Temperature", f"{weather['temperature']:.1f}°C")
    with col2:
        st.metric("Humidity", f"{weather['humidity']:.0f}%")
    with col3:
        st.metric("Rainfall (30d)", f"{weather['rainfall_last_30_days']:.0f}mm")
    with col4:
        st.metric("UV Index", weather['uv_index'])
    
    # Climate alerts
    st.subheader("🚨 Active Climate Alerts")
    
    for alert in climate_data['climate_alerts']:
        severity_color = {"High": "#dc3545", "Medium": "#ffc107", "Low": "#28a745"}
        color = severity_color.get(alert['severity'], "#6c757d")
        
        st.markdown(f"""
        <div style="border-left: 4px solid {color}; background-color: {color}15; padding: 1rem; margin: 0.5rem 0; border-radius: 5px;">
            <h4 style="color: {color}; margin: 0;">{alert['type']} - {alert['severity']} Severity</h4>
            <p><strong>Affected Areas:</strong> {', '.join(alert['affected_districts'])}</p>
            <p><strong>Impact:</strong> {alert['impact']}</p>
            <p><strong>Validity:</strong> {alert['validity']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Seasonal forecast
    st.subheader("📅 Seasonal Forecast & Recommendations")
    
    forecast = climate_data['seasonal_forecast']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **3-Month Outlook:** {forecast['next_3_months']}
        
        **Crop Assessment:** {forecast['crop_outlook']}
        
        **Risk Level:** {forecast['risk_level']}
        """)
    
    with col2:
        st.warning("""
        **Lending Recommendations:**
        
        • Verify crop insurance for all agricultural loans
        • Consider weather-indexed insurance products
        • Implement flexible repayment schedules for affected regions
        • Enhanced monitoring for drought-prone areas
        """)

def render_economic_indicators(economic_data):
    """Render economic indicators tab"""
    
    st.header("📈 Economic Indicators Dashboard")
    
    # Key indicators
    indicators = economic_data['current_indicators']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Repo Rate", f"{indicators['repo_rate']:.2f}%")
        st.metric("Inflation Rate", f"{indicators['inflation_rate']:.2f}%")
        st.metric("GDP Growth", f"{indicators['gdp_growth']:.1f}%")
    
    with col2:
        st.metric("Unemployment", f"{indicators['unemployment_rate']:.1f}%")
        st.metric("USD/INR", f"₹{indicators['rupee_usd']:.2f}")
        st.metric("Sensex", f"{indicators['sensex']:,}")
    
    with col3:
        # Market sentiment
        sentiment = economic_data['market_sentiment']
        st.write("**Market Sentiment:**")
        for sector, sent in sentiment.items():
            emoji = "🟢" if "positive" in sent.lower() or "growing" in sent.lower() or "stable" in sent.lower() else "🟡" if "moderate" in sent.lower() or "steady" in sent.lower() else "🔴"
            st.write(f"{emoji} {sector.replace('_', ' ').title()}: {sent}")
    
    # Recent policy updates
    st.subheader("📋 Recent Policy Updates")
    
    for update in economic_data['policy_updates']:
        st.markdown(f"""
        **{update['date']} - {update['type']}**
        
        {update['description']}
        
        *Impact:* {update['impact']}
        
        ---
        """)
    
    # Economic trend visualization
    st.subheader("📊 Economic Trends")
    
    # Simulate trend data
    dates = pd.date_range(start='2024-01-01', end='2024-11-22', freq='M')
    repo_rates = np.random.normal(6.5, 0.2, len(dates))
    inflation = np.random.normal(5.8, 0.5, len(dates))
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(x=dates, y=repo_rates, name="Repo Rate", line=dict(color="#1f77b4")),
        secondary_y=False,
    )
    
    fig.add_trace(
        go.Scatter(x=dates, y=inflation, name="Inflation Rate", line=dict(color="#ff7f0e")),
        secondary_y=True,
    )
    
    fig.update_layout(title="Economic Indicators Trend")
    fig.update_yaxes(title_text="Repo Rate (%)", secondary_y=False)
    fig.update_yaxes(title_text="Inflation Rate (%)", secondary_y=True)
    
    st.plotly_chart(fig, use_container_width=True)

def render_regulatory_updates(regulatory_data):
    """Render regulatory updates tab"""
    
    st.header("📋 Regulatory Intelligence")
    
    # Recent regulations
    st.subheader("📜 Recent Regulatory Updates")
    
    for reg in regulatory_data['recent_regulations']:
        risk_color = {"High": "#dc3545", "Medium": "#ffc107", "Low": "#28a745"}
        color = risk_color.get(reg['risk_level'], "#6c757d")
        
        st.markdown(f"""
        <div style="border: 1px solid {color}; border-radius: 8px; padding: 1rem; margin: 1rem 0;">
            <h4 style="color: {color}; margin-top: 0;">{reg['title']}</h4>
            <p><strong>Regulator:</strong> {reg['regulator']} | <strong>Date:</strong> {reg['date']}</p>
            <p><strong>Impact:</strong> {reg['impact']}</p>
            <p><strong>Compliance Required By:</strong> {reg['compliance_date']}</p>
            <span style="background-color: {color}; color: white; padding: 0.2rem 0.5rem; border-radius: 3px; font-size: 0.8rem;">
                {reg['risk_level']} Risk
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    # Compliance alerts
    st.subheader("⚠️ Compliance Alerts")
    
    for alert in regulatory_data['compliance_alerts']:
        st.warning(f"• {alert}")

def render_social_factors(social_data, tech_data):
    """Render social and technology factors"""
    
    st.header("👥 Social & Technology Intelligence")
    
    # Demographic trends
    st.subheader("📊 Demographic Trends")
    
    trends = social_data['demographic_trends']
    
    col1, col2 = st.columns(2)
    
    with col1:
        for key, value in trends.items():
            trend_emoji = "📈" if "increasing" in value.lower() or "high" in value.lower() or "improving" in value.lower() or "growth" in value.lower() else "📊"
            st.write(f"{trend_emoji} **{key.replace('_', ' ').title()}:** {value}")
    
    with col2:
        st.subheader("💻 Technology Trends")
        tech_trends = tech_data['digital_trends']
        for key, value in tech_trends.items():
            st.write(f"🔧 **{key.replace('_', ' ').title()}:** {value}")
    
    # Current events
    st.subheader("📅 Current Events Impact")
    
    for event in social_data['current_events']:
        st.markdown(f"""
        **{event['event']} ({event['type']})**
        
        *Timeline:* {event['timeline']}
        
        *Impact:* {event['impact']}
        
        *Recommendation:* {event['recommendation']}
        
        ---
        """)
    
    # Regional analysis
    st.subheader("🗺️ Regional Risk Analysis")
    
    regions_df = pd.DataFrame(social_data['regional_factors']).T.reset_index()
    regions_df.columns = ['Region', 'Risk Level', 'Growth', 'Key Factor']
    
    # Color code by risk level
    def color_risk(val):
        colors = {'Low': '#d4edda', 'Medium': '#fff3cd', 'High': '#f8d7da'}
        return f'background-color: {colors.get(val, "#ffffff")}'
    
    styled_df = regions_df.style.applymap(color_risk, subset=['Risk Level'])
    st.dataframe(styled_df, use_container_width=True)

def render_recommendations(recommendations, risk_assessment):
    """Render intelligent recommendations"""
    
    st.header("💡 Intelligent Recommendations")
    
    # Overall recommendation based on risk score
    risk_score = risk_assessment['overall_risk_score']
    
    if risk_score < 30:
        st.success(f"""
        ## 🟢 Favorable Lending Environment (Risk Score: {risk_score:.0f}/100)
        
        **Recommended Strategy:** Aggressive lending with standard terms
        
        **Key Actions:**
        - Increase loan approval rates
        - Consider competitive interest rates
        - Expand portfolio in growth sectors
        """)
    elif risk_score < 60:
        st.warning(f"""
        ## 🟡 Moderate Risk Environment (Risk Score: {risk_score:.0f}/100)
        
        **Recommended Strategy:** Balanced approach with enhanced monitoring
        
        **Key Actions:**
        - Maintain standard lending criteria
        - Increase frequency of portfolio reviews
        - Focus on secured lending
        """)
    else:
        st.error(f"""
        ## 🔴 High Risk Environment (Risk Score: {risk_score:.0f}/100)
        
        **Recommended Strategy:** Conservative lending with strict criteria
        
        **Key Actions:**
        - Tighten approval criteria
        - Increase collateral requirements
        - Enhanced due diligence processes
        """)
    
    # Specific recommendations by category
    categories = [
        ("🚨 Immediate Actions", recommendations['immediate_actions']),
        ("📋 Policy Adjustments", recommendations['policy_adjustments']),
        ("🛡️ Risk Mitigation", recommendations['risk_mitigation']),
        ("🎯 Opportunities", recommendations['opportunities'])
    ]
    
    for title, items in categories:
        if items:
            st.subheader(title)
            for item in items:
                st.write(f"• {item}")
    
    # Action plan
    st.subheader("📋 30-Day Action Plan")
    
    action_plan = [
        "**Week 1:** Implement immediate risk mitigation measures",
        "**Week 2:** Adjust lending policies based on current environment",
        "**Week 3:** Enhanced monitoring of high-risk portfolios",
        "**Week 4:** Review and optimize lending processes"
    ]
    
    for action in action_plan:
        st.write(action)

def main():
    """Main application entry point"""
    render_dashboard()

if __name__ == "__main__":
    main()
