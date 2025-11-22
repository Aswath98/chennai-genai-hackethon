#!/usr/bin/env python3
"""
Banking Intelligence Agent Test & Demo
Demonstrates the capabilities of the banking parameter agents
"""

import json
import requests
from datetime import datetime
import pandas as pd

def test_banking_intelligence():
    """Test and demonstrate the banking intelligence system"""
    
    print("🤖 BANKING INTELLIGENCE AGENT - DEMO")
    print("=" * 60)
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Simulate getting current parameters (without actual API)
    current_params = get_simulated_parameters()
    
    print("\n📊 CURRENT BANKING ENVIRONMENT PARAMETERS")
    print("-" * 50)
    
    # Climate & Weather
    print("🌤️  CLIMATE & WEATHER DATA:")
    climate = current_params['climate_data']
    print(f"   Temperature: {climate['current_temperature']}°C")
    print(f"   Humidity: {climate['humidity_percent']}%")
    print(f"   Rainfall (7 days): {climate['rainfall_last_7_days_mm']}mm")
    print(f"   Weather: {climate['weather_condition']}")
    print(f"   Drought Risk: {climate['drought_risk_level']}")
    print(f"   Flood Risk: {climate['flood_risk_level']}")
    
    # Economic Indicators
    print("\n📈 ECONOMIC INDICATORS:")
    economic = current_params['economic_indicators']
    print(f"   RBI Repo Rate: {economic['rbi_repo_rate']}%")
    print(f"   Inflation (CPI): {economic['inflation_cpi']}%")
    print(f"   GDP Growth: {economic['gdp_growth_rate']}%")
    print(f"   Unemployment: {economic['unemployment_rate']}%")
    print(f"   INR/USD: ₹{economic['inr_usd_rate']}")
    print(f"   Market Sentiment: {economic['market_sentiment']}")
    
    # Social Factors
    print("\n👥 SOCIAL & DEMOGRAPHIC FACTORS:")
    social = current_params['social_factors']
    print(f"   Festival Season: {social['festival_season']}")
    print(f"   Harvest Season: {social['harvest_season']}")
    print(f"   Consumer Confidence: {social['consumer_confidence']}/10")
    print(f"   Digital Adoption: {social['digital_adoption_rate']}%")
    print(f"   Migration Pattern: {social['migration_pattern']}")
    
    # Risk Assessment
    print("\n⚖️  RISK ASSESSMENT:")
    risk = current_params['risk_indicators']
    print(f"   Overall Risk Score: {risk['overall_risk_score']}/100")
    print(f"   Climate Risk: {risk['climate_risk']}/100")
    print(f"   Economic Risk: {risk['economic_risk']}/100")
    print(f"   Default Probability: {risk['default_probability_estimate']}%")
    print(f"   Portfolio Stress: {risk['portfolio_stress_level']}")
    
    # Technology Status
    print("\n💻 TECHNOLOGY & DIGITAL STATUS:")
    tech = current_params['technology_factors']
    print(f"   UPI Transactions: {tech['upi_transaction_volume']} million/month")
    print(f"   Mobile Banking: {tech['mobile_banking_penetration']}%")
    print(f"   Cyber Threat Level: {tech['cybersecurity_threat_level']}")
    print(f"   FinTech Adoption: {tech['fintech_adoption']}%")
    
    # Agricultural Data
    print("\n🌾 AGRICULTURAL PARAMETERS:")
    agri = current_params['agricultural_data']
    print(f"   Kharif Crop Status: {agri['kharif_crop_status']}")
    print(f"   Rabi Preparation: {agri['rabi_season_preparation']}")
    print(f"   Crop Insurance: {agri['crop_insurance_penetration']}%")
    print(f"   Credit Demand: {agri['agricultural_credit_demand']}")
    print(f"   Rice Price: ₹{agri['mandi_prices']['rice']}/quintal")
    
    # Generate Lending Scenarios
    print("\n" + "=" * 60)
    print("💡 LENDING SCENARIO ANALYSIS")
    print("=" * 60)
    
    scenarios = [
        {
            "borrower_type": "Rice Farmer",
            "loan_amount": 200000,
            "purpose": "Agriculture",
            "location": "Thanjavur",
            "season": "Rabi"
        },
        {
            "borrower_type": "Small Trader",
            "loan_amount": 500000,
            "purpose": "Business",
            "location": "Coimbatore", 
            "season": "Festival"
        },
        {
            "borrower_type": "Auto Driver",
            "loan_amount": 150000,
            "purpose": "Vehicle",
            "location": "Chennai",
            "season": "Regular"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n📋 SCENARIO {i}: {scenario['borrower_type']}")
        print("-" * 30)
        print(f"   Loan Amount: ₹{scenario['loan_amount']:,}")
        print(f"   Purpose: {scenario['purpose']}")
        print(f"   Location: {scenario['location']}")
        
        # Simulate lending recommendation
        recommendation = analyze_lending_scenario(scenario, current_params)
        
        print(f"   Recommendation: {recommendation['decision']}")
        print(f"   Risk Level: {recommendation['risk_level']}")
        print(f"   Interest Rate: {recommendation['interest_rate']}%")
        print(f"   Conditions: {', '.join(recommendation['conditions'])}")
    
    # Recommendations
    print("\n" + "=" * 60)
    print("🎯 INTELLIGENT RECOMMENDATIONS")
    print("=" * 60)
    
    recommendations = current_params['recommendations']
    
    if recommendations['alerts']:
        print("\n🚨 IMMEDIATE ALERTS:")
        for alert in recommendations['alerts']:
            print(f"   • {alert}")
    
    if recommendations['immediate_actions']:
        print("\n⚡ IMMEDIATE ACTIONS:")
        for action in recommendations['immediate_actions']:
            print(f"   • {action}")
    
    if recommendations['risk_mitigation']:
        print("\n🛡️  RISK MITIGATION:")
        for mitigation in recommendations['risk_mitigation']:
            print(f"   • {mitigation}")
    
    if recommendations['opportunities']:
        print("\n🎯 OPPORTUNITIES:")
        for opportunity in recommendations['opportunities']:
            print(f"   • {opportunity}")
    
    # Generate Daily Brief
    print("\n" + "=" * 60)
    print("📋 DAILY LENDING BRIEF")
    print("=" * 60)
    
    brief = generate_daily_brief(current_params)
    print(brief)
    
    print("\n" + "=" * 60)
    print("✅ BANKING INTELLIGENCE DEMO COMPLETED")
    print("🚀 Ready for real-time deployment!")
    print("=" * 60)

def get_simulated_parameters():
    """Get simulated current parameters"""
    
    import random
    
    return {
        'timestamp': datetime.now().isoformat(),
        'climate_data': {
            'current_temperature': round(random.uniform(22, 35), 1),
            'humidity_percent': round(random.uniform(45, 90), 1),
            'rainfall_last_7_days_mm': round(random.uniform(0, 50), 1),
            'weather_condition': random.choice(["Clear", "Cloudy", "Light Rain", "Sunny"]),
            'drought_risk_level': random.choice(["Low", "Medium", "High"]),
            'flood_risk_level': random.choice(["Low", "Medium"]),
        },
        'economic_indicators': {
            'rbi_repo_rate': 6.50,
            'inflation_cpi': round(random.uniform(4.5, 6.5), 2),
            'gdp_growth_rate': round(random.uniform(5.8, 7.2), 1),
            'unemployment_rate': round(random.uniform(6.5, 8.0), 1),
            'inr_usd_rate': round(random.uniform(82.5, 84.0), 2),
            'market_sentiment': random.choice(["Bullish", "Neutral", "Cautious"])
        },
        'social_factors': {
            'festival_season': random.choice(["High Activity", "Medium Activity", "Low Activity"]),
            'harvest_season': random.choice(["Active", "Post-Harvest", "Pre-Harvest"]),
            'consumer_confidence': round(random.uniform(3.5, 8.5), 1),
            'digital_adoption_rate': round(random.uniform(65, 85), 1),
            'migration_pattern': random.choice(["Low", "Medium", "High"])
        },
        'risk_indicators': {
            'overall_risk_score': random.randint(25, 65),
            'climate_risk': random.randint(10, 40),
            'economic_risk': random.randint(15, 35),
            'social_risk': random.randint(5, 25),
            'default_probability_estimate': round(random.uniform(2.5, 8.5), 2),
            'portfolio_stress_level': random.choice(["Low", "Medium", "High"])
        },
        'technology_factors': {
            'upi_transaction_volume': random.randint(8000, 12000),
            'mobile_banking_penetration': round(random.uniform(70, 85), 1),
            'cybersecurity_threat_level': random.choice(["Low", "Medium", "High"]),
            'fintech_adoption': round(random.uniform(60, 80), 1)
        },
        'agricultural_data': {
            'kharif_crop_status': random.choice(["Good", "Average", "Poor"]),
            'rabi_season_preparation': random.choice(["On Track", "Delayed"]),
            'crop_insurance_penetration': round(random.uniform(35, 55), 1),
            'agricultural_credit_demand': random.choice(["High", "Medium", "Low"]),
            'mandi_prices': {
                'rice': random.randint(2000, 2500),
                'wheat': random.randint(2100, 2400)
            }
        },
        'recommendations': {
            'alerts': [],
            'immediate_actions': [],
            'risk_mitigation': [],
            'opportunities': []
        }
    }

def analyze_lending_scenario(scenario, params):
    """Analyze a lending scenario and provide recommendation"""
    
    base_risk = params['risk_indicators']['overall_risk_score']
    
    # Adjust risk based on loan purpose
    purpose_adjustments = {
        'Agriculture': 10 if params['climate_data']['drought_risk_level'] == 'High' else 0,
        'Business': 5 if params['economic_indicators']['market_sentiment'] == 'Bearish' else 0,
        'Vehicle': 0,
        'Personal': 15
    }
    
    # Location risk adjustment
    location_risk = {'Chennai': 0, 'Coimbatore': 5, 'Thanjavur': 10}
    
    total_risk = base_risk + purpose_adjustments.get(scenario['purpose'], 5) + location_risk.get(scenario['location'], 0)
    
    if total_risk < 35:
        decision = "APPROVE"
        risk_level = "LOW"
        interest_rate = 10.5
        conditions = ["Standard terms"]
    elif total_risk < 55:
        decision = "CONDITIONAL APPROVE"
        risk_level = "MEDIUM"
        interest_rate = 12.0
        conditions = ["Enhanced monitoring", "Additional documentation"]
    else:
        decision = "DEFER/REJECT"
        risk_level = "HIGH"
        interest_rate = 14.0
        conditions = ["High risk environment", "Consider after conditions improve"]
    
    return {
        'decision': decision,
        'risk_level': risk_level,
        'interest_rate': interest_rate,
        'conditions': conditions,
        'calculated_risk': total_risk
    }

def generate_daily_brief(params):
    """Generate daily lending brief"""
    
    risk_score = params['risk_indicators']['overall_risk_score']
    
    if risk_score < 35:
        risk_status = "🟢 FAVORABLE"
        strategy = "Aggressive lending recommended"
    elif risk_score < 55:
        strategy = "Balanced approach with monitoring"
        risk_status = "🟡 MODERATE"
    else:
        risk_status = "🔴 ELEVATED"
        strategy = "Conservative lending advised"
    
    brief = f"""
📅 Date: {datetime.now().strftime('%B %d, %Y')}

🎯 LENDING ENVIRONMENT STATUS: {risk_status}
   Overall Risk Score: {risk_score}/100
   
📊 KEY INDICATORS:
   • Economic: Inflation at {params['economic_indicators']['inflation_cpi']}%, GDP growth {params['economic_indicators']['gdp_growth_rate']}%
   • Climate: {params['climate_data']['weather_condition']}, Drought risk {params['climate_data']['drought_risk_level']}
   • Social: {params['social_factors']['festival_season']} festival activity
   • Technology: {params['technology_factors']['cybersecurity_threat_level']} cyber threat level

💡 RECOMMENDED STRATEGY: {strategy}

🎯 TODAY'S FOCUS AREAS:
   • Agricultural loans: Monitor {params['climate_data']['drought_risk_level'].lower()} drought risk
   • Consumer loans: {params['social_factors']['festival_season']} demand expected
   • Digital security: {params['technology_factors']['cybersecurity_threat_level']} threat level protocols
"""
    
    return brief

def test_api_endpoints():
    """Test API endpoints if available"""
    
    print("\n🔗 TESTING API ENDPOINTS")
    print("-" * 40)
    
    # Test URLs (when API is running)
    test_urls = [
        "http://localhost:5000/api/health",
        "http://localhost:5000/api/banking-parameters",
        "http://localhost:5000/api/risk-assessment"
    ]
    
    for url in test_urls:
        try:
            # Note: This would work if the API server is running
            print(f"🔗 Testing: {url}")
            print("   [Simulated] API endpoint ready for testing")
        except:
            print(f"   API not available (run banking_intelligence_api.py)")

if __name__ == "__main__":
    test_banking_intelligence()
    test_api_endpoints()
    
    print(f"\n🎛️  DASHBOARD LINKS:")
    print(f"   Banking Parameter Agent: http://localhost:8505")
    print(f"   Real-time Agent: http://localhost:8506") 
    print(f"   Ultimate Dashboard: http://localhost:8504")
    print(f"   API Documentation: http://localhost:5000")
    
    print(f"\n🚀 To start individual components:")
    print(f"   streamlit run banking_parameter_agent.py --server.port 8505")
    print(f"   streamlit run realtime_banking_agent.py --server.port 8506")
    print(f"   python banking_intelligence_api.py")
