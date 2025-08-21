import streamlit as st
import pandas as pd
from pathlib import Path

# Custom CSS for better UI
st.set_page_config(
    page_title="UMC Vocabulary Search", 
    page_icon="🔍", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .search-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    .stats-box {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .vocab-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #4CAF50;
        margin-bottom: 1rem;
    }
    .stSelectbox > div > div {
        background-color: #f8f9fa;
    }
    .sidebar-info {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    h1 {
        color: #2c3e50;
    }
    .metric-container {
        background: #fff;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Base directory
BASE_DIR = Path("/Users/thanhphucphan/Library/CloudStorage/OneDrive-umc.edu.vn/OHDSI/Vocab mapping_Aug2025/python")

# Utility functions
@st.cache_data(show_spinner=False)
def load_csv(file_path):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        st.error(f"Error reading {file_path.name}: {e}")
        return pd.DataFrame()

def reorder_columns(df):
    desired_columns = [
        'concept_id', 'concept_name', 'concept_name_vi', 
        'domain_id', 'vocabulary_id', 'concept_class_id', 
        'standard_concept', 'concept_code'
    ]
    available_columns = [col for col in desired_columns if col in df.columns]
    return df[available_columns]

def search_dataframe(df, search_terms):
    if not search_terms.strip():
        return df
    
    search_lower = search_terms.strip().lower()
    search_columns = ['concept_id', 'concept_name', 'concept_name_vi', 'concept_code']
    
    masks = []
    for col in search_columns:
        if col in df.columns:
            if col == 'concept_id':
                try:
                    masks.append(df[col] == int(search_lower))
                except ValueError:
                    masks.append(df[col].astype(str).str.lower().str.contains(search_lower, na=False))
            else:
                masks.append(df[col].astype(str).str.lower().str.contains(search_lower, na=False))
    
    if masks:
        combined_mask = masks[0]
        for mask in masks[1:]:
            combined_mask = combined_mask | mask
        return df[combined_mask]
    
    return df

# Header
st.markdown("""
<div class="main-header">
    <h1>🔍 UMC Vocabulary Search Portal</h1>
    <p>Search and explore medical vocabularies with Vietnamese translations</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🏥 Vocabulary Collections")
    
    vocab_type = st.radio(
        "Select Vocabulary:",
        ["🔍 SNOMED CT", "🧬 LOINC", "📋 ICD-10"],
        help="Choose which medical vocabulary to search"
    )
    
    st.markdown("""
    <div class="sidebar-info">
        <h4>💡 Search Tips:</h4>
        <ul>
            <li>Use concept ID for exact matches</li>
            <li>Enter keywords for partial matches</li>
            <li>Search works in both English and Vietnamese</li>
            <li>Use filters to refine results</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Load data based on selection
@st.cache_data
def load_vocabulary_data(vocab_type):
    if vocab_type == "🔍 SNOMED CT":
        main_df = load_csv(BASE_DIR / 'df_grouped_SNOMED.csv')
        vi_df = load_csv(BASE_DIR / 'data_snomed_vi.csv')
        
        if not main_df.empty and not vi_df.empty:
            main_df['concept_code'] = main_df['concept_code'].astype(str)
            vi_df['Code'] = vi_df['Code'].astype(str)
            if 'concept_name_vi' in vi_df.columns:
                main_df = main_df.merge(
                    vi_df[['Code', 'concept_name_vi']],
                    left_on='concept_code',
                    right_on='Code',
                    how='left'
                )
        
    elif vocab_type == "🧬 LOINC":
        main_df = load_csv(BASE_DIR / 'df_grouped_LOINC.csv')
        vi_df = load_csv(BASE_DIR / 'tong_hop_loinc_2025-08-20_07-23-07.csv')
        
        if not main_df.empty and not vi_df.empty:
            main_df['concept_code'] = main_df['concept_code'].astype(str)
            vi_df['LOINC Number'] = vi_df['LOINC Number'].astype(str)
            if 'Long Common Name' in vi_df.columns:
                main_df = main_df.merge(
                    vi_df[['LOINC Number', 'Long Common Name']],
                    left_on='concept_code',
                    right_on='LOINC Number',
                    how='left'
                )
                main_df.rename(columns={'Long Common Name': 'concept_name_vi'}, inplace=True)
    
    else:  # ICD-10
        main_df = load_csv(BASE_DIR / 'df_grouped_ICD10.csv')
        try:
            vi_df = pd.read_excel(BASE_DIR / 'Danh mục ICD-10 kcb.xlsx')
        except:
            vi_df = pd.DataFrame()
        
        if not main_df.empty and not vi_df.empty:
            main_df['concept_code'] = main_df['concept_code'].astype(str)
            vi_df['Code'] = vi_df['Code'].astype(str)
            if 'Nội dung' in vi_df.columns:
                main_df = main_df.merge(
                    vi_df[['Code', 'Nội dung']],
                    left_on='concept_code',
                    right_on='Code',
                    how='left'
                )
                main_df.rename(columns={'Nội dung': 'concept_name_vi'}, inplace=True)
    
    return reorder_columns(main_df) if not main_df.empty else pd.DataFrame()

# Load selected vocabulary
df = load_vocabulary_data(vocab_type)

if df.empty:
    st.error("❌ Could not load vocabulary data. Please check file availability.")
    st.stop()

# Search interface
st.markdown("""
<div class="search-box">
    <h3>🔍 Search Interface</h3>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    search_query = st.text_input(
        "",
        placeholder="🔍 Search by concept ID, name, Vietnamese name, or code...",
        help="Enter keywords to search across all fields",
        key=f"search_{vocab_type}"
    )

with col2:
    show_mapped_only = st.checkbox("✅ Mapped only", value=True, 
                                  help="Show only records with Vietnamese translations")

with col3:
    rows_to_show = st.selectbox("📄 Show", [50, 100, 250, 500], index=1)

# Apply filters
if search_query:
    df_filtered = search_dataframe(df, search_query)
else:
    df_filtered = df

if show_mapped_only and 'concept_name_vi' in df_filtered.columns:
    df_filtered = df_filtered[df_filtered['concept_name_vi'].notna()]

# Quick stats
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-container">
        <h3 style="color: #667eea; margin: 0;">{len(df_filtered):,}</h3>
        <p style="margin: 0; color: #666;">Results Found</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    mapped_count = df_filtered['concept_name_vi'].notna().sum() if 'concept_name_vi' in df_filtered.columns else 0
    st.markdown(f"""
    <div class="metric-container">
        <h3 style="color: #4CAF50; margin: 0;">{mapped_count:,}</h3>
        <p style="margin: 0; color: #666;">With Vietnamese</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    coverage = (mapped_count / len(df_filtered) * 100) if len(df_filtered) > 0 else 0
    st.markdown(f"""
    <div class="metric-container">
        <h3 style="color: #FF9800; margin: 0;">{coverage:.1f}%</h3>
        <p style="margin: 0; color: #666;">Coverage</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    unique_domains = df_filtered['domain_id'].nunique() if 'domain_id' in df_filtered.columns else 0
    st.markdown(f"""
    <div class="metric-container">
        <h3 style="color: #9C27B0; margin: 0;">{unique_domains}</h3>
        <p style="margin: 0; color: #666;">Domains</p>
    </div>
    """, unsafe_allow_html=True)

# Results display
if len(df_filtered) > 0:
    st.markdown("---")
    
    # Show results with pagination
    total_results = len(df_filtered)
    
    if total_results > rows_to_show:
        st.info(f"📊 Showing first {rows_to_show:,} of {total_results:,} results")
        df_display = df_filtered.head(rows_to_show)
    else:
        df_display = df_filtered
    
    # Display the data with better formatting
    st.dataframe(
        df_display,
        use_container_width=True,
        height=600,
        column_config={
            "concept_id": st.column_config.NumberColumn("Concept ID", width="small"),
            "concept_name": st.column_config.TextColumn("English Name", width="large"),
            "concept_name_vi": st.column_config.TextColumn("Vietnamese Name", width="large"),
            "domain_id": st.column_config.TextColumn("Domain", width="small"),
            "vocabulary_id": st.column_config.TextColumn("Vocabulary", width="small"),
            "concept_class_id": st.column_config.TextColumn("Class", width="small"),
            "standard_concept": st.column_config.TextColumn("Standard", width="small"),
            "concept_code": st.column_config.TextColumn("Code", width="medium")
        }
    )
    
    # Download section
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        csv_data = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            "⬇️ Download Results",
            data=csv_data,
            file_name=f"{vocab_type.split()[1].lower()}_search_results.csv",
            mime="text/csv",
            help="Download current search results as CSV"
        )
    
    with col2:
        if st.button("🔄 Clear Filters"):
            st.rerun()
    
    with col3:
        st.markdown(f"**Last updated:** Data contains {len(df):,} total {vocab_type.split()[1]} concepts")

else:
    st.markdown("""
    <div class="vocab-card" style="text-align: center; border-left-color: #FF5722;">
        <h3>🔍 No Results Found</h3>
        <p>Try adjusting your search terms or filters</p>
        <ul style="text-align: left; display: inline-block;">
            <li>Check spelling of search terms</li>
            <li>Try broader keywords</li>
            <li>Remove the "Mapped only" filter</li>
            <li>Use partial matches instead of exact terms</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🏥 <strong>UMC Vocabulary Search Portal</strong> | Medical terminology search with Vietnamese translations</p>
</div>
""", unsafe_allow_html=True)