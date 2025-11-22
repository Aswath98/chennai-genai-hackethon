#!/usr/bin/env python3
"""
Excel-Enhanced Data Generator and Risk Assessment System
Integrates Excel input data to create realistic block/panchayat level micro-lending data
"""

import pandas as pd
import numpy as np
import os
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional

# Set random seeds for reproducibility
np.random.seed(42)
random.seed(42)

class ExcelEnhancedDataGenerator:
    """Enhanced data generator that uses Excel input for realistic geographic hierarchies"""
    
    def __init__(self):
        self.excel_data = None
        self.geographic_hierarchy = None
        self.risk_factors = {}
        
        # Enhanced Tamil Nadu districts with detailed characteristics
        self.tn_districts = {
            'Chennai': {
                'urban_ratio': 0.95, 'literacy': 0.90, 'banking_density': 0.85,
                'avg_income': 45000, 'infrastructure_score': 9.2, 'coords': (13.0827, 80.2707)
            },
            'Coimbatore': {
                'urban_ratio': 0.75, 'literacy': 0.84, 'banking_density': 0.70,
                'avg_income': 32000, 'infrastructure_score': 8.1, 'coords': (11.0168, 76.9558)
            },
            'Madurai': {
                'urban_ratio': 0.65, 'literacy': 0.78, 'banking_density': 0.65,
                'avg_income': 25000, 'infrastructure_score': 7.3, 'coords': (9.9252, 78.1198)
            },
            'Tiruchirappalli': {
                'urban_ratio': 0.60, 'literacy': 0.76, 'banking_density': 0.62,
                'avg_income': 23000, 'infrastructure_score': 7.0, 'coords': (10.7905, 78.7047)
            },
            'Salem': {
                'urban_ratio': 0.55, 'literacy': 0.72, 'banking_density': 0.58,
                'avg_income': 21000, 'infrastructure_score': 6.8, 'coords': (11.6643, 78.1460)
            },
            'Tirunelveli': {
                'urban_ratio': 0.45, 'literacy': 0.70, 'banking_density': 0.50,
                'avg_income': 19000, 'infrastructure_score': 6.2, 'coords': (8.7139, 77.7567)
            },
            'Vellore': {
                'urban_ratio': 0.50, 'literacy': 0.74, 'banking_density': 0.55,
                'avg_income': 20000, 'infrastructure_score': 6.5, 'coords': (12.9165, 79.1325)
            },
            'Thanjavur': {
                'urban_ratio': 0.40, 'literacy': 0.73, 'banking_density': 0.48,
                'avg_income': 18000, 'infrastructure_score': 6.0, 'coords': (10.7870, 79.1378)
            },
            'Erode': {
                'urban_ratio': 0.52, 'literacy': 0.75, 'banking_density': 0.60,
                'avg_income': 22000, 'infrastructure_score': 6.9, 'coords': (11.3410, 77.7172)
            },
            'Kanchipuram': {
                'urban_ratio': 0.68, 'literacy': 0.82, 'banking_density': 0.75,
                'avg_income': 28000, 'infrastructure_score': 7.8, 'coords': (12.8342, 79.7036)
            }
        }
    
    def load_excel_data(self) -> bool:
        """Load and process Excel data"""
        
        excel_path = "input_excel/input_data.xlsx"
        print(f"🔍 Looking for Excel file: {excel_path}")
        
        if not os.path.exists(excel_path):
            print("⚠️  Excel file not found, creating sample structure...")
            self._create_sample_excel_data()
            
        try:
            # Try reading the Excel file
            self.excel_data = pd.read_excel(excel_path)
            print(f"✅ Loaded Excel data: {self.excel_data.shape}")
            
            # Extract geographic hierarchy from Excel
            self._extract_geographic_hierarchy()
            return True
            
        except Exception as e:
            print(f"❌ Error loading Excel data: {e}")
            self._create_default_hierarchy()
            return False
    
    def _create_sample_excel_data(self):
        """Create sample Excel data for demonstration"""
        
        print("📊 Creating sample Excel data structure...")
        
        districts = list(self.tn_districts.keys())
        rows = []
        
        for district in districts:
            district_info = self.tn_districts[district]
            
            # Create blocks for each district
            for i in range(8, 15):  # 8-14 blocks per district
                block_name = f"{district} Block-{i}"
                
                # Create panchayats for each block
                for j in range(15, 25):  # 15-24 panchayats per block
                    panchayat_name = f"Panchayat-{district[:3]}-{i}-{j}"
                    
                    row = {
                        'District': district,
                        'Block': block_name,
                        'Panchayat': panchayat_name,
                        'Population': random.randint(2000, 15000),
                        'Literacy_Rate': district_info['literacy'] + random.uniform(-0.1, 0.1),
                        'Banking_Penetration': district_info['banking_density'] + random.uniform(-0.15, 0.1),
                        'Agriculture_Percentage': random.uniform(0.3, 0.8),
                        'Infrastructure_Score': district_info['infrastructure_score'] + random.uniform(-1, 1),
                        'SHG_Count': random.randint(5, 50),
                        'Bank_Branch_Count': random.randint(1, 5),
                        'ATM_Count': random.randint(2, 12)
                    }
                    rows.append(row)
        
        # Create Excel file
        df = pd.DataFrame(rows)
        os.makedirs('input_excel', exist_ok=True)
        df.to_excel('input_excel/input_data.xlsx', index=False)
        
        print(f"✅ Created sample Excel with {len(df)} administrative units")
        self.excel_data = df
    
    def _extract_geographic_hierarchy(self):
        """Extract geographic hierarchy from Excel data"""
        
        if self.excel_data is None:
            return
        
        # Look for geographic columns
        geo_cols = {}
        for col in self.excel_data.columns:
            col_lower = col.lower()
            if 'district' in col_lower:
                geo_cols['district'] = col
            elif 'block' in col_lower or 'taluk' in col_lower:
                geo_cols['block'] = col
            elif 'panchayat' in col_lower or 'village' in col_lower:
                geo_cols['panchayat'] = col
        
        if geo_cols:
            self.geographic_hierarchy = {}
            for level, col in geo_cols.items():
                self.geographic_hierarchy[level] = self.excel_data[col].unique().tolist()
            
            print(f"📍 Extracted hierarchy: {len(self.geographic_hierarchy.get('district', []))} districts, "
                  f"{len(self.geographic_hierarchy.get('block', []))} blocks, "
                  f"{len(self.geographic_hierarchy.get('panchayat', []))} panchayats")
        else:
            print("⚠️  No geographic columns found in Excel")
            self._create_default_hierarchy()
    
    def _create_default_hierarchy(self):
        """Create default geographic hierarchy"""
        
        self.geographic_hierarchy = {
            'district': list(self.tn_districts.keys()),
            'block': [],
            'panchayat': []
        }
        
        # Generate blocks and panchayats
        for district in self.tn_districts.keys():
            for i in range(8, 15):
                self.geographic_hierarchy['block'].append(f"{district} Block-{i}")
                
            for i in range(50, 100):
                self.geographic_hierarchy['panchayat'].append(f"Panchayat-{district[:3]}-{i}")
    
    def generate_enhanced_borrowers(self, num_borrowers: int = 3000) -> pd.DataFrame:
        """Generate comprehensive borrower dataset with Excel integration"""
        
        print(f"🏗️  Generating {num_borrowers} enhanced borrower records...")
        
        borrowers = []
        
        # Enhanced attributes
        first_names = [
            'Arjun', 'Priya', 'Rahul', 'Kavya', 'Amit', 'Sneha', 'Vikram', 'Pooja',
            'Raj', 'Meera', 'Suresh', 'Divya', 'Kiran', 'Anita', 'Manoj', 'Sita',
            'Kumar', 'Lakshmi', 'Ravi', 'Geetha', 'Arun', 'Kamala', 'Bala', 'Uma',
            'Selvam', 'Devi', 'Murugan', 'Kamala', 'Senthil', 'Bharathi'
        ]
        
        last_names = [
            'Kumar', 'Singh', 'Sharma', 'Reddy', 'Patel', 'Nair', 'Iyer', 'Rao',
            'Murugan', 'Krishnan', 'Subramanian', 'Venkatesh', 'Raman', 'Selvam'
        ]
        
        occupations = [
            'Farmer', 'Shopkeeper', 'Tailor', 'Auto Driver', 'Construction Worker',
            'Domestic Helper', 'Street Vendor', 'Handicraft Maker', 'Small Trader',
            'Agricultural Laborer', 'Fisherman', 'Weaver', 'Mechanic', 'Carpenter',
            'Mason', 'Electrician', 'Milkman', 'Fruit Vendor', 'Tea Seller'
        ]
        
        loan_purposes = [
            'Business Expansion', 'Agriculture', 'Education', 'Medical Emergency',
            'Home Improvement', 'Vehicle Purchase', 'Marriage', 'Debt Consolidation',
            'Livestock Purchase', 'Equipment Purchase', 'Seeds & Fertilizers'
        ]
        
        for i in range(num_borrowers):
            # Basic demographics
            age = max(18, min(70, int(np.random.normal(38, 14))))
            gender = random.choice(['Male', 'Female'])
            
            # Geographic assignment
            district = random.choice(self.geographic_hierarchy['district'])
            district_info = self.tn_districts.get(district, {
                'urban_ratio': 0.5, 'literacy': 0.75, 'banking_density': 0.6,
                'avg_income': 25000, 'infrastructure_score': 7.0, 'coords': (11.0, 78.0)
            })
            
            # Select block and panchayat related to district
            district_blocks = [b for b in self.geographic_hierarchy['block'] if district in b]
            district_panchayats = [p for p in self.geographic_hierarchy['panchayat'] if district[:3] in p]
            
            block = random.choice(district_blocks) if district_blocks else f"{district} Block-1"
            panchayat = random.choice(district_panchayats) if district_panchayats else f"Panchayat-{district[:3]}-1"
            
            # Income calculation with multiple factors
            base_income = district_info['avg_income']
            age_factor = 1 + (age - 30) * 0.01  # Slight increase with age
            education_bonus = 1.0
            
            education_level = 'Illiterate'
            if random.random() < district_info['literacy']:
                education_options = ['Primary', 'Secondary', 'Higher Secondary', 'Graduate']
                education_weights = [0.4, 0.35, 0.2, 0.05]
                education_level = np.random.choice(education_options, p=education_weights)
                education_bonus = {'Primary': 1.1, 'Secondary': 1.25, 'Higher Secondary': 1.4, 'Graduate': 1.8}[education_level]
            
            monthly_income = max(8000, int(np.random.lognormal(
                np.log(base_income), 0.5) * age_factor * education_bonus))
            
            # Financial profile
            has_bank_account = random.random() < (district_info['banking_density'] + 
                                                 (0.2 if education_level != 'Illiterate' else 0))
            credit_history_length = random.randint(0, min(8, age - 18)) if has_bank_account else 0
            savings_amount = random.randint(0, monthly_income * 4) if has_bank_account else 0
            
            # Loan details
            loan_amount = random.choice([15000, 20000, 25000, 30000, 40000, 50000, 75000])
            loan_purpose = random.choice(loan_purposes)
            
            # Enhanced risk factors
            borrower = {
                # Basic Information
                'borrower_id': f"BRW{i+1:06d}",
                'name': f"{random.choice(first_names)} {random.choice(last_names)}",
                'age': age,
                'gender': gender,
                
                # Geographic
                'district': district,
                'block': block,
                'panchayat': panchayat,
                'latitude': district_info['coords'][0] + random.uniform(-0.5, 0.5),
                'longitude': district_info['coords'][1] + random.uniform(-0.5, 0.5),
                
                # Demographics
                'education_level': education_level,
                'occupation': random.choice(occupations),
                'marital_status': random.choice(['Single', 'Married', 'Widowed']),
                'family_size': random.randint(2, 8),
                'years_in_location': min(age - 18, random.randint(1, 30)),
                'religion': random.choice(['Hindu', 'Muslim', 'Christian', 'Others']),
                'caste_category': random.choice(['General', 'OBC', 'SC', 'ST']),
                
                # Financial
                'monthly_income': monthly_income,
                'monthly_expenses': int(monthly_income * random.uniform(0.65, 0.88)),
                'has_bank_account': has_bank_account,
                'bank_account_type': random.choice(['Savings', 'Current', 'Jan Dhan']) if has_bank_account else None,
                'savings_amount': savings_amount,
                'existing_loans': random.randint(0, 3) if random.random() < 0.35 else 0,
                'credit_history_length': credit_history_length,
                'credit_score': random.randint(300, 850) if credit_history_length > 0 else None,
                'previous_defaults': random.randint(0, 1) if credit_history_length > 0 and random.random() < 0.12 else 0,
                
                # Loan Information
                'requested_loan_amount': loan_amount,
                'loan_purpose': loan_purpose,
                'collateral_offered': random.random() < 0.65,
                'collateral_value': random.randint(loan_amount, loan_amount * 3) if random.random() < 0.65 else 0,
                'guarantor_available': random.random() < 0.70,
                
                # Digital & Documentation
                'mobile_ownership': random.random() < 0.90,
                'smartphone_user': random.random() < 0.60,
                'internet_usage': random.random() < 0.45,
                'aadhaar_linked': random.random() < 0.85,
                'pan_card': random.random() < (0.25 if education_level in ['Illiterate', 'Primary'] else 0.75),
                'driving_license': random.random() < 0.30,
                'voter_id': random.random() < 0.80,
                
                # Assets & Property
                'owns_house': random.random() < 0.70,
                'house_type': random.choice(['Kutcha', 'Semi-Pucca', 'Pucca']),
                'owns_land': random.random() < 0.45,
                'land_size_acres': random.uniform(0.25, 8.0) if random.random() < 0.45 else 0,
                'owns_livestock': random.random() < 0.35,
                'livestock_count': random.randint(1, 15) if random.random() < 0.35 else 0,
                'owns_vehicle': random.random() < 0.40,
                'vehicle_type': random.choice(['Bicycle', 'Motorcycle', 'Auto', 'Tractor', 'Car']) if random.random() < 0.40 else None,
                
                # Infrastructure Access
                'electricity_connection': random.random() < 0.88,
                'water_source': random.choice(['Piped', 'Borewell', 'Well', 'Public Tap', 'Hand Pump']),
                'toilet_facility': random.random() < 0.75,
                'cooking_fuel': random.choice(['LPG', 'Kerosene', 'Wood', 'Coal']),
                'road_connectivity': random.choice(['Paved', 'Gravel', 'Mud']),
                
                # Social & Financial Inclusion
                'shg_member': random.random() < 0.40,
                'shg_position': random.choice(['Member', 'Secretary', 'President', 'Treasurer']) if random.random() < 0.40 else None,
                'shg_savings': random.randint(1000, 10000) if random.random() < 0.40 else 0,
                'insurance_life': random.random() < 0.35,
                'insurance_health': random.random() < 0.25,
                'insurance_crop': random.random() < 0.20,
                'pradhan_mantri_schemes': random.choice(['Jan Dhan', 'Ujjwala', 'Awas', 'None']),
                
                # Behavioral & Social
                'seasonal_migration': random.random() < 0.25,
                'multiple_income_sources': random.random() < 0.45,
                'remittances_received': random.random() < 0.20,
                'community_reputation': random.choice(['Excellent', 'Good', 'Average', 'Poor']),
                'financial_literacy_score': random.randint(1, 10),
                'social_connections_score': random.randint(1, 10),
                'local_leader_recommendation': random.random() < 0.30,
                
                # Agricultural (if applicable)
                'primary_crop': random.choice(['Rice', 'Cotton', 'Sugarcane', 'Groundnut', 'Millets', 'None']),
                'irrigation_access': random.random() < 0.55,
                'crop_insurance': random.random() < 0.15,
                'market_access_score': random.randint(1, 10),
                
                # Timestamps
                'application_date': datetime.now() - timedelta(days=random.randint(1, 365)),
                'data_creation_timestamp': datetime.now()
            }
            
            borrowers.append(borrower)
        
        df = pd.DataFrame(borrowers)
        print(f"✅ Generated {len(df)} borrower records with {len(df.columns)} attributes")
        return df
    
    def calculate_comprehensive_risk_scores(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate multi-dimensional risk scores"""
        
        print("🧮 Calculating comprehensive risk assessment...")
        
        # 1. Demographic Risk (Weight: 18%)
        demo_risk = (
            (df['age'] > 60).astype(int) * 12 +
            (df['age'] < 25).astype(int) * 8 +
            (df['education_level'] == 'Illiterate').astype(int) * 20 +
            (df['family_size'] > 7).astype(int) * 10 +
            (df['years_in_location'] < 3).astype(int) * 12
        )
        
        # 2. Financial Risk (Weight: 25%)
        income_loan_ratio = df['monthly_income'] / df['requested_loan_amount'] * 1000
        expense_ratio = df['monthly_expenses'] / df['monthly_income']
        
        financial_risk = (
            (income_loan_ratio < 6).astype(int) * 25 +
            (expense_ratio > 0.85).astype(int) * 20 +
            (~df['has_bank_account']).astype(int) * 15 +
            (df['existing_loans'] > 2).astype(int) * 20 +
            (df['previous_defaults'] > 0).astype(int) * 35 +
            (df['savings_amount'] < df['monthly_income']).astype(int) * 10 +
            ((df['credit_score'].fillna(0) < 600) & (df['credit_score'].notna())).astype(int) * 15
        )
        
        # 3. Asset & Collateral Risk (Weight: 22%)
        asset_risk = (
            (~df['owns_house']).astype(int) * 12 +
            (df['house_type'] == 'Kutcha').astype(int) * 8 +
            (~df['owns_land']).astype(int) * 15 +
            (~df['owns_vehicle']).astype(int) * 8 +
            (~df['collateral_offered']).astype(int) * 18 +
            (df['collateral_value'] < df['requested_loan_amount']).astype(int) * 15 +
            (~df['guarantor_available']).astype(int) * 10
        )
        
        # 4. Social & Digital Risk (Weight: 15%)
        social_risk = (
            (~df['shg_member']).astype(int) * 15 +
            (~df['mobile_ownership']).astype(int) * 12 +
            (~df['aadhaar_linked']).astype(int) * 10 +
            (df['seasonal_migration']).astype(int) * 18 +
            (df['financial_literacy_score'] < 5).astype(int) * 12 +
            (df['community_reputation'] == 'Poor').astype(int) * 20 +
            (~df['local_leader_recommendation']).astype(int) * 8
        )
        
        # 5. Infrastructure & Access Risk (Weight: 12%)
        infrastructure_risk = (
            (~df['electricity_connection']).astype(int) * 15 +
            (df['water_source'].isin(['Hand Pump', 'Public Tap'])).astype(int) * 10 +
            (~df['toilet_facility']).astype(int) * 8 +
            (df['road_connectivity'] == 'Mud').astype(int) * 12 +
            (~df['internet_usage']).astype(int) * 8 +
            (df['market_access_score'] < 5).astype(int) * 10
        )
        
        # 6. Documentation Risk (Weight: 8%)
        doc_risk = (
            (~df['pan_card']).astype(int) * 20 +
            (~df['insurance_life']).astype(int) * 10 +
            (~df['insurance_health']).astype(int) * 12 +
            (df['credit_history_length'] == 0).astype(int) * 25 +
            (~df['voter_id']).astype(int) * 5
        )
        
        # Calculate component scores (0-100 scale)
        df['demographic_risk_score'] = np.clip(demo_risk * 0.18, 0, 100)
        df['financial_risk_score'] = np.clip(financial_risk * 0.25, 0, 100)
        df['asset_collateral_risk_score'] = np.clip(asset_risk * 0.22, 0, 100)
        df['social_digital_risk_score'] = np.clip(social_risk * 0.15, 0, 100)
        df['infrastructure_risk_score'] = np.clip(infrastructure_risk * 0.12, 0, 100)
        df['documentation_risk_score'] = np.clip(doc_risk * 0.08, 0, 100)
        
        # Overall weighted risk score
        df['overall_risk_score'] = (
            df['demographic_risk_score'] * 0.18 +
            df['financial_risk_score'] * 0.25 +
            df['asset_collateral_risk_score'] * 0.22 +
            df['social_digital_risk_score'] * 0.15 +
            df['infrastructure_risk_score'] * 0.12 +
            df['documentation_risk_score'] * 0.08
        )
        
        # Risk categories with refined thresholds
        df['risk_category'] = pd.cut(
            df['overall_risk_score'],
            bins=[0, 20, 40, 65, 100],
            labels=['Low Risk', 'Medium Risk', 'High Risk', 'Very High Risk'],
            include_lowest=True
        )
        
        # Additional risk indicators
        df['default_probability'] = np.clip(df['overall_risk_score'] / 100 * 0.25, 0, 1)
        df['recommended_interest_rate'] = 12 + (df['overall_risk_score'] / 100) * 8  # 12-20% range
        
        print("📊 Risk Score Distribution:")
        print(df['risk_category'].value_counts())
        print(f"\nAverage Risk Score: {df['overall_risk_score'].mean():.2f}")
        
        return df
    
    def generate_administrative_aggregations(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """Generate risk aggregations at all administrative levels"""
        
        print("📊 Creating administrative risk aggregations...")
        
        aggregations = {}
        
        # Panchayat level
        panchayat_agg = df.groupby(['district', 'block', 'panchayat']).agg({
            'overall_risk_score': ['mean', 'std', 'count', 'min', 'max'],
            'requested_loan_amount': ['sum', 'mean', 'count'],
            'monthly_income': ['mean', 'median'],
            'age': 'mean',
            'has_bank_account': 'sum',
            'owns_land': 'sum',
            'shg_member': 'sum',
            'financial_literacy_score': 'mean',
            'default_probability': 'mean'
        }).round(3)
        
        panchayat_agg.columns = ['_'.join(col).strip() for col in panchayat_agg.columns]
        panchayat_agg = panchayat_agg.reset_index()
        panchayat_agg['administrative_level'] = 'Panchayat'
        aggregations['panchayat'] = panchayat_agg
        
        # Block level
        block_agg = df.groupby(['district', 'block']).agg({
            'overall_risk_score': ['mean', 'std', 'count', 'min', 'max'],
            'requested_loan_amount': ['sum', 'mean', 'count'],
            'monthly_income': ['mean', 'median'],
            'age': 'mean',
            'has_bank_account': 'sum',
            'owns_land': 'sum',
            'shg_member': 'sum',
            'financial_literacy_score': 'mean',
            'default_probability': 'mean'
        }).round(3)
        
        block_agg.columns = ['_'.join(col).strip() for col in block_agg.columns]
        block_agg = block_agg.reset_index()
        block_agg['administrative_level'] = 'Block'
        aggregations['block'] = block_agg
        
        # District level
        district_agg = df.groupby('district').agg({
            'overall_risk_score': ['mean', 'std', 'count', 'min', 'max'],
            'requested_loan_amount': ['sum', 'mean', 'count'],
            'monthly_income': ['mean', 'median'],
            'age': 'mean',
            'has_bank_account': 'sum',
            'owns_land': 'sum',
            'shg_member': 'sum',
            'financial_literacy_score': 'mean',
            'default_probability': 'mean'
        }).round(3)
        
        district_agg.columns = ['_'.join(col).strip() for col in district_agg.columns]
        district_agg = district_agg.reset_index()
        district_agg['administrative_level'] = 'District'
        aggregations['district'] = district_agg
        
        return aggregations
    
    def save_all_data(self, borrowers_df: pd.DataFrame, aggregations: Dict[str, pd.DataFrame]):
        """Save all generated data with proper organization"""
        
        print("💾 Saving comprehensive dataset...")
        
        # Ensure directories exist
        os.makedirs('data', exist_ok=True)
        os.makedirs('results', exist_ok=True)
        
        # Save main borrower dataset
        borrowers_df.to_csv('data/enhanced_borrowers_comprehensive.csv', index=False)
        print(f"✅ Saved {len(borrowers_df)} borrower records")
        
        # Save administrative aggregations
        for level, df_agg in aggregations.items():
            filename = f'results/{level}_comprehensive_risk_aggregation.csv'
            df_agg.to_csv(filename, index=False)
            print(f"✅ Saved {len(df_agg)} {level} aggregations")
        
        # Create summary report
        summary = {
            'generation_timestamp': datetime.now().isoformat(),
            'total_borrowers': len(borrowers_df),
            'districts_count': len(borrowers_df['district'].unique()),
            'blocks_count': len(borrowers_df['block'].unique()),
            'panchayats_count': len(borrowers_df['panchayat'].unique()),
            'overall_stats': {
                'avg_risk_score': float(borrowers_df['overall_risk_score'].mean()),
                'avg_loan_amount': float(borrowers_df['requested_loan_amount'].mean()),
                'avg_income': float(borrowers_df['monthly_income'].mean()),
                'bank_account_penetration': float(borrowers_df['has_bank_account'].mean()),
                'shg_penetration': float(borrowers_df['shg_member'].mean()),
                'land_ownership_rate': float(borrowers_df['owns_land'].mean())
            },
            'risk_distribution': borrowers_df['risk_category'].value_counts().to_dict(),
            'top_districts_by_risk': borrowers_df.groupby('district')['overall_risk_score'].mean().nlargest(5).to_dict(),
            'excel_integration_status': self.excel_data is not None
        }
        
        with open('results/comprehensive_generation_summary.json', 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        print(f"📋 Summary saved to results/comprehensive_generation_summary.json")
        
        # Display key metrics
        print(f"\n📊 KEY METRICS:")
        print(f"  Total Borrowers: {len(borrowers_df):,}")
        print(f"  Average Risk Score: {borrowers_df['overall_risk_score'].mean():.2f}")
        print(f"  Average Loan Amount: ₹{borrowers_df['requested_loan_amount'].mean():,.0f}")
        print(f"  Bank Account Penetration: {borrowers_df['has_bank_account'].mean():.1%}")
        print(f"  SHG Membership: {borrowers_df['shg_member'].mean():.1%}")

def main():
    """Main execution function"""
    
    print("🚀 EXCEL-ENHANCED MICRO-LENDING RISK ASSESSMENT")
    print("=" * 80)
    print(f"Generation Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Initialize enhanced generator
    generator = ExcelEnhancedDataGenerator()
    
    # Load Excel data
    excel_loaded = generator.load_excel_data()
    
    # Generate comprehensive borrower data
    borrowers_df = generator.generate_enhanced_borrowers(num_borrowers=3000)
    
    # Calculate comprehensive risk scores
    borrowers_df = generator.calculate_comprehensive_risk_scores(borrowers_df)
    
    # Generate administrative aggregations
    aggregations = generator.generate_administrative_aggregations(borrowers_df)
    
    # Save all data
    generator.save_all_data(borrowers_df, aggregations)
    
    print("\n" + "=" * 80)
    print("✅ COMPREHENSIVE DATA GENERATION COMPLETED!")
    print("🎯 Enhanced micro-lending platform ready for deployment")
    print("📊 Run dashboard applications for interactive analysis")
    print("🤖 Ready for ML model training and risk prediction")
    print("=" * 80)

if __name__ == "__main__":
    main()
