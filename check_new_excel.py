#!/usr/bin/env python3
"""
Check the new Excel file data
"""
import pandas as pd

excel_file = '청라_층별_넓이_수정.xlsx'
df = pd.read_excel(excel_file, sheet_name='Sheet1')

print("=" * 80)
print("Updated Excel File Data")
print("=" * 80)

print(f"\nTotal rows: {len(df)}")
print(f"\nColumns: {list(df.columns)}")

print("\nAll floor data:")
for idx, row in df.iterrows():
    floor = row['층']
    area = row['면적(미터제곱)']
    print(f"  {floor:>6}: {area:>10.2f}㎡")

print(f"\nTotal floors: {len(df)}")
print("=" * 80)
