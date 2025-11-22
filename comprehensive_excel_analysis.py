#!/usr/bin/env python3
"""
Comprehensive Excel Integration and Analysis Script
Analyzes Excel input data and integrates it with micro-lending risk assessment
"""

import pandas as pd
import numpy as np
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def analyze_excel_structure():
    """Analyze the structure of the Excel input file"""
    
    excel_path = "input_excel/input_data.xlsx"
    
    print("🔍 EXCEL DATA ANALYSIS")
    print("=" * 50)
    
    if not os.path.exists(excel_path):
        print(f"❌ Excel file not found at: {excel_path}")
        print("📊 Creating sample Excel structure for demonstration...")
        
        # Create sample Excel data for demonstration
        sample_data = {
            'District': ['Chennai', 'Coimbatore', 'Madurai', 'Salem', 'Tiruchirappalli'] * 20,
            'Block': [f'Block-{i}' for i in range(1, 101)],
            'Panchayat': [f'Panchayat-{i}' for i in range(1, 101)],
            'Population': np.random.randint(1000, 50000, 100),
            'Literacy_Rate': np.random.uniform(0.6, 0.9, 100),
            'Banking_Penetration': np.random.uniform(0.3, 0.8, 100),
            'Agriculture_Percentage': np.random.uniform(0.2, 0.8, 100),
            'Infrastructure_Score': np.random.randint(1, 10, 100)
        }
        
        df = pd.DataFrame(sample_data)
        os.makedirs('input_excel', exist_ok=True)
        df.to_excel(excel_path, index=False)
        print(f"✅ Created sample Excel file with {len(df)} records")
        
        return df
    
    else:
        try:
            # Read Excel file
            excel_file = pd.ExcelFile(excel_path)
            print(f"📊 Excel file found with sheets: {excel_file.sheet_names}")
            
            # Read the first sheet
            df = pd.read_excel(excel_path, sheet_name=0)
            print(f"📋 Loaded sheet with shape: {df.shape}")
            
            # Display column information
            print(f"\n📝 Column Information:")
            for i, col in enumerate(df.columns):
                dtype = df[col].dtype
                null_count = df[col].isnull().sum()
                unique_count = df[col].nunique()
                print(f"  {i+1:2d}. {col:20s} | Type: {dtype:10s} | Nulls: {null_count:3d} | Unique: {unique_count:4d}")
            
            # Display sample data
            print(f"\n🔍 Sample Data (first 5 rows):")
            print(df.head().to_string(index=False))
            
            return df
            
        except Exception as e:
            print(f"❌ Error reading Excel file: {e}")
            return None

def analyze_existing_data():
    """Analyze existing generated data"""
    
    print("\n🗂️ EXISTING DATA ANALYSIS")
    print("=" * 50)
    
    data_files = {
        'borrowers': 'data/borrowers.csv',
        'districts': 'data/districts.csv',
        'blocks': 'data/blocks.csv',
        'panchayats': 'data/panchayats.csv'
    }
    
    data_summary = {}
    
    for name, file_path in data_files.items():
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                data_summary[name] = {
                    'shape': df.shape,
                    'columns': list(df.columns),
                    'sample': df.head(2).to_dict('records') if len(df) > 0 else []
                }
                print(f"✅ {name:12s}: {df.shape[0]:5d} rows, {df.shape[1]:2d} columns")
            except Exception as e:
                print(f"❌ Error loading {name}: {e}")
                data_summary[name] = None
        else:
            print(f"❌ {name:12s}: File not found")
            data_summary[name] = None
    
    return data_summary

