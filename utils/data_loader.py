import pandas as pd
import streamlit as st
from pathlib import Path
from config import BASE_DIR, DATA_FILES


@st.cache_data(show_spinner=False)
def load_csv(file_path):
    """Load CSV file with error handling."""
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        st.error(f"Error reading {file_path.name}: {e}")
        return pd.DataFrame()


def reorder_columns(df):
    """Reorder columns in the specified order and remove unwanted columns."""
    from config import DISPLAY_COLUMNS
    
    available_columns = [col for col in DISPLAY_COLUMNS if col in df.columns]
    return df[available_columns]


@st.cache_data
def load_vocabulary_data(vocab_type):
    """Load and merge vocabulary data with Vietnamese translations."""
    
    # Map vocabulary type to config key
    vocab_map = {
        "🔍 SNOMED CT": "snomed",
        "🧬 LOINC": "loinc", 
        "📋 ICD-10": "icd"
    }
    
    config_key = vocab_map.get(vocab_type)
    if not config_key:
        return pd.DataFrame()
    
    config = DATA_FILES[config_key]
    
    # Load main vocabulary file
    main_df = load_csv(BASE_DIR / config["main"])
    
    # Load Vietnamese translation file
    if config_key == "icd":
        try:
            vi_df = pd.read_excel(BASE_DIR / config["vietnamese"])
        except Exception as e:
            st.error(f"Error reading Excel file: {e}")
            vi_df = pd.DataFrame()
    else:
        vi_df = load_csv(BASE_DIR / config["vietnamese"])
    
    # Return empty if either file failed to load
    if main_df.empty or vi_df.empty:
        return pd.DataFrame()
    
    # Merge data based on vocabulary type
    main_df = merge_vocabulary_data(main_df, vi_df, config)
    
    return reorder_columns(main_df) if not main_df.empty else pd.DataFrame()


def merge_vocabulary_data(main_df, vi_df, config):
    """Merge main vocabulary data with Vietnamese translations."""
    
    # Convert concept_code to string for matching
    main_df['concept_code'] = main_df['concept_code'].astype(str)
    vi_df[config["code_column"]] = vi_df[config["code_column"]].astype(str)
    
    # Check if Vietnamese name column exists
    if config["name_column"] not in vi_df.columns:
        st.warning(f"Missing '{config['name_column']}' column in Vietnamese file.")
        main_df['concept_name_vi'] = None
        return main_df
    
    # Perform left join
    main_df = main_df.merge(
        vi_df[[config["code_column"], config["name_column"]]],
        left_on='concept_code',
        right_on=config["code_column"],
        how='left'
    )
    
    # Rename Vietnamese column to standard name
    if config["name_column"] != 'concept_name_vi':
        main_df.rename(columns={config["name_column"]: 'concept_name_vi'}, inplace=True)
    
    return main_df
