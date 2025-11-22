#!/usr/bin/env python3
"""
Enhanced Excel-based Data Generator for Block/Panchayat Level Simulation
Generates comprehensive micro-lending risk assessment data using Excel input as reference
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os
import json
from typing import Dict, List, Any, Optional

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

class ExcelBasedDataGenerator:
    """Generate realistic micro-lending data using Excel input as reference"""
    
    def __init__(self, excel_path: str = "input_excel/input_data.xlsx"):
        self.excel_path = excel_path
        self.excel_data = None
        self.load_excel_data()
        
        # Tamil Nadu districts and their characteristics
        self.tamil_nadu_districts = {
            'Chennai': {'urban_ratio': 0.9, 'avg_income': 35000, 'literacy': 0.85},
            'Coimbatore': {'urban_ratio': 0.7, 'avg_income': 28000, 'literacy': 0.82},
            'Madurai': {'urban_ratio': 0.6, 'avg_income': 22000, 'literacy': 0.78},
            'Tiruchirappalli': {'urban_ratio': 0.5, 'avg_income': 20000, 'literacy': 0.75},
            'Salem': {'urban_ratio': 0.5, 'avg_income': 18000, 'literacy': 0.72},
            'Tirunelveli': {'urban_ratio': 0.4, 'avg_income': 16000, 'literacy': 0.70},
            'Vellore': {'urban_ratio': 0.4, 'avg_income': 17000, 'literacy': 0.71},
            'Thanjavur': {'urban_ratio': 0.3, 'avg_income': 15000, 'literacy': 0.68},
            'Kanchipuram': {'urban_ratio': 0.6, 'avg_income': 25000, 'literacy': 0.80},
            'Erode': {'urban_ratio': 0.5, 'avg_income': 19000, 'literacy': 0.73},
        }
        
    def load_excel_data(self) -> None:
        """Load and analyze Excel data"""
        if not os.path.exists(self.excel_path):
            print(f"⚠️  Excel file not found at {self.excel_path}")
            print("📊 Proceeding with default data generation")
            return
            
        try:
            # Try to read the Excel file
            excel_file = pd.ExcelFile(self.excel_path)
            print(f"📈 Found Excel file with sheets: {excel_file.sheet_names}")
            
            self.excel_data = {}
            for sheet_name in excel_file.sheet_names:
                try:
                    df = pd.read_excel(self.excel_path, sheet_name=sheet_name)
                    self.excel_data[sheet_name] = df
                    print(f"   ✅ Loaded sheet '{sheet_name}': {df.shape}")
                except Exception as e:
                    print(f"   ❌ Error loading sheet '{sheet_name}': {e}")
                    
        except Exception as e:
            print(f"❌ Error reading Excel file: {e}")
            self.excel_data = None
    
    def extract_geographic_hierarchy(self) -> Dict[str, List[str]]:
        """Extract or create geographic hierarchy from Excel data"""
        
        hierarchy = {'districts': [], 'blocks': [], 'panchayats': []}
        
        if self.excel_data:
            # Try to extract from Excel data
            for sheet_name, df in self.excel_data.items():
                print(f"🔍 Analyzing sheet '{sheet_name}' for geographic data...")
                
                # Look for common geographic column names
                geo_columns = []
                for col in df.columns:
                    col_lower = col.lower()
                    if any(keyword in col_lower for keyword in ['district', 'block', 'panchayat', 'village', 'taluk']):
                        geo_columns.append(col)
                        
                if geo_columns:
                    print(f"   📍 Found geographic columns: {geo_columns}")
                    
                    # Extract unique values
                    for col in geo_columns:
                        unique_values = df[col].dropna().unique()
                        if 'district' in col.lower():
                            hierarchy['districts'].extend(unique_values)
                        elif 'block' in col.lower() or 'taluk' in col.lower():
                            hierarchy['blocks'].extend(unique_values)
                        elif 'panchayat' in col.lower() or 'village' in col.lower():
                            hierarchy['panchayats'].extend(unique_values)
        
        # Remove duplicates
        for key in hierarchy:
            hierarchy[key] = list(set(hierarchy[key]))
            
        # If no data found in Excel, use default Tamil Nadu structure
        if not any(hierarchy.values()):
            print("📍 Using default Tamil Nadu geographic structure")
            hierarchy = self.create_default_hierarchy()
            
        return hierarchy
    
    def create_default_hierarchy(self) -> Dict[str, List[str]]:
        """Create default Tamil Nadu administrative hierarchy"""
        
        districts = list(self.tamil_nadu_districts.keys())
        
        # Generate blocks for each district (8-15 blocks per district)
        blocks = []
        block_suffixes = ['North', 'South', 'East', 'West', 'Central', 'Main', 'Rural', 'Urban']
        
        for district in districts:
            num_blocks = random.randint(8, 15)
            for i in range(num_blocks):
                if i < len(block_suffixes):
                    block_name = f"{district} {block_suffixes[i]}"
                else:
                    block_name = f"{district} Block-{i+1}"
                blocks.append(block_name)
        
        # Generate panchayats for each district (50-80 per district)
        panchayats = []
        panchayat_prefixes = [
            'Kuppam', 'Patti', 'Nagar', 'Pur', 'Gram', 'Guda', 'Pet', 'Palayam',
            'Kodai', 'Theru', 'Nallur', 'Perur', 'Mangalam', 'Puram', 'Nagar'
        ]
        
        for district in districts:
            num_panchayats = random.randint(50, 80)
            for i in range(num_panchayats):
                prefix = random.choice(panchayat_prefixes)
                panchayat_name = f"{prefix} {district[:3]}-{i+1:02d}"
                panchayats.append(panchayat_name)
        
        return {
            'districts': districts,
            'blocks': blocks,
            'panchayats': panchayats
        }
    
    def generate_enhanced_borrower_data(self, num_borrowers: int = 2000) -> pd.DataFrame:
        """Generate enhanced borrower data with comprehensive risk factors"""
        
        print(f"🏗️  Generating {num_borrowers} borrower records...")
        
        # Get geographic hierarchy
        geo_hierarchy = self.extract_geographic_hierarchy()
        
        borrowers = []
        
        # Indian names for realistic data
        first_names = [
            'Arjun', 'Priya', 'Rahul', 'Kavya', 'Amit', 'Sneha', 'Vikram', 'Pooja',
            'Raj', 'Meera', 'Suresh', 'Divya', 'Kiran', 'Anita', 'Manoj', 'Sita',
            'Kumar', 'Lakshmi', 'Ravi', 'Geetha', 'Arun', 'Kamala', 'Bala', 'Uma'
        ]
        
        last_names = [
            'Kumar', 'Singh', 'Sharma', 'Reddy', 'Patel', 'Nair', 'Iyer', 'Rao',
            'Gupta', 'Agarwal', 'Murugan', 'Krishnan', 'Subramanian', 'Venkatesh'
        ]
        
        occupations = [
            'Farmer', 'Shopkeeper', 'Tailor', 'Auto Driver', 'Construction Worker',
            'Domestic Helper', 'Street Vendor', 'Handicraft Maker', 'Small Trader',
            'Agricultural Laborer', 'Fisherman', 'Weaver', 'Mechanic', 'Carpenter'
        ]
        
        for i in range(num_borrowers):
            # Basic demographics
            age = np.random.normal(35, 12)
            age = max(18, min(70, int(age)))
            
            # Geographic assignment
            district = random.choice(geo_hierarchy['districts'])
            district_info = self.tamil_nadu_districts.get(district, {
                'urban_ratio': 0.5, 'avg_income': 20000, 'literacy': 0.75
            })
            
            # Income based on district and age
            base_income = district_info['avg_income']
            income_multiplier = 1 + (age - 30) * 0.01  # Slight income increase with age
            monthly_income = max(5000, int(np.random.lognormal(
                np.log(base_income), 0.6) * income_multiplier))
            
            # Education level
            education_levels = ['Illiterate', 'Primary', 'Secondary', 'Higher Secondary', 'Graduate']
            education_weights = [0.15, 0.25, 0.35, 0.20, 0.05]
            if random.random() < district_info['literacy']:
                education = np.random.choice(education_levels[1:], 
                                          p=[w/sum(education_weights[1:]) for w in education_weights[1:]])
            else:
                education = 'Illiterate'
            
            # Financial history
            years_in_location = min(age - 18, random.randint(1, 25))
            has_bank_account = random.random() < (0.7 + 0.2 * (education != 'Illiterate'))
            credit_history_length = random.randint(0, min(5, years_in_location)) if has_bank_account else 0
            
            # Loan request details
            loan_amount = random.choice([10000, 15000, 20000, 25000, 30000, 40000, 50000])
            loan_purpose = random.choice([
                'Business Expansion', 'Agriculture', 'Education', 'Medical Emergency',
                'Home Improvement', 'Vehicle Purchase', 'Marriage', 'Debt Consolidation'
            ])
            
            # Enhanced risk factors
            borrower = {
                # Basic Information
                'borrower_id': f"BR{i+1:06d}",
                'name': f"{random.choice(first_names)} {random.choice(last_names)}",
                'age': age,
                'gender': random.choice(['Male', 'Female']),
                
                # Geographic Information
                'district': district,
                'block': random.choice([b for b in geo_hierarchy['blocks'] if district.split()[0] in b][:5] 
                                     if any(district.split()[0] in b for b in geo_hierarchy['blocks']) 
                                     else geo_hierarchy['blocks'][:5]),
                'panchayat': random.choice([p for p in geo_hierarchy['panchayats'] 
                                          if district[:3] in p][:10] 
                                        if any(district[:3] in p for p in geo_hierarchy['panchayats']) 
                                        else geo_hierarchy['panchayats'][:10]),
                
                # Demographics
                'occupation': random.choice(occupations),
                'education_level': education,
                'marital_status': random.choice(['Married', 'Single', 'Widowed']),
                'family_size': random.randint(2, 8),
                'years_in_location': years_in_location,
                
                # Financial Information
                'monthly_income': monthly_income,
                'monthly_expenses': int(monthly_income * random.uniform(0.6, 0.9)),
                'has_bank_account': has_bank_account,
                'savings_amount': random.randint(0, monthly_income * 3) if has_bank_account else 0,
                'existing_loans': random.randint(0, 2) if random.random() < 0.4 else 0,
                'credit_history_length': credit_history_length,
                'previous_defaults': random.randint(0, 1) if credit_history_length > 0 and random.random() < 0.15 else 0,
                
                # Loan Information
                'requested_loan_amount': loan_amount,
                'loan_purpose': loan_purpose,
                'collateral_value': random.randint(loan_amount // 2, loan_amount * 2) if random.random() < 0.6 else 0,
                
                # Enhanced Risk Factors
                'mobile_ownership': random.random() < 0.85,
                'aadhaar_linked': random.random() < 0.75,
                'pan_card': random.random() < (0.3 if education in ['Illiterate', 'Primary'] else 0.7),
                
                # Asset Ownership
                'owns_land': random.random() < 0.4,
                'land_size_acres': random.uniform(0.5, 5) if random.random() < 0.4 else 0,
                'owns_livestock': random.random() < 0.3,
                'livestock_count': random.randint(1, 10) if random.random() < 0.3 else 0,
                'owns_vehicle': random.random() < 0.25,
                'vehicle_type': random.choice(['Bicycle', 'Motorcycle', 'Auto', 'Car']) if random.random() < 0.25 else None,
                
                # Infrastructure Access
                'electricity_access': random.random() < 0.85,
                'water_access': random.choice(['Piped', 'Well', 'Borewell', 'Public Tap']),
                'road_connectivity': random.choice(['Paved', 'Gravel', 'Mud']),
                'internet_access': random.random() < (0.6 if district_info['urban_ratio'] > 0.5 else 0.3),
                
                # Social Factors
                'shg_member': random.random() < 0.35,  # Self Help Group
                'shg_position': random.choice(['Member', 'Secretary', 'President']) if random.random() < 0.35 else None,
                'government_scheme_beneficiary': random.random() < 0.4,
                'insurance_coverage': random.random() < 0.3,
                
                # Behavioral Factors
                'seasonal_migration': random.random() < 0.2,
                'multiple_income_sources': random.random() < 0.4,
                'financial_literacy_score': random.randint(1, 10),
                'social_connections_score': random.randint(1, 10),
                
                # Generated timestamps
                'application_date': datetime.now() - timedelta(days=random.randint(1, 365)),
                'data_generation_timestamp': datetime.now()
            }
            
            # Calculate coordinates based on district (approximate Tamil Nadu bounds)
            lat_base = 8.0 + (hash(district) % 100) / 100 * 5  # 8°N to 13°N
            lon_base = 76.0 + (hash(district) % 100) / 100 * 5  # 76°E to 81°E
            
            borrower['latitude'] = lat_base + random.uniform(-0.5, 0.5)
            borrower['longitude'] = lon_base + random.uniform(-0.5, 0.5)
            
            borrowers.append(borrower)
        
        df = pd.DataFrame(borrowers)
        print(f"✅ Generated {len(df)} borrower records with {len(df.columns)} attributes")
        return df
    
    def calculate_comprehensive_risk_scores(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate comprehensive risk scores with multiple components"""
        
        print("🧮 Calculating comprehensive risk scores...")
        
        # Demographic Risk (weight: 20%)
        demo_risk = (
            (df['age'] > 55).astype(int) * 15 +  # Age risk
            (df['education_level'] == 'Illiterate').astype(int) * 20 +
            (df['family_size'] > 6).astype(int) * 10 +
            (df['years_in_location'] < 2).astype(int) * 15
        )
        
        # Financial Risk (weight: 30%)
        income_to_loan_ratio = df['monthly_income'] / df['requested_loan_amount'] * 1000
        expense_ratio = df['monthly_expenses'] / df['monthly_income']
        
        financial_risk = (
            (income_to_loan_ratio < 5).astype(int) * 25 +  # Low income to loan ratio
            (expense_ratio > 0.8).astype(int) * 20 +
            (~df['has_bank_account']).astype(int) * 15 +
            (df['existing_loans'] > 1).astype(int) * 20 +
            (df['previous_defaults'] > 0).astype(int) * 30 +
            (df['savings_amount'] < df['monthly_income']).astype(int) * 10
        )
        
        # Asset & Infrastructure Risk (weight: 25%)
        asset_risk = (
            (~df['owns_land']).astype(int) * 15 +
            (~df['owns_vehicle']).astype(int) * 10 +
            (~df['electricity_access']).astype(int) * 15 +
            (df['road_connectivity'] == 'Mud').astype(int) * 15 +
            (~df['internet_access']).astype(int) * 10 +
            (df['collateral_value'] < df['requested_loan_amount']).astype(int) * 20
        )
        
        # Social & Behavioral Risk (weight: 15%)
        social_risk = (
            (~df['shg_member']).astype(int) * 15 +
            (~df['mobile_ownership']).astype(int) * 10 +
            (~df['aadhaar_linked']).astype(int) * 10 +
            (df['seasonal_migration']).astype(int) * 20 +
            (df['financial_literacy_score'] < 5).astype(int) * 15
        )
        
        # Documentation Risk (weight: 10%)
        doc_risk = (
            (~df['pan_card']).astype(int) * 20 +
            (~df['insurance_coverage']).astype(int) * 10 +
            (df['credit_history_length'] == 0).astype(int) * 25
        )
        
        # Weighted risk score (0-100 scale)
        df['demographic_risk_score'] = np.clip(demo_risk * 0.2, 0, 100)
        df['financial_risk_score'] = np.clip(financial_risk * 0.3, 0, 100)
        df['asset_infrastructure_risk_score'] = np.clip(asset_risk * 0.25, 0, 100)
        df['social_behavioral_risk_score'] = np.clip(social_risk * 0.15, 0, 100)
        df['documentation_risk_score'] = np.clip(doc_risk * 0.1, 0, 100)
        
        # Overall risk score
        df['overall_risk_score'] = (
            df['demographic_risk_score'] * 0.2 +
            df['financial_risk_score'] * 0.3 +
            df['asset_infrastructure_risk_score'] * 0.25 +
            df['social_behavioral_risk_score'] * 0.15 +
            df['documentation_risk_score'] * 0.1
        )
        
        # Risk categories
        df['risk_category'] = pd.cut(
            df['overall_risk_score'],
            bins=[0, 25, 50, 75, 100],
            labels=['Low Risk', 'Medium Risk', 'High Risk', 'Very High Risk']
        )
        
        print(f"✅ Risk distribution:")
        print(df['risk_category'].value_counts())
        
        return df
    
    def generate_administrative_aggregations(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """Generate risk aggregations at different administrative levels"""
        
        print("📊 Generating administrative level aggregations...")
        
        aggregations = {}
        
        # Panchayat level aggregation
        panchayat_agg = df.groupby(['district', 'block', 'panchayat']).agg({
            'overall_risk_score': ['mean', 'std', 'count'],
            'requested_loan_amount': ['sum', 'mean'],
            'monthly_income': 'mean',
            'age': 'mean',
            'has_bank_account': 'sum',
            'owns_land': 'sum',
            'shg_member': 'sum'
        }).round(2)
        
        panchayat_agg.columns = ['_'.join(col).strip() for col in panchayat_agg.columns]
        panchayat_agg = panchayat_agg.reset_index()
        panchayat_agg['administrative_level'] = 'Panchayat'
        aggregations['panchayat'] = panchayat_agg
        
        # Block level aggregation  
        block_agg = df.groupby(['district', 'block']).agg({
            'overall_risk_score': ['mean', 'std', 'count'],
            'requested_loan_amount': ['sum', 'mean'],
            'monthly_income': 'mean',
            'age': 'mean',
            'has_bank_account': 'sum',
            'owns_land': 'sum',
            'shg_member': 'sum'
        }).round(2)
        
        block_agg.columns = ['_'.join(col).strip() for col in block_agg.columns]
        block_agg = block_agg.reset_index()
        block_agg['administrative_level'] = 'Block'
        aggregations['block'] = block_agg
        
        # District level aggregation
        district_agg = df.groupby('district').agg({
            'overall_risk_score': ['mean', 'std', 'count'],
            'requested_loan_amount': ['sum', 'mean'],
            'monthly_income': 'mean',
            'age': 'mean',
            'has_bank_account': 'sum',
            'owns_land': 'sum',
            'shg_member': 'sum'
        }).round(2)
        
        district_agg.columns = ['_'.join(col).strip() for col in district_agg.columns]
        district_agg = district_agg.reset_index()
        district_agg['administrative_level'] = 'District'
        aggregations['district'] = district_agg
        
        return aggregations
    
    def save_all_data(self, borrowers_df: pd.DataFrame, aggregations: Dict[str, pd.DataFrame]) -> None:
        """Save all generated data to files"""
        
        os.makedirs('data', exist_ok=True)
        os.makedirs('results', exist_ok=True)
        
        # Save borrower data
        borrowers_df.to_csv('data/enhanced_borrowers.csv', index=False)
        print(f"💾 Saved {len(borrowers_df)} borrower records to data/enhanced_borrowers.csv")
        
        # Save aggregations
        for level, df in aggregations.items():
            filename = f'results/{level}_risk_aggregation.csv'
            df.to_csv(filename, index=False)
            print(f"💾 Saved {len(df)} {level} records to {filename}")
        
        # Save summary statistics
        summary = {
            'generation_timestamp': datetime.now().isoformat(),
            'total_borrowers': len(borrowers_df),
            'districts': len(borrowers_df['district'].unique()),
            'blocks': len(borrowers_df['block'].unique()),
            'panchayats': len(borrowers_df['panchayat'].unique()),
            'avg_risk_score': float(borrowers_df['overall_risk_score'].mean()),
            'risk_distribution': borrowers_df['risk_category'].value_counts().to_dict()
        }
        
        with open('results/generation_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"📋 Saved generation summary to results/generation_summary.json")

def main():
    """Main execution function"""
    print("🚀 Starting Enhanced Excel-based Data Generation")
    print("=" * 60)
    
    # Initialize generator
    generator = ExcelBasedDataGenerator()
    
    # Generate borrower data
    borrowers_df = generator.generate_enhanced_borrower_data(num_borrowers=2000)
    
    # Calculate risk scores
    borrowers_df = generator.calculate_comprehensive_risk_scores(borrowers_df)
    
    # Generate administrative aggregations
    aggregations = generator.generate_administrative_aggregations(borrowers_df)
    
    # Save all data
    generator.save_all_data(borrowers_df, aggregations)
    
    print("\n" + "=" * 60)
    print("✅ Enhanced data generation completed successfully!")
    print("🎯 Generated comprehensive micro-lending risk assessment dataset")
    print("📊 Ready for ML model training and dashboard visualization")

if __name__ == "__main__":
    main()
