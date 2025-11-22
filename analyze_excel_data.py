"""
Excel Data Reader and Analyzer for Block/Panchayat Level Data
"""
import pandas as pd
import numpy as np
import os

def read_excel_data():
    """Read and analyze the input Excel file"""
    
    excel_path = "input_excel/input_data.xlsx"
    
    if not os.path.exists(excel_path):
        print(f"❌ Excel file not found at {excel_path}")
        return None
    
    try:
        # Read all sheets in the Excel file
        excel_file = pd.ExcelFile(excel_path)
        print(f"📊 Excel file sheets: {excel_file.sheet_names}")
        
        # Read each sheet
        sheets_data = {}
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(excel_path, sheet_name=sheet_name)
            sheets_data[sheet_name] = df
            print(f"\n📋 Sheet '{sheet_name}':")
            print(f"  • Shape: {df.shape}")
            print(f"  • Columns: {list(df.columns)}")
            print(f"  • Data types: {df.dtypes.to_dict()}")
            
            # Display first few rows
            print(f"  • Sample data:")
            print(df.head().to_string(index=False))
            
            # Check for missing values
            missing_data = df.isnull().sum()
            if missing_data.any():
                print(f"  • Missing values: {missing_data[missing_data > 0].to_dict()}")
        
        return sheets_data
        
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")
        return None

def analyze_geographic_data(sheets_data):
    """Analyze geographic structure in the data"""
    
    if not sheets_data:
        return None
    
    print(f"\n🗺️ GEOGRAPHIC DATA ANALYSIS")
    print("=" * 40)
    
    geographic_info = {}
    
    for sheet_name, df in sheets_data.items():
        print(f"\nAnalyzing sheet: {sheet_name}")
        
        # Look for geographic columns
        geo_columns = []
        for col in df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in ['district', 'block', 'panchayat', 'village', 'taluk', 'mandal', 'state']):
                geo_columns.append(col)
        
        print(f"  • Geographic columns found: {geo_columns}")
        
        if geo_columns:
            for col in geo_columns:
                unique_values = df[col].unique()
                print(f"  • {col}: {len(unique_values)} unique values")
                if len(unique_values) <= 20:  # Show values if not too many
                    print(f"    Values: {list(unique_values)}")
        
        geographic_info[sheet_name] = {
            'columns': list(df.columns),
            'geo_columns': geo_columns,
            'shape': df.shape
        }
    
    return geographic_info

