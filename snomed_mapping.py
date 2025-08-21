import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Snomed Mapping", layout="wide")
BASE_DIR = Path("/Users/thanhphucphan/Library/CloudStorage/OneDrive-umc.edu.vn/OHDSI/Vocab mapping_Aug2025/python")

def load_csv(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error reading {file_path}: {e}")
        return pd.DataFrame()

def process_file():
    sno_df = load_csv(BASE_DIR / 'df_grouped_SNOMED.csv')
    sno_df_vi = load_csv(BASE_DIR / 'data_snomed_vi.csv')

    if sno_df.empty or sno_df_vi.empty:
        st.warning("One or both source files are empty or missing.")
        return pd.DataFrame()

    st.write(f'Các cột trong sno_df: {"|".join(sno_df.columns.tolist())}')
    st.write(f'Các cột trong sno_df_vi: {"|".join(sno_df_vi.columns.tolist())}')
    
    # Show only first few rows to avoid memory issues
    st.write("Sample data from sno_df:")
    st.dataframe(sno_df.head(10))
    st.write("Sample data from sno_df_vi:")
    st.dataframe(sno_df_vi.head(10))

    # Ensure required columns exist before type conversion and merging
    if 'concept_code' in sno_df.columns and 'Code' in sno_df_vi.columns:
        sno_df['concept_code'] = sno_df['concept_code'].astype(str)
        sno_df_vi['Code'] = sno_df_vi['Code'].astype(str)
        if 'concept_name_vi' in sno_df_vi.columns:
            sno_df = sno_df.merge(
                sno_df_vi[['Code', 'concept_name_vi']],
                left_on='concept_code',
                right_on='Code',
                how='left'
            )
        else:
            st.warning("Missing 'concept_name_vi' column in data_snomed_vi.csv.")
            sno_df['concept_name_vi'] = None
    else:
        st.error("Missing 'concept_code' in SNOMED or 'Code' in data_snomed_vi.csv.")
        sno_df['concept_name_vi'] = None

    return sno_df

sno_df = process_file()
if sno_df.empty:
    st.stop()

# Display dataset info
st.subheader("Dataset Information")
st.write(f"Total rows: {len(sno_df):,}")
st.write(f"Memory usage: {sno_df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# Add pagination for large datasets
rows_per_page = st.selectbox("Rows per page:", [100, 500, 1000, 5000], index=1)
total_pages = (len(sno_df) - 1) // rows_per_page + 1
page = st.selectbox(f"Page (1 to {total_pages}):", range(1, total_pages + 1))

start_idx = (page - 1) * rows_per_page
end_idx = min(start_idx + rows_per_page, len(sno_df))

st.subheader(f"Showing rows {start_idx + 1} to {end_idx} of {len(sno_df):,}")
st.dataframe(sno_df.iloc[start_idx:end_idx], use_container_width=True)

# đếm số lượng nunique của concept_code và concept_name_vi
if 'concept_code' in sno_df.columns:
    st.write(f'Số lượng concept_code: {sno_df["concept_code"].nunique():,}')
if 'concept_name_vi' in sno_df.columns:
    st.write(f'Số lượng concept_name_vi: {sno_df["concept_name_vi"].nunique():,}')

# Add download option
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv_data = convert_df(sno_df)
st.download_button(
    label="Download full dataset as CSV",
    data=csv_data,
    file_name='snomed_mapping_result.csv',
    mime='text/csv',
)