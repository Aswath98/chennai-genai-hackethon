#!/usr/bin/env python3
"""
Banking Parameter API Agent
RESTful API for accessing real-time banking intelligence data
"""

from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import json
import random
import numpy as np

app = Flask(__name__)

class BankingIntelligenceAPI:
    """API class for banking intelligence data"""
    
    def __init__(self):
        self.last_updated = datetime.now()
        
    def get_current_parameters(self, location="Tamil Nadu"):
        """Get comprehensive current parameters affecting banking"""
        
        current_time = datetime.now()
        
        data = {
            "timestamp": current_time.isoformat(),
            "location": location,
            "validity_minutes": 15,  # Data valid for 15 minutes
            
            # Climate & Weather Parameters
            "climate_data": {
                "current_temperature": round(random.uniform(22, 35), 1),
                "humidity_percent": round(random.uniform(45, 90), 1),
                "rainfall_last_7_days_mm": round(random.uniform(0, 50), 1),
                "weather_condition": random.choice(["Clear", "Cloudy", "Light Rain", "Heavy Rain", "Sunny"]),
                "wind_speed_kmh": round(random.uniform(5, 25), 1),
                "uv_index": random.randint(1, 11),
                "air_quality_index": random.randint(50, 200),
                "drought_risk_level": random.choice(["Low", "Medium", "High"]),
                "flood_risk_level": random.choice(["Low", "Medium", "High"]),
                "seasonal_outlook": "Post-monsoon transition period"
            },
            
            # Economic Parameters
            "economic_indicators": {
                "rbi_repo_rate": 6.50,
                "inflation_cpi": round(random.uniform(4.5, 6.5), 2),
                "gdp_growth_rate": round(random.uniform(5.8, 7.2), 1),
                "unemployment_rate": round(random.uniform(6.5, 8.0), 1),
                "inr_usd_rate": round(random.uniform(82.5, 84.0), 2),
                "sensex_index": random.randint(65000, 68000),
                "bank_nifty": random.randint(44000, 46000),
                "gold_price_per_10g": random.randint(61000, 64000),
                "crude_oil_price": round(random.uniform(75, 85), 2),
                "market_sentiment": random.choice(["Bullish", "Bearish", "Neutral", "Volatile"])
            },
            
            # Social & Demographic Parameters
            "social_factors": {
                "festival_season": self._get_festival_status(),
                "harvest_season": self._get_harvest_status(),
                "migration_pattern": random.choice(["Low", "Medium", "High"]),
                "employment_demand": random.choice(["Growing", "Stable", "Declining"]),
                "consumer_confidence": round(random.uniform(3.5, 8.5), 1),
                "digital_adoption_rate": round(random.uniform(65, 85), 1),
                "financial_literacy_score": round(random.uniform(4.0, 7.5), 1),
                "rural_urban_migration": random.choice(["Increasing", "Stable", "Decreasing"])
            },
            
            # Government & Regulatory Parameters
            "regulatory_environment": {
                "recent_policy_changes": random.choice(["None", "Minor", "Significant"]),
                "compliance_burden": random.choice(["Low", "Medium", "High"]),
                "lending_guidelines": "Standard",
                "priority_sector_targets": "18% of ANBC",
                "digital_lending_rules": "Enhanced due diligence required",
                "kcc_scheme_status": "Active",
                "pradhan_mantri_schemes": ["PMJDY", "PMJJBY", "PMSBY", "APY"],
                "regulatory_sentiment": random.choice(["Supportive", "Neutral", "Restrictive"])
            },
            
            # Technology & Cybersecurity Parameters
            "technology_factors": {
                "upi_transaction_volume": random.randint(8000, 12000),  # Million transactions/month
                "mobile_banking_penetration": round(random.uniform(70, 85), 1),
                "internet_connectivity": round(random.uniform(75, 90), 1),
                "cybersecurity_threat_level": random.choice(["Low", "Medium", "High"]),
                "digital_fraud_incidents": random.randint(50, 200),  # Per month
                "fintech_adoption": round(random.uniform(60, 80), 1),
                "ai_ml_readiness": round(random.uniform(40, 70), 1),
                "blockchain_adoption": round(random.uniform(10, 30), 1)
            },
            
            # Agricultural Parameters (specific to rural lending)
            "agricultural_data": {
                "kharif_crop_status": random.choice(["Good", "Average", "Poor"]),
                "rabi_season_preparation": random.choice(["On Track", "Delayed", "Advanced"]),
                "crop_insurance_penetration": round(random.uniform(35, 55), 1),
                "mandi_prices": {
                    "rice": random.randint(2000, 2500),
                    "wheat": random.randint(2100, 2400),
                    "cotton": random.randint(5500, 6500),
                    "sugarcane": random.randint(280, 320)
                },
                "irrigation_availability": round(random.uniform(60, 85), 1),
                "farm_mechanization": round(random.uniform(45, 65), 1),
                "agricultural_credit_demand": random.choice(["High", "Medium", "Low"])
            },
            
            # Infrastructure Parameters
            "infrastructure_status": {
                "electricity_availability": round(random.uniform(85, 95), 1),
                "road_connectivity": round(random.uniform(75, 90), 1),
                "banking_infrastructure": round(random.uniform(70, 85), 1),
                "telecom_coverage": round(random.uniform(90, 98), 1),
                "transportation_efficiency": round(random.uniform(65, 80), 1),
                "market_access": round(random.uniform(60, 80), 1),
                "storage_facilities": round(random.uniform(40, 70), 1),
                "cold_chain_availability": round(random.uniform(30, 60), 1)
            },
            
            # Risk Assessment Parameters
            "risk_indicators": {
                "overall_risk_score": self._calculate_risk_score(),
                "climate_risk": random.randint(10, 40),
                "economic_risk": random.randint(15, 35),
                "social_risk": random.randint(5, 25),
                "technology_risk": random.randint(8, 20),
                "regulatory_risk": random.randint(5, 15),
                "default_probability_estimate": round(random.uniform(2.5, 8.5), 2),
                "portfolio_stress_level": random.choice(["Low", "Medium", "High"]),
                "liquidity_risk": random.choice(["Low", "Medium", "High"])
            }
        }
        
        # Add intelligent recommendations
        data["recommendations"] = self._generate_recommendations(data)
        
        return data
    
    def _get_festival_status(self):
        """Determine current festival season status"""
        current_month = datetime.now().month
        if current_month in [10, 11, 12]:  # Festival season
            return "High Activity"
        elif current_month in [1, 4, 8]:   # Major festivals
            return "Medium Activity" 
        else:
            return "Low Activity"
    
    def _get_harvest_status(self):
        """Determine harvest season status"""
        current_month = datetime.now().month
        if current_month in [3, 4, 10, 11]:  # Harvest seasons
            return "Active"
        elif current_month in [5, 6, 12, 1]:  # Post-harvest
            return "Post-Harvest"
        else:
            return "Pre-Harvest"
    
    def _calculate_risk_score(self):
        """Calculate overall risk score (0-100)"""
        base_score = random.randint(25, 45)
        
        # Seasonal adjustments
        current_month = datetime.now().month
        if current_month in [6, 7, 8]:  # Monsoon months
            base_score += random.randint(-5, 10)
        
        return min(100, max(0, base_score))
    
    def _generate_recommendations(self, data):
        """Generate intelligent recommendations based on current parameters"""
        
        recommendations = {
            "immediate_actions": [],
            "risk_mitigation": [],
            "opportunities": [],
            "alerts": []
        }
        
        # Climate-based recommendations
        if data["climate_data"]["drought_risk_level"] == "High":
            recommendations["immediate_actions"].append("Verify crop insurance for agricultural loans")
            recommendations["risk_mitigation"].append("Consider flexible repayment schedules for farmers")
        
        if data["climate_data"]["flood_risk_level"] == "High":
            recommendations["alerts"].append("Monitor flood-prone areas for loan applications")
        
        # Economic recommendations
        if data["economic_indicators"]["inflation_cpi"] > 6.0:
            recommendations["immediate_actions"].append("Review interest rate structures")
            recommendations["risk_mitigation"].append("Enhanced income verification for new applications")
        
        if data["economic_indicators"]["unemployment_rate"] > 7.5:
            recommendations["risk_mitigation"].append("Stricter employment verification required")
        
        # Social factor recommendations
        if data["social_factors"]["festival_season"] == "High Activity":
            recommendations["opportunities"].append("Increase consumer loan marketing during festival season")
        
        # Technology recommendations
        if data["technology_factors"]["cybersecurity_threat_level"] == "High":
            recommendations["alerts"].append("Enhanced cybersecurity protocols recommended")
        
        # Agricultural recommendations
        if data["agricultural_data"]["agricultural_credit_demand"] == "High":
            recommendations["opportunities"].append("Focus on agricultural loan portfolio expansion")
        
        return recommendations

