#!/usr/bin/env python3
"""
Read the Excel file to understand the floor area data
"""
import pandas as pd

# Read Excel file
excel_file = '청라_층별_넓이.xlsx'

try:
    # Try to read all sheets
    xls = pd.ExcelFile(excel_file)
    print("=" * 80)
    print("Excel File Analysis: 청라 층별 넓이.xlsx")
    print("=" * 80)
    
    print(f"\nSheet names: {xls.sheet_names}")
    
    # Read each sheet
    for sheet_name in xls.sheet_names:
        print(f"\n{'='*80}")
        print(f"Sheet: {sheet_name}")
        print(f"{'='*80}")
        
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        print(f"\nShape: {df.shape}")
        print(f"\nColumns: {list(df.columns)}")
        print(f"\nFirst 20 rows:")
        print(df.head(20))
        
        print(f"\nData types:")
        print(df.dtypes)
        
        print(f"\nAll data:")
        print(df.to_string())
        
except Exception as e:
    print(f"Error reading Excel: {e}")
    import traceback
    traceback.print_exc()
