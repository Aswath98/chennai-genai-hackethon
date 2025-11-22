#!/usr/bin/env python3
"""
Quick script to examine Excel file structure
"""
import pandas as pd
import os

def examine_excel():
    excel_path = 'input_excel/input_data.xlsx'
    
    print(f"Looking for Excel file at: {excel_path}")
    print(f"File exists: {os.path.exists(excel_path)}")
    
    if not os.path.exists(excel_path):
        print("Excel file not found!")
        return
    
    try:
        # Read Excel file
        excel_file = pd.ExcelFile(excel_path)
        print(f"\n📊 Excel file has {len(excel_file.sheet_names)} sheets:")
        
        for i, sheet_name in enumerate(excel_file.sheet_names):
            print(f"\n{i+1}. Sheet: '{sheet_name}'")
            
            try:
                df = pd.read_excel(excel_path, sheet_name=sheet_name)
                print(f"   Shape: {df.shape}")
                print(f"   Columns: {list(df.columns)}")
                
                if len(df) > 0:
                    print(f"   Sample data (first 2 rows):")
                    for idx, row in df.head(2).iterrows():
                        print(f"     Row {idx}: {dict(row)}")
                else:
                    print("   Empty sheet")
                    
            except Exception as sheet_error:
                print(f"   Error reading sheet: {sheet_error}")
                
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")

if __name__ == "__main__":
    examine_excel()