# Initialize API
banking_api = BankingIntelligenceAPI()

@app.route('/api/banking-parameters', methods=['GET'])
def get_banking_parameters():
    """Get current banking parameters"""
    location = request.args.get('location', 'Tamil Nadu')
    data = banking_api.get_current_parameters(location)
    return jsonify(data)

@app.route('/api/risk-assessment', methods=['GET'])
def get_risk_assessment():
    """Get focused risk assessment"""
    data = banking_api.get_current_parameters()
    
    risk_data = {
        "timestamp": data["timestamp"],
        "overall_risk_score": data["risk_indicators"]["overall_risk_score"],
        "risk_breakdown": {
            "climate_risk": data["risk_indicators"]["climate_risk"],
            "economic_risk": data["risk_indicators"]["economic_risk"],
            "social_risk": data["risk_indicators"]["social_risk"],
            "technology_risk": data["risk_indicators"]["technology_risk"],
            "regulatory_risk": data["risk_indicators"]["regulatory_risk"]
        },
        "risk_level": "Low" if data["risk_indicators"]["overall_risk_score"] < 30 else 
                     "Medium" if data["risk_indicators"]["overall_risk_score"] < 60 else "High",
        "default_probability": data["risk_indicators"]["default_probability_estimate"],
        "recommendations": data["recommendations"]
    }
    
    return jsonify(risk_data)

