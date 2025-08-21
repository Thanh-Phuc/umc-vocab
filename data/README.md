# Data Directory

This directory contains the medical vocabulary data files required by the UMC Vocabulary Search Portal.

## Required Files

### SNOMED CT
- `df_grouped_SNOMED.csv` - Main SNOMED CT vocabulary data
- `data_snomed_vi.csv` - Vietnamese translations for SNOMED CT concepts

### LOINC
- `df_grouped_LOINC.csv` - Main LOINC vocabulary data
- `tong_hop_loinc_2025-08-20_07-23-07.csv` - Vietnamese translations for LOINC concepts

### ICD-10
- `df_grouped_ICD10.csv` - Main ICD-10 vocabulary data
- `Danh mục ICD-10 kcb.xlsx` - Vietnamese translations for ICD-10 concepts (Excel format)

## File Structure

```
data/
├── df_grouped_SNOMED.csv
├── data_snomed_vi.csv
├── df_grouped_LOINC.csv
├── tong_hop_loinc_2025-08-20_07-23-07.csv
├── df_grouped_ICD10.csv
└── Danh mục ICD-10 kcb.xlsx
```

## Data Format Requirements

### Main Vocabulary Files (SNOMED, LOINC, ICD-10)
Required columns:
- `concept_id` - Unique concept identifier
- `concept_name` - English concept name
- `concept_code` - Vocabulary-specific code
- `domain_id` - Domain classification
- `vocabulary_id` - Source vocabulary identifier
- `concept_class_id` - Concept class
- `standard_concept` - Standard concept flag

### Vietnamese Translation Files

#### SNOMED CT (`data_snomed_vi.csv`)
Required columns:
- `Code` - Matches `concept_code` in main file
- `concept_name_vi` - Vietnamese translation

#### LOINC (`tong_hop_loinc_2025-08-20_07-23-07.csv`)
Required columns:
- `LOINC Number` - Matches `concept_code` in main file
- `Long Common Name` - Vietnamese translation

#### ICD-10 (`Danh mục ICD-10 kcb.xlsx`)
Required columns:
- `Code` - Matches `concept_code` in main file
- `Nội dung` - Vietnamese translation

## Data Sources

- **SNOMED CT**: International Health Terminology Standards Development Organisation (IHTSDO)
- **LOINC**: Regenstrief Institute, Inc.
- **ICD-10**: World Health Organization (WHO)
- **Vietnamese Translations**: Vietnam Ministry of Health

## Important Notes

1. **Data files are not included in the Git repository** due to:
   - Large file sizes
   - Licensing restrictions
   - Data privacy concerns

2. **To use the application**, you must:
   - Obtain the required vocabulary files from their respective sources
   - Place them in this directory with the exact filenames listed above
   - Ensure proper licensing compliance

3. **File Encoding**: 
   - CSV files should use UTF-8 encoding
   - Excel files should be in .xlsx format

4. **Data Updates**:
   - Vocabulary standards are updated regularly
   - Check for updated versions from official sources
   - Update filenames in `config.py` if using different versions

## Licensing

Each vocabulary has its own licensing terms:
- **SNOMED CT**: IHTSDO licensing
- **LOINC**: Regenstrief Institute licensing
- **ICD-10**: WHO licensing

Please ensure compliance with all applicable licenses before using the data.

## Support

For questions about data requirements or format issues, please:
1. Check the application logs for specific error messages
2. Verify file formats and column names
3. Contact the development team for assistance

## Data Privacy

- Handle all medical terminology data according to institutional privacy policies
- Do not commit sensitive or proprietary data to version control
- Follow data governance guidelines for your organization
