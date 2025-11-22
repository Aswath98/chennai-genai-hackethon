"""
Enhanced Data Generator using Excel input for Block/Panchayat level analysis
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

def load_excel_data():
    """Load and analyze Excel input data"""
    excel_path = "input_excel/input_data.xlsx"
    
    print(f"📊 Loading Excel data from {excel_path}...")
    
    if not os.path.exists(excel_path):
        print("⚠️  Excel file not found, using default geographic structure")
        return None
    
    try:
        # Try to read all sheets
        excel_file = pd.ExcelFile(excel_path)
        sheets = {}
        
        print(f"📋 Found {len(excel_file.sheet_names)} sheets: {excel_file.sheet_names}")
        
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(excel_path, sheet_name=sheet_name)
            sheets[sheet_name] = df
            print(f"✅ Loaded '{sheet_name}': {df.shape[0]} rows, {df.shape[1]} columns")
            
            # Show column names
            print(f"   Columns: {list(df.columns)[:10]}{'...' if len(df.columns) > 10 else ''}")
            
        return sheets
        
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")
        return None

def extract_geographic_hierarchy(excel_data):
    """Extract or create geographic hierarchy"""
    
    if excel_data:
        print(f"🗺️  Extracting geographic hierarchy from Excel data...")
        # Use first sheet as primary data source
        main_sheet_name = list(excel_data.keys())[0]
        main_df = excel_data[main_sheet_name]
        
        print(f"📊 Using primary sheet: '{main_sheet_name}' with {len(main_df)} records")
        
        # Look for geographic columns
        geo_columns = {}
        for col in main_df.columns:
            col_lower = str(col).lower()
            if any(keyword in col_lower for keyword in ['district', 'dist']):
                geo_columns['district'] = col
            elif any(keyword in col_lower for keyword in ['block', 'taluk', 'taluka', 'mandal']):
                geo_columns['block'] = col
            elif any(keyword in col_lower for keyword in ['panchayat', 'village', 'gram', 'town']):
                geo_columns['panchayat'] = col
        
        print(f"🔍 Geographic columns found: {geo_columns}")
        
        # Extract unique values and create hierarchy
        hierarchy = create_hierarchy_from_excel(main_df, geo_columns)
        
    else:
        print(f"🏗️  Creating default Tamil Nadu geographic hierarchy...")
        hierarchy = create_default_tamil_nadu_hierarchy()
    
    return hierarchy

def create_hierarchy_from_excel(df, geo_columns):
    """Create hierarchy from Excel data"""
    
    hierarchy = {'districts': [], 'blocks': [], 'panchayats': []}
    
    # Extract districts
    if 'district' in geo_columns:
        district_col = geo_columns['district']
        unique_districts = df[district_col].dropna().unique()
        
        for i, district_name in enumerate(unique_districts):
            hierarchy['districts'].append({
                'district_id': i + 1,
                'district_name': str(district_name).strip(),
                'coordinates': generate_tamil_nadu_coordinates()
            })
        
        print(f"📍 Extracted {len(hierarchy['districts'])} districts from Excel")
    
    # Extract blocks
    if 'block' in geo_columns and 'district' in geo_columns:
        # Group by district and block
        block_groups = df.groupby([geo_columns['district'], geo_columns['block']]).size()
        
        block_id = 1
        for (district_name, block_name), count in block_groups.items():
            # Find district_id
            district_id = None
            for d in hierarchy['districts']:
                if d['district_name'] == str(district_name).strip():
                    district_id = d['district_id']
                    break
            
            if district_id:
                hierarchy['blocks'].append({
                    'district_id': district_id,
                    'block_id': block_id,
                    'block_name': str(block_name).strip(),
                    'coordinates': generate_tamil_nadu_coordinates()
                })
                block_id += 1
        
        print(f"📍 Extracted {len(hierarchy['blocks'])} blocks from Excel")
    
    # Extract panchayats
    if 'panchayat' in geo_columns and 'block' in geo_columns and 'district' in geo_columns:
        # Group by all three levels
        panchayat_groups = df.groupby([geo_columns['district'], geo_columns['block'], geo_columns['panchayat']]).size()
        
        panchayat_id = 1
        for (district_name, block_name, panchayat_name), count in panchayat_groups.items():
            # Find district_id and block_id
            district_id = None
            block_id = None
            
            for d in hierarchy['districts']:
                if d['district_name'] == str(district_name).strip():
                    district_id = d['district_id']
                    break
            
            for b in hierarchy['blocks']:
                if b['district_id'] == district_id and b['block_name'] == str(block_name).strip():
                    block_id = b['block_id']
                    break
            
            if district_id and block_id:
                hierarchy['panchayats'].append({
                    'district_id': district_id,
                    'block_id': block_id,
                    'panchayat_id': panchayat_id,
                    'panchayat_name': str(panchayat_name).strip(),
                    'coordinates': generate_tamil_nadu_coordinates()
                })
                panchayat_id += 1
        
        print(f"📍 Extracted {len(hierarchy['panchayats'])} panchayats from Excel")
    
    # Fill missing levels if needed
    hierarchy = ensure_complete_hierarchy(hierarchy)
    
    return hierarchy

def create_default_tamil_nadu_hierarchy():
    """Create default hierarchy for Tamil Nadu"""
    
    # Real Tamil Nadu districts (sample)
    tn_districts = [
        "Chennai", "Coimbatore", "Salem", "Madurai", "Tiruchirappalli",
        "Tirunelveli", "Vellore", "Erode", "Thanjavur", "Dindigul"
    ]
    
    districts = []
    blocks = []
    panchayats = []
    
    # Create districts
    for i, district_name in enumerate(tn_districts):
        districts.append({
            'district_id': i + 1,
            'district_name': district_name,
            'coordinates': generate_tamil_nadu_coordinates()
        })
    
    # Create blocks (3-5 per district)
    block_id = 1
    for district in districts:
        num_blocks = np.random.randint(3, 6)
        for j in range(num_blocks):
            blocks.append({
                'district_id': district['district_id'],
                'block_id': block_id,
                'block_name': f"{district['district_name']}_Block_{j+1:02d}",
                'coordinates': generate_tamil_nadu_coordinates()
            })
            block_id += 1
    
    # Create panchayats (5-10 per block)
    panchayat_id = 1
    for block in blocks:
        num_panchayats = np.random.randint(5, 11)
        for k in range(num_panchayats):
            # Find district name
            district_name = None
            for d in districts:
                if d['district_id'] == block['district_id']:
                    district_name = d['district_name']
                    break
            
            panchayats.append({
                'district_id': block['district_id'],
                'block_id': block['block_id'],
                'panchayat_id': panchayat_id,
                'panchayat_name': f"{block['block_name']}_Panchayat_{k+1:02d}",
                'coordinates': generate_tamil_nadu_coordinates()
            })
            panchayat_id += 1
    
    return {'districts': districts, 'blocks': blocks, 'panchayats': panchayats}

def ensure_complete_hierarchy(hierarchy):
    """Ensure all levels of hierarchy are complete"""
    
    # If no districts, create default
    if not hierarchy['districts']:
        hierarchy = create_default_tamil_nadu_hierarchy()
        return hierarchy
    
    # If districts exist but no blocks, create blocks
    if hierarchy['districts'] and not hierarchy['blocks']:
        block_id = 1
        for district in hierarchy['districts']:
            for j in range(3):  # 3 blocks per district
                hierarchy['blocks'].append({
                    'district_id': district['district_id'],
                    'block_id': block_id,
                    'block_name': f"{district['district_name']}_Block_{j+1:02d}",
                    'coordinates': generate_tamil_nadu_coordinates()
                })
                block_id += 1
    
    # If blocks exist but no panchayats, create panchayats
    if hierarchy['blocks'] and not hierarchy['panchayats']:
        panchayat_id = 1
        for block in hierarchy['blocks']:
            for k in range(5):  # 5 panchayats per block
                hierarchy['panchayats'].append({
                    'district_id': block['district_id'],
                    'block_id': block['block_id'],
                    'panchayat_id': panchayat_id,
                    'panchayat_name': f"{block['block_name']}_Panchayat_{k+1:02d}",
                    'coordinates': generate_tamil_nadu_coordinates()
                })
                panchayat_id += 1
    
    return hierarchy

def generate_tamil_nadu_coordinates():
    """Generate coordinates within Tamil Nadu bounds"""
    lat = np.random.uniform(8.0, 13.5)   # Tamil Nadu latitude range
    lon = np.random.uniform(76.0, 80.5)  # Tamil Nadu longitude range
    return (lat, lon)

def generate_enhanced_borrower_data(hierarchy):
    """Generate enhanced borrower data with comprehensive risk factors"""
    
    borrowers = []
    borrower_id = 1
    
    # Enhanced occupations specific to Tamil Nadu
    occupations = [
        'rice_farmer', 'cotton_farmer', 'sugarcane_farmer', 'coconut_farmer',
        'agricultural_laborer', 'dairy_farmer', 'poultry_farmer',
        'textile_worker', 'handloom_weaver', 'small_trader',
        'auto_driver', 'construction_worker', 'domestic_worker',
        'artisan', 'fisherman', 'government_employee', 'private_service'
    ]
    
    # Loan purposes
    loan_purposes = [
        'crop_cultivation', 'livestock_purchase', 'agriculture_equipment',
        'small_business', 'education', 'healthcare', 'home_construction',
        'home_improvement', 'vehicle_purchase', 'emergency', 'marriage'
    ]
    
    for panchayat in hierarchy['panchayats']:
        # Generate 80-200 borrowers per panchayat for realistic density
        num_borrowers = np.random.randint(80, 201)
        
        for _ in range(num_borrowers):
            # Demographic factors
            age = np.random.randint(18, 75)
            gender = random.choice(['Male', 'Female'])
            income = generate_realistic_income(age)
            education = random.choice(['illiterate', 'primary', 'secondary', 'higher_secondary', 'graduate', 'postgraduate'])
            occupation = random.choice(occupations)
            family_size = np.random.randint(2, 8)
            
            # Geographic coordinates near panchayat
            base_lat, base_lon = panchayat['coordinates']
            borrower_lat = base_lat + np.random.normal(0, 0.01)  # Within ~1km
            borrower_lon = base_lon + np.random.normal(0, 0.01)
            
            # Financial factors
            credit_history_months = np.random.randint(0, 120)  # 0-10 years
            existing_loans = np.random.randint(0, 4)
            has_bank_account = random.choice([True, False])
            has_savings_account = random.choice([True, False]) if has_bank_account else False
            monthly_expenses = generate_realistic_expenses(income, family_size)
            
            # Asset ownership
            owns_land = random.choice([True, False])
            land_size_acres = np.random.uniform(0.1, 5.0) if owns_land else 0
            owns_livestock = random.choice([True, False])
            livestock_count = np.random.randint(1, 20) if owns_livestock else 0
            owns_vehicle = random.choice([True, False])
            
            # Infrastructure and geographic factors
            distance_to_bank = np.random.uniform(0.5, 25.0)
            distance_to_market = np.random.uniform(0.2, 30.0)
            road_connectivity = np.random.randint(1, 5)  # 1=poor, 5=excellent
            electricity_access = random.choice([True, False])
            water_source = random.choice(['piped', 'well', 'borewell', 'public_tap', 'river'])
            
            # Behavioral and social factors
            group_membership = random.choice([True, False])  # SHG membership
            government_scheme_beneficiary = random.choice([True, False])
            seasonal_migration = random.choice([True, False])
            mobile_phone_ownership = random.choice([True, False])
            
            # Calculate comprehensive risk scores
            demographic_risk = calculate_demographic_risk(age, income, education, family_size)
            financial_risk = calculate_financial_risk(credit_history_months, existing_loans, has_savings_account, income, monthly_expenses)
            asset_risk = calculate_asset_risk(owns_land, land_size_acres, owns_livestock, livestock_count)
            geographic_risk = calculate_geographic_risk(distance_to_bank, distance_to_market, road_connectivity, electricity_access)
            social_risk = calculate_social_risk(group_membership, government_scheme_beneficiary, mobile_phone_ownership)
            
            # Overall risk with weights
            overall_risk = (
                demographic_risk * 0.20 +
                financial_risk * 0.30 +
                asset_risk * 0.20 +
                geographic_risk * 0.20 +
                social_risk * 0.10
            )
            
            # Loan characteristics based on risk profile
            loan_amount = generate_loan_amount(income, overall_risk, owns_land, owns_livestock)
            loan_purpose = random.choice(loan_purposes)
            
            borrower = {
                # Basic identifiers
                'borrower_id': borrower_id,
                'district_id': panchayat['district_id'],
                'block_id': panchayat['block_id'],
                'panchayat_id': panchayat['panchayat_id'],
                
                # Personal details
                'name': f'Borrower_{borrower_id:05d}',
                'age': age,
                'gender': gender,
                'family_size': family_size,
                'education': education,
                'occupation': occupation,
                
                # Financial details
                'monthly_income': income,
                'monthly_expenses': monthly_expenses,
                'credit_history_months': credit_history_months,
                'existing_loans': existing_loans,
                'has_bank_account': has_bank_account,
                'has_savings_account': has_savings_account,
                
                # Asset ownership
                'owns_land': owns_land,
                'land_size_acres': round(land_size_acres, 2),
                'owns_livestock': owns_livestock,
                'livestock_count': livestock_count,
                'owns_vehicle': owns_vehicle,
                
                # Geographic factors
                'latitude': round(borrower_lat, 6),
                'longitude': round(borrower_lon, 6),
                'distance_to_bank_km': round(distance_to_bank, 1),
                'distance_to_market_km': round(distance_to_market, 1),
                'road_connectivity_score': road_connectivity,
                'has_electricity': electricity_access,
                'water_source': water_source,
                
                # Social factors
                'shg_member': group_membership,
                'govt_scheme_beneficiary': government_scheme_beneficiary,
                'seasonal_migrant': seasonal_migration,
                'owns_mobile_phone': mobile_phone_ownership,
                
                # Risk scores
                'demographic_risk': round(demographic_risk, 4),
                'financial_risk': round(financial_risk, 4),
                'asset_risk': round(asset_risk, 4),
                'geographic_risk': round(geographic_risk, 4),
                'social_risk': round(social_risk, 4),
                'overall_risk_score': round(overall_risk, 4),
                'risk_category': categorize_risk(overall_risk),
                
                # Loan details
                'loan_amount': loan_amount,
                'loan_purpose': loan_purpose
            }
            
            borrowers.append(borrower)
            borrower_id += 1
            
    return borrowers

def generate_realistic_income(age):
    """Generate realistic income based on age"""
    if age < 25:
        return np.random.randint(8000, 25000)
    elif age < 45:
        return np.random.randint(12000, 45000)
    elif age < 60:
        return np.random.randint(10000, 40000)
    else:
        return np.random.randint(5000, 20000)

def generate_realistic_expenses(income, family_size):
    """Generate realistic expenses based on income and family size"""
    base_expenses = income * np.random.uniform(0.6, 0.9)
    family_factor = 1 + (family_size - 2) * 0.1
    return int(base_expenses * family_factor)

def generate_loan_amount(income, risk_score, owns_land, owns_livestock):
    """Generate loan amount based on income and risk profile"""
    base_amount = income * np.random.uniform(3, 8)  # 3-8 months of income
    
    # Adjust based on risk
    risk_factor = 1.5 - risk_score  # Lower risk = higher loan
    
    # Adjust based on collateral
    if owns_land:
        risk_factor *= 1.3
    if owns_livestock:
        risk_factor *= 1.1
    
    loan_amount = int(base_amount * risk_factor)
    return max(5000, min(500000, loan_amount))  # Cap between 5k and 5 lakh

def calculate_demographic_risk(age, income, education, family_size):
    """Calculate demographic risk component"""
    # Age risk (U-shaped curve)
    if 25 <= age <= 50:
        age_risk = 0.1
    elif age < 25 or age > 60:
        age_risk = 0.7
    else:
        age_risk = 0.4
    
    # Income risk
    income_risk = max(0, min(1, (30000 - income) / 30000))
    
    # Education risk
    education_risk_map = {
        'illiterate': 0.8, 'primary': 0.6, 'secondary': 0.4,
        'higher_secondary': 0.3, 'graduate': 0.1, 'postgraduate': 0.05
    }
    education_risk = education_risk_map.get(education, 0.5)
    
    # Family size risk
    family_risk = min(1, max(0, (family_size - 4) * 0.1))
    
    return (age_risk + income_risk + education_risk + family_risk) / 4

def calculate_financial_risk(credit_months, existing_loans, has_savings, income, expenses):
    """Calculate financial risk component"""
    # Credit history risk
    credit_risk = max(0, (24 - credit_months) / 24) if credit_months < 24 else 0.1
    
    # Existing loan burden
    loan_risk = min(1, existing_loans / 3)
    
    # Savings risk
    savings_risk = 0.2 if has_savings else 0.6
    
    # Income-expense ratio risk
    expense_ratio = expenses / income
    expense_risk = max(0, min(1, (expense_ratio - 0.5) / 0.3))
    
    return (credit_risk + loan_risk + savings_risk + expense_risk) / 4

def calculate_asset_risk(owns_land, land_size, owns_livestock, livestock_count):
    """Calculate asset-based risk component"""
    # Land ownership risk
    if owns_land:
        land_risk = max(0, (2 - land_size) / 2)  # Risk decreases with land size
    else:
        land_risk = 0.8
    
    # Livestock risk
    if owns_livestock:
        livestock_risk = max(0, (5 - livestock_count) / 5)
    else:
        livestock_risk = 0.6
    
    return (land_risk + livestock_risk) / 2

def calculate_geographic_risk(bank_distance, market_distance, road_score, has_electricity):
    """Calculate geographic risk component"""
    # Distance risks
    bank_risk = min(1, bank_distance / 20)
    market_risk = min(1, market_distance / 25)
    
    # Infrastructure risks
    road_risk = (5 - road_score) / 4
    electricity_risk = 0.2 if has_electricity else 0.6
    
    return (bank_risk + market_risk + road_risk + electricity_risk) / 4

def calculate_social_risk(shg_member, govt_beneficiary, mobile_phone):
    """Calculate social risk component"""
    shg_risk = 0.2 if shg_member else 0.6
    govt_risk = 0.3 if govt_beneficiary else 0.5
    mobile_risk = 0.1 if mobile_phone else 0.7
    
    return (shg_risk + govt_risk + mobile_risk) / 3

def categorize_risk(score):
    """Categorize risk score into levels"""
    if score <= 0.2:
        return "Very Low"
    elif score <= 0.4:
        return "Low"
    elif score <= 0.6:
        return "Medium"
    elif score <= 0.8:
        return "High"
    else:
        return "Very High"

def create_aggregations(borrowers_df):
    """Create administrative level aggregations"""
    
    aggregations = {}
    
    # Panchayat level aggregation
    panchayat_agg = borrowers_df.groupby(['district_id', 'block_id', 'panchayat_id']).agg({
        'overall_risk_score': ['mean', 'std', 'min', 'max'],
        'demographic_risk': 'mean',
        'financial_risk': 'mean',
        'asset_risk': 'mean',
        'geographic_risk': 'mean',
        'social_risk': 'mean',
        'borrower_id': 'count',
        'loan_amount': 'sum',
        'monthly_income': 'mean',
        'land_size_acres': 'mean',
        'distance_to_bank_km': 'mean'
    }).round(4)
    
    panchayat_agg.columns = [
        'avg_risk_score', 'risk_score_std', 'min_risk_score', 'max_risk_score',
        'avg_demographic_risk', 'avg_financial_risk', 'avg_asset_risk', 'avg_geographic_risk', 'avg_social_risk',
        'num_borrowers', 'total_loan_volume', 'avg_income', 'avg_land_size', 'avg_bank_distance'
    ]
    panchayat_agg = panchayat_agg.reset_index()
    panchayat_agg['risk_level'] = panchayat_agg['avg_risk_score'].apply(categorize_risk)
    aggregations['panchayat'] = panchayat_agg
    
    # Block level aggregation
    block_agg = borrowers_df.groupby(['district_id', 'block_id']).agg({
        'overall_risk_score': ['mean', 'std', 'min', 'max'],
        'demographic_risk': 'mean',
        'financial_risk': 'mean',
        'asset_risk': 'mean',
        'geographic_risk': 'mean',
        'social_risk': 'mean',
        'borrower_id': 'count',
        'loan_amount': 'sum',
        'monthly_income': 'mean'
    }).round(4)
    
    block_agg.columns = [
        'avg_risk_score', 'risk_score_std', 'min_risk_score', 'max_risk_score',
        'avg_demographic_risk', 'avg_financial_risk', 'avg_asset_risk', 'avg_geographic_risk', 'avg_social_risk',
        'num_borrowers', 'total_loan_volume', 'avg_income'
    ]
    block_agg = block_agg.reset_index()
    block_agg['risk_level'] = block_agg['avg_risk_score'].apply(categorize_risk)
    aggregations['block'] = block_agg
    
    # District level aggregation
    district_agg = borrowers_df.groupby('district_id').agg({
        'overall_risk_score': ['mean', 'std', 'min', 'max'],
        'demographic_risk': 'mean',
        'financial_risk': 'mean',
        'asset_risk': 'mean',
        'geographic_risk': 'mean',
        'social_risk': 'mean',
        'borrower_id': 'count',
        'loan_amount': 'sum',
        'monthly_income': 'mean'
    }).round(4)
    
    district_agg.columns = [
        'avg_risk_score', 'risk_score_std', 'min_risk_score', 'max_risk_score',
        'avg_demographic_risk', 'avg_financial_risk', 'avg_asset_risk', 'avg_geographic_risk', 'avg_social_risk',
        'num_borrowers', 'total_loan_volume', 'avg_income'
    ]
    district_agg = district_agg.reset_index()
    district_agg['risk_level'] = district_agg['avg_risk_score'].apply(categorize_risk)
    aggregations['district'] = district_agg
    
    return aggregations

def main():
    """Main function to generate enhanced data using Excel input"""
    
    print("🏦 ENHANCED MICRO-LENDING DATA GENERATOR WITH EXCEL INTEGRATION")
    print("=" * 70)
    
    # Create directories
    os.makedirs('data', exist_ok=True)
    os.makedirs('results', exist_ok=True)
    
    # Load Excel data
    excel_data = load_excel_data()
    
    # Create geographic hierarchy
    print(f"\n🗺️  Creating geographic hierarchy...")
    hierarchy = extract_geographic_hierarchy(excel_data)
    
    print(f"✅ Geographic hierarchy created:")
    print(f"   • Districts: {len(hierarchy['districts'])}")
    print(f"   • Blocks: {len(hierarchy['blocks'])}")
    print(f"   • Panchayats: {len(hierarchy['panchayats'])}")
    
    # Save hierarchy data
    for level, data in hierarchy.items():
        df = pd.DataFrame(data)
        df.to_csv(f'data/{level}.csv', index=False)
        print(f"✅ Saved data/{level}.csv")
    
    # Generate borrower data
    print(f"\n👥 Generating enhanced borrower data...")
    borrowers = generate_enhanced_borrower_data(hierarchy)
    borrowers_df = pd.DataFrame(borrowers)
    
    # Save borrower data
    borrowers_df.to_csv('data/borrowers_enhanced.csv', index=False)
    borrowers_df.to_csv('results/individual_risk_scores.csv', index=False)
    print(f"✅ Generated {len(borrowers_df):,} borrower records")
    
    # Create aggregations
    print(f"\n📊 Creating administrative level aggregations...")
    aggregations = create_aggregations(borrowers_df)
    
    for level, agg_df in aggregations.items():
        agg_df.to_csv(f'results/{level}_risk_aggregation.csv', index=False)
        print(f"✅ Saved results/{level}_risk_aggregation.csv")
    
    # Print comprehensive summary
    print(f"\n📈 ENHANCED DATA SUMMARY:")
    print(f"   • Total borrowers: {len(borrowers_df):,}")
    print(f"   • Total districts: {len(hierarchy['districts'])}")
    print(f"   • Total blocks: {len(hierarchy['blocks'])}")
    print(f"   • Total panchayats: {len(hierarchy['panchayats'])}")
    print(f"   • Average risk score: {borrowers_df['overall_risk_score'].mean():.4f}")
    print(f"   • Total loan volume: ₹{borrowers_df['loan_amount'].sum()/1e6:.1f}M")
    print(f"   • Average loan amount: ₹{borrowers_df['loan_amount'].mean():,.0f}")
    
    print(f"\n🎯 Risk Distribution:")
    risk_dist = borrowers_df['risk_category'].value_counts(normalize=True).sort_index()
    for category, percentage in risk_dist.items():
        print(f"   • {category}: {percentage:.1%}")
    
    print(f"\n🏞️  Geographic Coverage:")
    print(f"   • Latitude range: {borrowers_df['latitude'].min():.2f} to {borrowers_df['latitude'].max():.2f}")
    print(f"   • Longitude range: {borrowers_df['longitude'].min():.2f} to {borrowers_df['longitude'].max():.2f}")
    
    print(f"\n💰 Financial Profile:")
    print(f"   • Income range: ₹{borrowers_df['monthly_income'].min():,} to ₹{borrowers_df['monthly_income'].max():,}")
    print(f"   • Loan amount range: ₹{borrowers_df['loan_amount'].min():,} to ₹{borrowers_df['loan_amount'].max():,}")
    
    print(f"\n🎉 Enhanced data generation completed successfully!")
    print(f"\n🚀 Next steps:")
    print(f"   1. Launch enhanced dashboard: streamlit run simple_dashboard.py")
    print(f"   2. Analyze data: python demo.py")
    print(f"   3. Explore in Jupyter: jupyter lab notebooks/risk_analysis.ipynb")
    
    return borrowers_df, hierarchy, aggregations

if __name__ == "__main__":
    main()
