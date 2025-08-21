#!/usr/bin/env python3
"""
Create sample data files for testing the UMC Vocabulary Search Portal
This script generates minimal sample data to test the application functionality.
"""

import pandas as pd
import os
from pathlib import Path

def create_sample_data():
    """Create sample vocabulary data files for testing."""
    
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Sample SNOMED CT data
    snomed_main_data = {
        'concept_id': ['12345', '23456', '34567'],
        'concept_name': ['Hypertension', 'Diabetes mellitus', 'Asthma'],
        'concept_code': ['38341003', '73211009', '195967001'],
        'domain_id': ['Condition', 'Condition', 'Condition'],
        'vocabulary_id': ['SNOMED', 'SNOMED', 'SNOMED'],
        'concept_class_id': ['Clinical finding', 'Clinical finding', 'Clinical finding'],
        'standard_concept': ['S', 'S', 'S']
    }
    
    snomed_vi_data = {
        'Code': ['38341003', '73211009', '195967001'],
        'concept_name_vi': ['Tăng huyết áp', 'Đái tháo đường', 'Hen suyễn']
    }
    
    # Sample LOINC data
    loinc_main_data = {
        'concept_id': ['45678', '56789', '67890'],
        'concept_name': ['Hemoglobin', 'Glucose', 'Cholesterol'],
        'concept_code': ['718-7', '2345-7', '2093-3'],
        'domain_id': ['Measurement', 'Measurement', 'Measurement'],
        'vocabulary_id': ['LOINC', 'LOINC', 'LOINC'],
        'concept_class_id': ['Lab Test', 'Lab Test', 'Lab Test'],
        'standard_concept': ['S', 'S', 'S']
    }
    
    loinc_vi_data = {
        'LOINC Number': ['718-7', '2345-7', '2093-3'],
        'Long Common Name': ['Hemoglobin [Mass/volume] in Blood', 'Glucose [Mass/volume] in Serum or Plasma', 'Cholesterol [Mass/volume] in Serum or Plasma']
    }
    
    # Sample ICD-10 data
    icd_main_data = {
        'concept_id': ['78901', '89012', '90123'],
        'concept_name': ['Essential hypertension', 'Type 2 diabetes mellitus', 'Asthma, unspecified'],
        'concept_code': ['I10', 'E11', 'J45.9'],
        'domain_id': ['Condition', 'Condition', 'Condition'],
        'vocabulary_id': ['ICD10CM', 'ICD10CM', 'ICD10CM'],
        'concept_class_id': ['3-char nonbill code', '3-char nonbill code', '4-char billing code'],
        'standard_concept': ['S', 'S', 'S']
    }
    
    icd_vi_data = {
        'Code': ['I10', 'E11', 'J45.9'],
        'Nội dung': ['Tăng huyết áp nguyên phát', 'Đái tháo đường type 2', 'Hen suyễn không đặc hiệu']
    }
    
    # Create CSV files
    pd.DataFrame(snomed_main_data).to_csv(data_dir / "df_grouped_SNOMED.csv", index=False)
    pd.DataFrame(snomed_vi_data).to_csv(data_dir / "data_snomed_vi.csv", index=False)
    
    pd.DataFrame(loinc_main_data).to_csv(data_dir / "df_grouped_LOINC.csv", index=False)
    pd.DataFrame(loinc_vi_data).to_csv(data_dir / "tong_hop_loinc_2025-08-20_07-23-07.csv", index=False)
    
    pd.DataFrame(icd_main_data).to_csv(data_dir / "df_grouped_ICD10.csv", index=False)
    
    # Create Excel file for ICD-10 Vietnamese translations
    with pd.ExcelWriter(data_dir / "Danh mục ICD-10 kcb.xlsx") as writer:
        pd.DataFrame(icd_vi_data).to_excel(writer, index=False)
    
    print("✅ Sample data files created successfully!")
    print("\nCreated files:")
    for file in data_dir.glob("*"):
        print(f"  - {file}")

if __name__ == "__main__":
    create_sample_data()
