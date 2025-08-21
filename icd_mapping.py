import streamlit as st
import pandas as pd
from pathlib import Path


st.set_page_config(page_title="ICD Mapping", layout="wide")
BASE_DIR = Path("/Users/thanhphucphan/Library/CloudStorage/OneDrive-umc.edu.vn/OHDSI/Vocab mapping_Aug2025/python")



def load_csv(file_path):
    df = pd.read_csv(file_path)
    return df

# xử lý file
def process_file():
    icd_df = load_csv(BASE_DIR/'df_grouped_ICD10.csv')
    icd_df_vi = pd.read_excel(BASE_DIR/'Danh mục ICD-10 kcb.xlsx')
    # lọc lại icd df vi cột Phân loại == "Mã nhánh"
    # icd_df_vi = icd_df_vi[icd_df_vi['Phân loại'] == "Mã nhánh"]
    # merge lấy cột Nội dung trong icd_df_vi theo left là 'concept_code' và right là 'Code'
    icd_df = icd_df.merge(icd_df_vi[['Code', 'Nội dung']], left_on='concept_code', right_on='Code', how='left')
    # đổi tên cột Nội dung thành concept_name_vi
    icd_df.rename(columns={'Nội dung': 'concept_name_vi'}, inplace=True)
    return icd_df


icd_df = process_file()

# đếm concept_name_vi
# số lượng gốc nunique theo cột concept_name
st.write(f'Số lượng concept_name: {icd_df["concept_name"].nunique()}')
# số lượng concept_name_vi nunique theo cột concept_name_vi
st.write(f'Số lượng concept_name_vi: {icd_df["concept_name_vi"].nunique()}')
# tính tỷ lệ
# tỷ lệ concept_name_vi so với concept_name
tỷ_lệ = icd_df['concept_name_vi'].nunique() / icd_df['concept_name'].nunique()
st.write(f'Tỷ lệ concept_name_vi so với concept_name: {tỷ_lệ:.2%}')

st.dataframe(icd_df)
