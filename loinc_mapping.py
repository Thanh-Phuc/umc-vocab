import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Loinc Mapping", layout="wide")
def load_csv(file_path):
    df = pd.read_csv(file_path)
    return df
BASE_DIR = Path("/Users/thanhphucphan/Library/CloudStorage/OneDrive-umc.edu.vn/OHDSI/Vocab mapping_Aug2025/python")

# xử lý file
def process_file():
    loinc_df = load_csv(BASE_DIR/'df_grouped_LOINC.csv')
    st.write(f'Các cột trong loinc_df: {"|".join(loinc_df.columns.tolist())}')
    loinc_vi = load_csv(BASE_DIR/'tong_hop_loinc_2025-08-20_07-23-07.csv')
    # các cột trong loinc_vi
    st.write(f'Các cột trong loinc_vi: {"|".join(loinc_vi.columns.tolist())}')
    # Các cột trong loinc_df: concept_id|concept_name|domain_id|vocabulary_id|concept_class_id|standard_concept|concept_code|valid_start_date|valid_end_date|invalid_reason

    # Các cột trong loinc_vi: LOINC Number|Long Common Name|Component|Property|Timing|Hệ thống|Scale|Phương thức|Rank
    # mapping các cột loinc vi vào loinc_df theo left là 'concept_code' và right là 'LOINC Number'
    loinc_df = loinc_df.merge(loinc_vi, left_on='concept_code', right_on='LOINC Number', how='left')
    # đổi tên cột Long Common Name thành concept_name_vi
    loinc_df.rename(columns={'Long Common Name': 'concept_name_vi'}, inplace=True)
    return loinc_df

df = process_file()

# hiển thị
st.dataframe(df[['concept_id','vocabulary_id','domain_id',"concept_name", "LOINC Number", "concept_name_vi"]])
cột_bỏ =['LOINC Number', 'Component', 'Property', 'Timing', 'Hệ thống', 'Scale', 'Phương thức', 'Rank']
df = df.drop(columns=cột_bỏ)
st.write(f'Số lượng dòng: {df.shape[0]}')
st.write(f'Các cột sẽ bỏ: {", ".join(df.columns.tolist())}')
st.dataframe(df)