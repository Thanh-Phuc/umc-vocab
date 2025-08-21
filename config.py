from pathlib import Path
import os

# Base configuration - use environment variable or default to data directory
BASE_DIR = Path(os.getenv('BASE_DIR', Path(__file__).parent / 'data'))

# Data file paths
DATA_FILES = {
    "snomed": {
        "main": "df_grouped_SNOMED.csv",
        "vietnamese": "data_snomed_vi.csv",
        "code_column": "Code",
        "name_column": "concept_name_vi"
    },
    "loinc": {
        "main": "df_grouped_LOINC.csv", 
        "vietnamese": "tong_hop_loinc_2025-08-20_07-23-07.csv",
        "code_column": "LOINC Number",
        "name_column": "Long Common Name"
    },
    "icd": {
        "main": "df_grouped_ICD10.csv",
        "vietnamese": "Danh mục ICD-10 kcb.xlsx",
        "code_column": "Code", 
        "name_column": "Nội dung"
    }
}

# UI Configuration
PAGE_CONFIG = {
    "page_title": "UMC Vocabulary Search",
    "page_icon": "🔍",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Display settings
DISPLAY_COLUMNS = [
    'concept_id', 'concept_name', 'concept_name_vi', 
    'domain_id', 'vocabulary_id', 'concept_class_id', 
    'standard_concept', 'concept_code'
]

SEARCH_COLUMNS = ['concept_id', 'concept_name', 'concept_name_vi', 'concept_code']

ROWS_PER_PAGE_OPTIONS = [50, 100, 250, 500]

# Vocabulary information
VOCABULARY_INFO = {
    "🔍 SNOMED CT": {
        "name": "SNOMED CT",
        "description": "Systematized Nomenclature of Medicine Clinical Terms",
        "color": "#667eea"
    },
    "🧬 LOINC": {
        "name": "LOINC", 
        "description": "Logical Observation Identifiers Names and Codes",
        "color": "#4CAF50"
    },
    "📋 ICD-10": {
        "name": "ICD-10",
        "description": "International Classification of Diseases, 10th Revision", 
        "color": "#FF9800"
    }
}