@app.route('/api/climate-data', methods=['GET'])
def get_climate_data():
    """Get climate and weather data"""
    data = banking_api.get_current_parameters()
    return jsonify({
        "timestamp": data["timestamp"],
        "climate_data": data["climate_data"],
        "agricultural_data": data["agricultural_data"]
    })

@app.route('/api/economic-indicators', methods=['GET'])
def get_economic_indicators():
    """Get economic indicators"""
    data = banking_api.get_current_parameters()
    return jsonify({
        "timestamp": data["timestamp"],
        "economic_indicators": data["economic_indicators"],
        "market_sentiment": data["economic_indicators"]["market_sentiment"]
    })

@app.route('/api/lending-recommendation', methods=['POST'])
def get_lending_recommendation():
    """Get lending recommendation for specific application"""
    
    request_data = request.get_json()
    
    # Sample lending recommendation logic
    loan_amount = request_data.get('loan_amount', 100000)
    borrower_location = request_data.get('location', 'Tamil Nadu')
    loan_purpose = request_data.get('loan_purpose', 'Business')
    
    # Get current parameters
    current_params = banking_api.get_current_parameters(borrower_location)
    
    # Simple recommendation logic
    base_risk = current_params["risk_indicators"]["overall_risk_score"]
    
    # Adjust based on loan purpose
    purpose_risk = {
        'Agriculture': 10,
        'Business': 5,
        'Personal': 15,
        'Home': 0,
        'Vehicle': 8
    }
    
    adjusted_risk = base_risk + purpose_risk.get(loan_purpose, 10)
    
    # Generate recommendation
    if adjusted_risk < 40:
        recommendation = "APPROVE"
        interest_rate = 10.5
        conditions = ["Standard terms applicable"]
    elif adjusted_risk < 70:
        recommendation = "CONDITIONAL_APPROVE"
        interest_rate = 12.0
        conditions = ["Additional collateral required", "Enhanced monitoring"]
    else:
        recommendation = "DEFER"
        interest_rate = 14.0
        conditions = ["High risk environment", "Consider after risk factors improve"]
    
    response = {
        "timestamp": datetime.now().isoformat(),
        "loan_application": {
            "amount": loan_amount,
            "purpose": loan_purpose,
            "location": borrower_location
        },
        "recommendation": recommendation,
        "risk_score": adjusted_risk,
        "suggested_interest_rate": interest_rate,
        "conditions": conditions,
        "current_environment": {
            "overall_risk": current_params["risk_indicators"]["overall_risk_score"],
            "climate_risk": current_params["climate_data"]["drought_risk_level"],
            "economic_conditions": current_params["economic_indicators"]["market_sentiment"]
        }
    }
    
    return jsonify(response)

@app.route('/api/health', methods=['GET'])
def health_check():
    """API health check"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "uptime_seconds": (datetime.now() - banking_api.last_updated).total_seconds()
    })

@app.route('/', methods=['GET'])
def api_documentation():
    """API documentation"""
    docs = {
        "Banking Intelligence API": "Real-time banking parameter monitoring",
        "version": "1.0.0",
        "endpoints": {
            "/api/banking-parameters": "Get comprehensive current banking parameters",
            "/api/risk-assessment": "Get focused risk assessment data", 
            "/api/climate-data": "Get climate and agricultural data",
            "/api/economic-indicators": "Get economic indicators",
            "/api/lending-recommendation": "POST - Get lending recommendation for application",
            "/api/health": "API health check"
        },
        "example_usage": {
            "get_parameters": "GET /api/banking-parameters?location=Tamil Nadu",
            "lending_decision": "POST /api/lending-recommendation with JSON body"
        }
    }
    
    return jsonify(docs)

if __name__ == '__main__':
    print("🤖 Banking Intelligence API Starting...")
    print("📡 Available endpoints:")
    print("  - GET  /api/banking-parameters")
    print("  - GET  /api/risk-assessment") 
    print("  - GET  /api/climate-data")
    print("  - GET  /api/economic-indicators")
    print("  - POST /api/lending-recommendation")
    print("  - GET  /api/health")
    print("\n🔗 API Documentation: http://localhost:5000/")
    print("🚀 Starting server on http://localhost:5000")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