def generate_enhanced_risk_analysis():
    """Generate enhanced risk analysis combining Excel and existing data"""
    
    print("\n📊 ENHANCED RISK ANALYSIS")
    print("=" * 50)
    
    # Load borrower data
    borrowers_path = 'data/borrowers.csv'
    if not os.path.exists(borrowers_path):
        print("❌ Borrower data not found")
        return
    
    borrowers_df = pd.read_csv(borrowers_path)
    print(f"📋 Loaded {len(borrowers_df)} borrower records")
    
    # Risk category analysis
    if 'risk_category' in borrowers_df.columns:
        risk_dist = borrowers_df['risk_category'].value_counts()
        print(f"\n🎯 Risk Distribution:")
        for category, count in risk_dist.items():
            percentage = (count / len(borrowers_df)) * 100
            print(f"  {category:15s}: {count:4d} ({percentage:5.1f}%)")
    
    # Geographic risk analysis
    if 'district_id' in borrowers_df.columns and 'overall_risk_score' in borrowers_df.columns:
        district_risk = borrowers_df.groupby('district_id').agg({
            'overall_risk_score': ['mean', 'std', 'count']
        }).round(3)
        
        district_risk.columns = ['avg_risk', 'risk_std', 'borrower_count']
        district_risk = district_risk.reset_index().sort_values('avg_risk', ascending=False)
        
        print(f"\n🌍 District-wise Risk Analysis:")
        print(district_risk.to_string(index=False))
    
    # Financial analysis
    if all(col in borrowers_df.columns for col in ['income', 'total_loan_amount', 'overall_risk_score']):
        # Income vs Risk correlation
        income_risk_corr = borrowers_df['income'].corr(borrowers_df['overall_risk_score'])
        loan_risk_corr = borrowers_df['total_loan_amount'].corr(borrowers_df['overall_risk_score'])
        
        print(f"\n💰 Financial Correlations:")
        print(f"  Income vs Risk:     {income_risk_corr:7.3f}")
        print(f"  Loan Amount vs Risk: {loan_risk_corr:7.3f}")
        
        # Risk by income quartiles
        borrowers_df['income_quartile'] = pd.qcut(borrowers_df['income'], 4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
        quartile_risk = borrowers_df.groupby('income_quartile')['overall_risk_score'].mean()
        
        print(f"\n📊 Risk by Income Quartile:")
        for quartile, avg_risk in quartile_risk.items():
            print(f"  {quartile}: {avg_risk:.3f}")

def create_integration_recommendations():
    """Create recommendations for Excel data integration"""
    
    print("\n💡 INTEGRATION RECOMMENDATIONS")
    print("=" * 50)
    
    recommendations = [
        {
            "category": "Data Structure",
            "recommendations": [
                "Ensure Excel data includes District, Block, and Panchayat columns",
                "Add population and demographic data for each administrative unit",
                "Include infrastructure scores and banking penetration rates",
                "Maintain consistent naming conventions across all levels"
            ]
        },
        {
            "category": "Risk Enhancement",
            "recommendations": [
                "Add literacy rates and education infrastructure data",
                "Include seasonal employment patterns and migration data",
                "Add market access and transportation infrastructure scores",
                "Include weather and climate risk indicators"
            ]
        },
        {
            "category": "Financial Inclusion",
            "recommendations": [
                "Add bank branch density and ATM coverage data",
                "Include mobile network coverage and digital literacy rates",
                "Add SHG (Self Help Group) penetration and activity data",
                "Include government scheme participation rates"
            ]
        },
        {
            "category": "Technical Implementation",
            "recommendations": [
                "Use standardized column names for geographic hierarchy",
                "Implement data validation rules for consistency",
                "Create automated data refresh pipelines",
                "Add data quality monitoring and alerts"
            ]
        }
    ]
    
    for rec_group in recommendations:
        print(f"\n🎯 {rec_group['category']}:")
        for i, rec in enumerate(rec_group['recommendations'], 1):
            print(f"  {i}. {rec}")

def create_excel_template():
    """Create an Excel template for data input"""
    
    print("\n📋 CREATING EXCEL TEMPLATE")
    print("=" * 50)
    
    # Create comprehensive template
    template_data = {
        'District': ['Chennai', 'Coimbatore', 'Madurai'],
        'Block': ['Chennai North', 'Coimbatore East', 'Madurai Central'],
        'Panchayat': ['Anna Nagar', 'RS Puram', 'Sellur'],
        'Population': [150000, 80000, 45000],
        'Literacy_Rate': [0.88, 0.82, 0.75],
        'Banking_Penetration': [0.75, 0.65, 0.55],
        'ATM_Count': [25, 15, 8],
        'Bank_Branch_Count': [12, 8, 4],
        'SHG_Count': [45, 30, 20],
        'Agriculture_Percentage': [0.2, 0.4, 0.6],
        'Industry_Percentage': [0.3, 0.4, 0.2],
        'Services_Percentage': [0.5, 0.2, 0.2],
        'Infrastructure_Score': [9, 7, 5],
        'Road_Connectivity_Score': [9, 8, 6],
        'Electricity_Access_Rate': [0.98, 0.92, 0.85],
        'Internet_Penetration': [0.75, 0.60, 0.40],
        'Mobile_Coverage_Score': [9, 8, 7],
        'Average_Annual_Rainfall': [1200, 800, 600],
        'Flood_Risk_Score': [7, 3, 2],
        'Drought_Risk_Score': [2, 5, 8],
        'Market_Access_Score': [9, 7, 5],
        'Healthcare_Access_Score': [8, 6, 4],
        'Education_Infrastructure_Score': [9, 7, 5]
    }
    
    template_df = pd.DataFrame(template_data)
    
    # Save template
    template_path = 'input_excel/data_input_template.xlsx'
    os.makedirs('input_excel', exist_ok=True)
    template_df.to_excel(template_path, index=False)
    
    print(f"✅ Created Excel template: {template_path}")
    print(f"📊 Template includes {len(template_df.columns)} columns with comprehensive risk factors")
    
    # Display template structure
    print(f"\n📋 Template Structure:")
    for i, col in enumerate(template_df.columns, 1):
        print(f"  {i:2d}. {col}")
    
    return template_df

def main():
    """Main execution function"""
    
    print("🚀 EXCEL INTEGRATION AND ANALYSIS")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # Analyze Excel structure
    excel_df = analyze_excel_structure()
    
    # Analyze existing data
    data_summary = analyze_existing_data()
    
    # Generate enhanced risk analysis
    generate_enhanced_risk_analysis()
    
    # Create integration recommendations
    create_integration_recommendations()
    
    # Create Excel template
    template_df = create_excel_template()
    
    # Save analysis summary
    analysis_summary = {
        'timestamp': datetime.now().isoformat(),
        'excel_file_status': excel_df is not None,
        'excel_shape': excel_df.shape if excel_df is not None else None,
        'data_files_status': data_summary,
        'template_created': True,
        'recommendations_provided': True
    }
    
    os.makedirs('results', exist_ok=True)
    with open('results/excel_integration_analysis.json', 'w') as f:
        json.dump(analysis_summary, f, indent=2, default=str)
    
    print(f"\n💾 Analysis summary saved to: results/excel_integration_analysis.json")
    
    print("\n" + "=" * 70)
    print("✅ EXCEL INTEGRATION ANALYSIS COMPLETED")
    print("🎯 Ready for enhanced micro-lending risk assessment!")
    print("📊 Use the Excel template for consistent data input")
    print("🚀 Run streamlit dashboards for interactive visualization")
    print("=" * 70)

if __name__ == "__main__":
    main()
