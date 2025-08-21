import os
import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Đọc các file CSV", layout="wide")

# Thư mục chứa các file CSV
BASE_DIR = Path("/Users/thanhphucphan/Library/CloudStorage/OneDrive-umc.edu.vn/OHDSI/Vocab mapping_Aug2025/python")

@st.cache_data(show_spinner=False)
def tạo_list_file_trong_folder(folder_path: Path):
    if not folder_path.exists():
        return []
    return sorted([f.name for f in folder_path.iterdir() if f.is_file() and f.suffix.lower() == '.csv'])

@st.cache_data(show_spinner=True)
def load_data(file_path: Path, nrows: int | None = None):
    # Thử đọc với UTF-8 trước, nếu lỗi thử latin-1
    encodings = ['utf-8', 'utf-8-sig', 'latin-1']
    last_err = None
    for enc in encodings:
        try:
            return pd.read_csv(file_path, encoding=enc, nrows=nrows)
        except Exception as e:
            last_err = e
            continue
    raise RuntimeError(f"Không đọc được file {file_path.name}: {last_err}")

def lọc_theo_từ_khóa(df: pd.DataFrame, key_word: str):
    if key_word.strip() == "":
        return df
    kw = key_word.strip().lower()
    # Chỉ áp dụng lọc trên các cột dạng chuỗi
    text_df = df.select_dtypes(include=['object', 'string']).fillna('')
    mask = text_df.apply(lambda col: col.str.lower().str.contains(kw, na=False))
    row_mask = mask.any(axis=1)
    return df[row_mask]

st.title("📁 Trình xem & lọc dữ liệu CSV")
st.caption("Chọn file, lọc theo từ khóa (tìm trong mọi cột dạng text).")

col_path, col_filter, col_rows = st.columns([2,2,1])

with col_path:
    st.write("Thư mục dữ liệu:")
    st.code(str(BASE_DIR))

with col_filter:
    key_word = st.text_input("Từ khóa lọc (không bắt buộc)", placeholder="Nhập từ khóa...")

with col_rows:
    sample_rows = st.number_input("Xem trước (số dòng)", min_value=0, value=0, step=100,
                                  help="0 = đọc toàn bộ")

list_file = tạo_list_file_trong_folder(BASE_DIR)
if not list_file:
    st.warning("Không tìm thấy file CSV nào trong thư mục.")
    st.stop()

file_chọn = st.selectbox("Chọn file CSV", list_file, index=0)

file_path = BASE_DIR / file_chọn
if not file_path.exists():
    st.error("File không tồn tại.")
    st.stop()

# Thông tin file
size_kb = file_path.stat().st_size / 1024
st.write(f"🗂️ File: `{file_chọn}` | Kích thước: {size_kb:,.1f} KB")

with st.spinner("Đang đọc dữ liệu..."):
    df = load_data(file_path, nrows=sample_rows if sample_rows > 0 else None)

st.success(f"Đã tải dữ liệu: {df.shape[0]:,} dòng × {df.shape[1]:,} cột")

# Lọc
df_filtered = lọc_theo_từ_khóa(df, key_word)

if key_word.strip():
    st.info(f"Kết quả lọc: {df_filtered.shape[0]:,} / {df.shape[0]:,} dòng")

# Hiển thị
st.dataframe(df_filtered, use_container_width=True, height=500)

# Thống kê nhanh
with st.expander("🔎 Thống kê nhanh"):
    st.write("Kiểu dữ liệu:")
    st.write(df.dtypes.astype(str))
    st.write("5 dòng đầu:")
    st.dataframe(df.head())

# Tải xuống
csv_export = df_filtered.to_csv(index=False).encode('utf-8-sig')
st.download_button(
    "⬇️ Tải dữ liệu (CSV UTF-8-SIG)",
    data=csv_export,
    file_name=f"filtered_{file_chọn}",
    mime="text/csv"
)

st.caption("✅ Hoàn tất. Bạn có thể chọn file khác hoặc thay đổi từ khóa để lọc.")