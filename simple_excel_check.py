#!/usr/bin/env python3
"""
Simple Excel Analysis and Data Integration
"""

import pandas as pd
import numpy as np
import os
import sys

def main():
    print("🔍 Excel Data Analysis Started")
    
    # Check Excel file
    excel_path = "input_excel/input_data.xlsx"
    print(f"Looking for Excel file at: {excel_path}")
    
    if os.path.exists(excel_path):
        try:
            print("📊 Reading Excel file...")
            df = pd.read_excel(excel_path)
            print(f"✅ Excel file loaded successfully!")
            print(f"Shape: {df.shape}")
            print(f"Columns: {list(df.columns)}")
            print("\nFirst 3 rows:")
            print(df.head(3))
            
            # Save as CSV for easier processing
            df.to_csv('data/excel_input_data.csv', index=False)
            print("💾 Saved Excel data as CSV")
            
        except Exception as e:
            print(f"❌ Error reading Excel: {e}")
    else:
        print("❌ Excel file not found")
        
        # Create sample data
        print("📊 Creating sample Excel data...")
        sample_data = {
            'District': ['Chennai', 'Coimbatore', 'Madurai'] * 10,
            'Block': [f'Block-{i}' for i in range(1, 31)],
            'Population': np.random.randint(5000, 100000, 30),
            'Literacy_Rate': np.random.uniform(0.6, 0.9, 30)
        }
        
        df = pd.DataFrame(sample_data)
        os.makedirs('input_excel', exist_ok=True)
        df.to_excel(excel_path, index=False)
        print(f"✅ Created sample Excel file with {len(df)} records")
    
    # Check existing data
    print("\n📊 Checking existing data files...")
    
    data_files = ['borrowers.csv', 'districts.csv', 'blocks.csv', 'panchayats.csv']
    for file in data_files:
        path = f'data/{file}'
        if os.path.exists(path):
            df = pd.read_csv(path)
            print(f"✅ {file:15s}: {df.shape[0]:4d} rows, {df.shape[1]:2d} columns")
        else:
            print(f"❌ {file:15s}: Not found")
    
    print("\n✅ Analysis completed!")

if __name__ == "__main__":
    main()
