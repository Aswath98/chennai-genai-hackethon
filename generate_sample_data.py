"""
Simple test to generate sample data
"""
import pandas as pd
import numpy as np
import os
from datetime import datetime
import random

# Set random seeds for reproducibility
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)

def generate_sample_data():
    """Generate a small sample dataset for testing"""
    print("Generating sample micro-lending data...")
    
    # Create directories
    os.makedirs("data", exist_ok=True)
    os.makedirs("results", exist_ok=True)
    
    # Generate districts (5 for testing)
    districts = []
    for i in range(1, 6):
        districts.append({
            "district_id": i,
            "district_name": f"District_{i:02d}",
            "coordinates": (
                np.random.uniform(8.0, 13.5),  # Tamil Nadu latitude range
                np.random.uniform(76.0, 80.5)  # Tamil Nadu longitude range
            )
        })
    
    districts_df = pd.DataFrame(districts)
    districts_df.to_csv("data/districts.csv", index=False)
    print(f"✅ Generated {len(districts_df)} districts")
    
    # Generate borrowers (100 per district)
    borrowers = []
    borrower_id = 1
    
    for district in districts:
        for _ in range(100):
            # Basic borrower data
            age = np.random.randint(18, 65)
            income = np.random.randint(10000, 150000)
            education = random.choice(["none", "primary", "secondary", "higher"])
            occupation = random.choice(["farmer", "laborer", "shopkeeper", "service", "unemployed"])
            
            # Geographic coordinates near district center
            base_lat, base_lon = district["coordinates"]
            borrower_lat = base_lat + np.random.normal(0, 0.1)
            borrower_lon = base_lon + np.random.normal(0, 0.1)
            
            # Risk factors
            credit_history = np.random.uniform(0, 10)
            existing_loans = np.random.randint(0, 5)
            has_savings = random.choice([True, False])
            monthly_expenses = np.random.randint(5000, 80000)
            
            # Calculate simple risk score
            risk_factors = {
                "age_risk": 0.5 if 25 <= age <= 45 else 0.8,
                "income_risk": max(0, 1 - income / 150000),
                "education_risk": {"none": 1.0, "primary": 0.7, "secondary": 0.4, "higher": 0.2}[education],
                "credit_risk": max(0, 1 - credit_history / 10)
            }
            
            overall_risk = sum(risk_factors.values()) / len(risk_factors)
            
            borrower = {
                "borrower_id": borrower_id,
                "district_id": district["district_id"],
                "block_id": (district["district_id"] - 1) * 3 + np.random.randint(1, 4),  # 3 blocks per district
                "panchayat_id": borrower_id,  # Simplified
                "name": f"Borrower_{borrower_id:04d}",
                "age": age,
                "gender": random.choice(["Male", "Female"]),
                "income": income,
                "education": education,
                "occupation": occupation,
                "credit_history": credit_history,
                "existing_loans": existing_loans,
                "has_savings_account": has_savings,
                "monthly_expenses": monthly_expenses,
                "latitude": borrower_lat,
                "longitude": borrower_lon,
                "overall_risk_score": overall_risk,
                "risk_category": (
                    "Very Low" if overall_risk <= 0.2 else
                    "Low" if overall_risk <= 0.4 else
                    "Medium" if overall_risk <= 0.6 else
                    "High" if overall_risk <= 0.8 else
                    "Very High"
                ),
                "total_loan_amount": np.random.randint(5000, 100000)
            }
            borrowers.append(borrower)
            borrower_id += 1
    
    borrowers_df = pd.DataFrame(borrowers)
    borrowers_df.to_csv("data/borrowers.csv", index=False)
    print(f"✅ Generated {len(borrowers_df)} borrowers")
    
    # Generate district-level risk aggregation
    district_risk = borrowers_df.groupby("district_id").agg({
        "overall_risk_score": ["mean", "std", "min", "max"],
        "borrower_id": "count",
        "total_loan_amount": "sum"
    }).round(4)
    
    district_risk.columns = [
        "avg_risk_score", "risk_score_std", "min_risk_score", "max_risk_score",
        "num_borrowers", "total_loan_volume"
    ]
    district_risk = district_risk.reset_index()
    district_risk["risk_level"] = district_risk["avg_risk_score"].apply(
        lambda x: (
            "Very Low" if x <= 0.2 else
            "Low" if x <= 0.4 else
            "Medium" if x <= 0.6 else
            "High" if x <= 0.8 else
            "Very High"
        )
    )
    
    district_risk.to_csv("results/district_risk_aggregation.csv", index=False)
    print(f"✅ Generated district risk aggregation")
    
    # Save individual risk scores
    borrowers_df.to_csv("results/individual_risk_scores.csv", index=False)
    print(f"✅ Generated individual risk scores")
    
    # Print summary
    print(f"\n📊 DATA SUMMARY:")
    print(f"  • Total borrowers: {len(borrowers_df):,}")
    print(f"  • Total districts: {len(districts_df)}")
    print(f"  • Average risk score: {borrowers_df['overall_risk_score'].mean():.4f}")
    print(f"  • Total loan volume: ₹{borrowers_df['total_loan_amount'].sum()/1e6:.1f}M")
    
    print(f"\n🎯 RISK DISTRIBUTION:")
    risk_dist = borrowers_df['risk_category'].value_counts(normalize=True)
    for category, percentage in risk_dist.items():
        print(f"  • {category}: {percentage:.1%}")
    
    return borrowers_df, districts_df, district_risk

if __name__ == "__main__":
    borrowers, districts, district_agg = generate_sample_data()
    print("\n🎉 Sample data generation completed successfully!")
    print("\n🚀 You can now test the dashboard with: streamlit run dashboard/app.py")