def create_enhanced_data_generator(sheets_data):
    """Create enhanced data generator using Excel input"""
    
    if not sheets_data:
        print("❌ No Excel data available")
        return
    
    print(f"\n🔧 CREATING ENHANCED DATA GENERATOR")
    print("=" * 40)
    
    # Create enhanced data generation script
    generator_code = '''"""
Enhanced Data Generator using Excel input data for Block/Panchayat level simulation
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

def load_excel_reference_data():
    """Load reference data from Excel file"""
    excel_path = "input_excel/input_data.xlsx"
    
    if not os.path.exists(excel_path):
        print("⚠️  Excel file not found, using default data")
        return None
    
    try:
        # Read all sheets
        excel_data = {}
        excel_file = pd.ExcelFile(excel_path)
        
        for sheet_name in excel_file.sheet_names:
            excel_data[sheet_name] = pd.read_excel(excel_path, sheet_name=sheet_name)
            print(f"✅ Loaded sheet: {sheet_name}")
        
        return excel_data
    except Exception as e:
        print(f"❌ Error loading Excel data: {e}")
        return None

def extract_geographic_hierarchy(excel_data):
    """Extract district/block/panchayat hierarchy from Excel data"""
    
    hierarchy = {
        'districts': [],
        'blocks': [],
        'panchayats': []
    }
    
    if not excel_data:
        return create_default_hierarchy()
    
    # Try to extract from first sheet
    main_sheet = list(excel_data.values())[0]
    
    # Look for geographic columns
    geo_mapping = {}
    for col in main_sheet.columns:
        col_lower = col.lower()
        if 'district' in col_lower:
            geo_mapping['district'] = col
        elif any(keyword in col_lower for keyword in ['block', 'taluk', 'mandal']):
            geo_mapping['block'] = col
        elif any(keyword in col_lower for keyword in ['panchayat', 'village', 'gram']):
            geo_mapping['panchayat'] = col
    
    print(f"📍 Geographic mapping found: {geo_mapping}")
    
    if geo_mapping:
        # Extract unique values
        district_col = geo_mapping.get('district')
        block_col = geo_mapping.get('block')
        panchayat_col = geo_mapping.get('panchayat')
        
        if district_col:
            unique_districts = main_sheet[district_col].dropna().unique()
            for i, district in enumerate(unique_districts):
                hierarchy['districts'].append({
                    'district_id': i + 1,
                    'district_name': str(district),
                    'coordinates': generate_tamil_nadu_coordinates()
                })
        
        if block_col:
            unique_blocks = main_sheet[block_col].dropna().unique()
            for i, block in enumerate(unique_blocks):
                # Assign to districts cyclically
                district_id = (i % len(hierarchy['districts'])) + 1 if hierarchy['districts'] else 1
                hierarchy['blocks'].append({
                    'district_id': district_id,
                    'block_id': i + 1,
                    'block_name': str(block),
                    'coordinates': generate_tamil_nadu_coordinates()
                })
        
        if panchayat_col:
            unique_panchayats = main_sheet[panchayat_col].dropna().unique()
            for i, panchayat in enumerate(unique_panchayats):
                # Assign to blocks cyclically
                block_id = (i % len(hierarchy['blocks'])) + 1 if hierarchy['blocks'] else 1
                district_id = hierarchy['blocks'][block_id - 1]['district_id'] if hierarchy['blocks'] else 1
                hierarchy['panchayats'].append({
                    'district_id': district_id,
                    'block_id': block_id,
                    'panchayat_id': i + 1,
                    'panchayat_name': str(panchayat),
                    'coordinates': generate_tamil_nadu_coordinates()
                })
    
    # Fill in missing levels if needed
    if not hierarchy['districts']:
        hierarchy = create_default_hierarchy()
    elif not hierarchy['blocks']:
        hierarchy = fill_missing_blocks(hierarchy)
    elif not hierarchy['panchayats']:
        hierarchy = fill_missing_panchayats(hierarchy)
    
    return hierarchy

def generate_tamil_nadu_coordinates():
    """Generate random coordinates within Tamil Nadu bounds"""
    lat = np.random.uniform(8.0, 13.5)  # Tamil Nadu latitude range
    lon = np.random.uniform(76.0, 80.5)  # Tamil Nadu longitude range
    return (lat, lon)

def create_default_hierarchy():
    """Create default hierarchy if Excel data is not available"""
    districts = []
    blocks = []
    panchayats = []
    
    # Create 10 districts
    for i in range(1, 11):
        districts.append({
            'district_id': i,
            'district_name': f'District_{i:02d}',
            'coordinates': generate_tamil_nadu_coordinates()
        })
    
    # Create 3 blocks per district
    block_id = 1
    for district in districts:
        for j in range(1, 4):
            blocks.append({
                'district_id': district['district_id'],
                'block_id': block_id,
                'block_name': f'Block_{district["district_id"]:02d}_{j:02d}',
                'coordinates': generate_tamil_nadu_coordinates()
            })
            block_id += 1
    
    # Create 5 panchayats per block
    panchayat_id = 1
    for block in blocks:
        for k in range(1, 6):
            panchayats.append({
                'district_id': block['district_id'],
                'block_id': block['block_id'],
                'panchayat_id': panchayat_id,
                'panchayat_name': f'Panchayat_{block["district_id"]:02d}_{block["block_id"]:02d}_{k:02d}',
                'coordinates': generate_tamil_nadu_coordinates()
            })
            panchayat_id += 1
    
    return {'districts': districts, 'blocks': blocks, 'panchayats': panchayats}

def fill_missing_blocks(hierarchy):
    """Fill missing blocks for existing districts"""
    blocks = []
    block_id = 1
    
    for district in hierarchy['districts']:
        for j in range(1, 4):
            blocks.append({
                'district_id': district['district_id'],
                'block_id': block_id,
                'block_name': f'{district["district_name"]}_Block_{j:02d}',
                'coordinates': generate_tamil_nadu_coordinates()
            })
            block_id += 1
    
    hierarchy['blocks'] = blocks
    return hierarchy

def fill_missing_panchayats(hierarchy):
    """Fill missing panchayats for existing blocks"""
    panchayats = []
    panchayat_id = 1
    
    for block in hierarchy['blocks']:
        for k in range(1, 6):
            panchayats.append({
                'district_id': block['district_id'],
                'block_id': block['block_id'],
                'panchayat_id': panchayat_id,
                'panchayat_name': f'{block["block_name"]}_Panchayat_{k:02d}',
                'coordinates': generate_tamil_nadu_coordinates()
            })
            panchayat_id += 1
    
    hierarchy['panchayats'] = panchayats
    return hierarchy

def generate_enhanced_borrower_data(hierarchy, excel_data):
    """Generate enhanced borrower data using Excel reference"""
    
    borrowers = []
    borrower_id = 1
    
    # Extract additional factors from Excel if available
    additional_factors = extract_additional_factors(excel_data)
    
    for panchayat in hierarchy['panchayats']:
        # Generate 50-150 borrowers per panchayat
        num_borrowers = np.random.randint(50, 151)
        
        for _ in range(num_borrowers):
            # Enhanced borrower profile
            age = np.random.randint(18, 70)
            income = np.random.randint(8000, 200000)
            education = random.choice(['none', 'primary', 'secondary', 'higher_secondary', 'graduate'])
            occupation = random.choice(['farmer', 'agricultural_laborer', 'daily_wage', 'small_business', 
                                     'service', 'artisan', 'livestock', 'fishery'])
            
            # Geographic coordinates near panchayat
            base_lat, base_lon = panchayat['coordinates']
            borrower_lat = base_lat + np.random.normal(0, 0.02)
            borrower_lon = base_lon + np.random.normal(0, 0.02)
            
            # Enhanced risk factors
            credit_history_score = np.random.uniform(0, 10)
            existing_loans = np.random.randint(0, 4)
            has_savings = random.choice([True, False])
            monthly_expenses = np.random.randint(4000, int(income * 0.8))
            
            # Additional Excel-based factors
            market_distance = np.random.uniform(1, 50)
            infrastructure_access = np.random.randint(1, 10)
            seasonal_income_variation = np.random.uniform(0.1, 0.8)
            
            # Calculate comprehensive risk score
            demographic_risk = calculate_demographic_risk(age, income, education, occupation)
            financial_risk = calculate_financial_risk(credit_history_score, existing_loans, has_savings, income, monthly_expenses)
            geographic_risk = calculate_geographic_risk(market_distance, infrastructure_access)
            behavioral_risk = calculate_behavioral_risk(seasonal_income_variation)
            
            overall_risk = (demographic_risk * 0.25 + financial_risk * 0.35 + 
                          geographic_risk * 0.20 + behavioral_risk * 0.20)
            
            borrower = {
                'borrower_id': borrower_id,
                'district_id': panchayat['district_id'],
                'block_id': panchayat['block_id'],
                'panchayat_id': panchayat['panchayat_id'],
                'name': f'Borrower_{borrower_id:05d}',
                'age': age,
                'gender': random.choice(['Male', 'Female']),
                'income': income,
                'education': education,
                'occupation': occupation,
                'credit_history_score': round(credit_history_score, 2),
                'existing_loans': existing_loans,
                'has_savings_account': has_savings,
                'monthly_expenses': monthly_expenses,
                'market_distance_km': round(market_distance, 1),
                'infrastructure_access_score': infrastructure_access,
                'seasonal_variation': round(seasonal_income_variation, 2),
                'latitude': round(borrower_lat, 6),
                'longitude': round(borrower_lon, 6),
                'demographic_risk': round(demographic_risk, 4),
                'financial_risk': round(financial_risk, 4),
                'geographic_risk': round(geographic_risk, 4),
                'behavioral_risk': round(behavioral_risk, 4),
                'overall_risk_score': round(overall_risk, 4),
                'risk_category': categorize_risk(overall_risk),
                'total_loan_amount': np.random.randint(5000, 150000),
                'loan_purpose': random.choice(['agriculture', 'livestock', 'small_business', 'education', 
                                             'healthcare', 'home_improvement', 'emergency'])
            }
            borrowers.append(borrower)
            borrower_id += 1
    
    return borrowers

def extract_additional_factors(excel_data):
    """Extract additional risk factors from Excel data"""
    factors = {}
    
    if excel_data:
        # Look for numerical columns that could be risk factors
        main_sheet = list(excel_data.values())[0]
        
        for col in main_sheet.columns:
            if main_sheet[col].dtype in ['int64', 'float64']:
                factors[col] = main_sheet[col].describe().to_dict()
    
    return factors

def calculate_demographic_risk(age, income, education, occupation):
    """Calculate demographic risk component"""
    age_risk = 0.3 if age < 25 or age > 55 else 0.1
    income_risk = max(0, 1 - income / 150000)
    education_risk = {'none': 0.8, 'primary': 0.6, 'secondary': 0.4, 'higher_secondary': 0.3, 'graduate': 0.1}[education]
    occupation_risk = {'farmer': 0.4, 'agricultural_laborer': 0.7, 'daily_wage': 0.8, 'small_business': 0.5,
                      'service': 0.2, 'artisan': 0.6, 'livestock': 0.5, 'fishery': 0.6}.get(occupation, 0.5)
    
    return (age_risk + income_risk + education_risk + occupation_risk) / 4

def calculate_financial_risk(credit_score, existing_loans, has_savings, income, expenses):
    """Calculate financial risk component"""
    credit_risk = max(0, 1 - credit_score / 10)
    loan_burden_risk = min(1, existing_loans / 3)
    savings_risk = 0.2 if has_savings else 0.7
    expense_ratio_risk = max(0, min(1, expenses / income))
    
    return (credit_risk + loan_burden_risk + savings_risk + expense_ratio_risk) / 4

def calculate_geographic_risk(market_distance, infrastructure_score):
    """Calculate geographic risk component"""
    distance_risk = min(1, market_distance / 30)
    infrastructure_risk = max(0, 1 - infrastructure_score / 10)
    
    return (distance_risk + infrastructure_risk) / 2

def calculate_behavioral_risk(seasonal_variation):
    """Calculate behavioral risk component"""
    return seasonal_variation

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

def aggregate_by_administrative_levels(borrowers_df):
    """Aggregate risk data by district, block, and panchayat levels"""
    
    aggregations = {}
    
    # Panchayat level
    panchayat_agg = borrowers_df.groupby(['district_id', 'block_id', 'panchayat_id']).agg({
        'overall_risk_score': ['mean', 'std', 'min', 'max'],
        'demographic_risk': 'mean',
        'financial_risk': 'mean',
        'geographic_risk': 'mean',
        'behavioral_risk': 'mean',
        'borrower_id': 'count',
        'total_loan_amount': 'sum',
        'income': 'mean',
        'market_distance_km': 'mean'
    }).round(4)
    
    panchayat_agg.columns = [
        'avg_risk_score', 'risk_score_std', 'min_risk_score', 'max_risk_score',
        'avg_demographic_risk', 'avg_financial_risk', 'avg_geographic_risk', 'avg_behavioral_risk',
        'num_borrowers', 'total_loan_volume', 'avg_income', 'avg_market_distance'
    ]
    panchayat_agg = panchayat_agg.reset_index()
    panchayat_agg['risk_level'] = panchayat_agg['avg_risk_score'].apply(categorize_risk)
    aggregations['panchayat'] = panchayat_agg
    
    # Block level
    block_agg = borrowers_df.groupby(['district_id', 'block_id']).agg({
        'overall_risk_score': ['mean', 'std', 'min', 'max'],
        'demographic_risk': 'mean',
        'financial_risk': 'mean',
        'geographic_risk': 'mean',
        'behavioral_risk': 'mean',
        'borrower_id': 'count',
        'total_loan_amount': 'sum',
        'income': 'mean'
    }).round(4)
    
    block_agg.columns = [
        'avg_risk_score', 'risk_score_std', 'min_risk_score', 'max_risk_score',
        'avg_demographic_risk', 'avg_financial_risk', 'avg_geographic_risk', 'avg_behavioral_risk',
        'num_borrowers', 'total_loan_volume', 'avg_income'
    ]
    block_agg = block_agg.reset_index()
    block_agg['risk_level'] = block_agg['avg_risk_score'].apply(categorize_risk)
    aggregations['block'] = block_agg
    
    # District level
    district_agg = borrowers_df.groupby('district_id').agg({
        'overall_risk_score': ['mean', 'std', 'min', 'max'],
        'demographic_risk': 'mean',
        'financial_risk': 'mean',
        'geographic_risk': 'mean',
        'behavioral_risk': 'mean',
        'borrower_id': 'count',
        'total_loan_amount': 'sum',
        'income': 'mean'
    }).round(4)
    
    district_agg.columns = [
        'avg_risk_score', 'risk_score_std', 'min_risk_score', 'max_risk_score',
        'avg_demographic_risk', 'avg_financial_risk', 'avg_geographic_risk', 'avg_behavioral_risk',
        'num_borrowers', 'total_loan_volume', 'avg_income'
    ]
    district_agg = district_agg.reset_index()
    district_agg['risk_level'] = district_agg['avg_risk_score'].apply(categorize_risk)
    aggregations['district'] = district_agg
    
    return aggregations

def main():
    """Main function to generate enhanced data"""
    
    print("🏦 ENHANCED MICRO-LENDING DATA GENERATOR")
    print("=" * 50)
    
    # Create directories
    os.makedirs('data', exist_ok=True)
    os.makedirs('results', exist_ok=True)
    
    # Load Excel reference data
    print("\\n📊 Loading Excel reference data...")
    excel_data = load_excel_reference_data()
    
    # Extract geographic hierarchy
    print("\\n🗺️ Extracting geographic hierarchy...")
    hierarchy = extract_geographic_hierarchy(excel_data)
    
    print(f"  • Districts: {len(hierarchy['districts'])}")
    print(f"  • Blocks: {len(hierarchy['blocks'])}")
    print(f"  • Panchayats: {len(hierarchy['panchayats'])}")
    
    # Save hierarchy data
    for level, data in hierarchy.items():
        df = pd.DataFrame(data)
        df.to_csv(f'data/{level}.csv', index=False)
        print(f"✅ Saved {level}.csv with {len(df)} records")
    
    # Generate enhanced borrower data
    print("\\n👥 Generating enhanced borrower data...")
    borrowers = generate_enhanced_borrower_data(hierarchy, excel_data)
    borrowers_df = pd.DataFrame(borrowers)
    
    # Save borrower data
    borrowers_df.to_csv('data/borrowers_enhanced.csv', index=False)
    borrowers_df.to_csv('results/individual_risk_scores.csv', index=False)
    print(f"✅ Generated {len(borrowers_df):,} borrower records")
    
    # Generate aggregations
    print("\\n📈 Creating administrative level aggregations...")
    aggregations = aggregate_by_administrative_levels(borrowers_df)
    
    for level, agg_df in aggregations.items():
        agg_df.to_csv(f'results/{level}_risk_aggregation.csv', index=False)
        print(f"✅ Saved {level}_risk_aggregation.csv with {len(agg_df)} records")
    
    # Print summary
    print(f"\\n🎯 ENHANCED DATA SUMMARY:")
    print(f"  • Total borrowers: {len(borrowers_df):,}")
    print(f"  • Districts: {len(hierarchy['districts'])}")
    print(f"  • Blocks: {len(hierarchy['blocks'])}")
    print(f"  • Panchayats: {len(hierarchy['panchayats'])}")
    print(f"  • Average risk score: {borrowers_df['overall_risk_score'].mean():.4f}")
    print(f"  • Total loan volume: ₹{borrowers_df['total_loan_amount'].sum()/1e6:.1f}M")
    
    print(f"\\n📊 Risk Distribution:")
    risk_dist = borrowers_df['risk_category'].value_counts(normalize=True)
    for category, percentage in risk_dist.items():
        print(f"  • {category}: {percentage:.1%}")
    
    print(f"\\n🎉 Enhanced data generation completed!")
    return borrowers_df, hierarchy, aggregations

if __name__ == "__main__":
    main()
'''
    
    # Save the enhanced generator
    with open('generate_enhanced_data.py', 'w') as f:
        f.write(generator_code)
    
    print(f"✅ Created enhanced data generator: generate_enhanced_data.py")

def main():
    """Main analysis function"""
    
    print("📊 EXCEL DATA INTEGRATION FOR BLOCK/PANCHAYAT ANALYSIS")
    print("=" * 60)
    
    # Read Excel data
    sheets_data = read_excel_data()
    
    if sheets_data:
        # Analyze geographic structure
        geographic_info = analyze_geographic_data(sheets_data)
        
        # Create enhanced data generator
        create_enhanced_data_generator(sheets_data)
        
        print(f"\\n🚀 NEXT STEPS:")
        print(f"  1. Run enhanced data generator: python generate_enhanced_data.py")
        print(f"  2. Launch enhanced dashboard: streamlit run simple_dashboard.py")
        print(f"  3. Analyze results: python demo.py")
    else:
        print("❌ Could not analyze Excel data. Please check the file.")

if __name__ == "__main__":
    main()
'''
