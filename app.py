import streamlit as st
import pandas as pd

# Import custom modules
from config import PAGE_CONFIG, VOCABULARY_INFO, ROWS_PER_PAGE_OPTIONS
from utils.data_loader import load_vocabulary_data
from utils.search import search_dataframe, apply_filters, get_search_statistics
from utils.ui_components import (
    render_custom_css, render_header, render_search_box, render_sidebar_info,
    render_metric_card, render_no_results, render_footer, configure_dataframe_display
)

# Configure Streamlit page
st.set_page_config(**PAGE_CONFIG)

# Apply custom styling
render_custom_css()

# Render header
render_header()

# Sidebar
with st.sidebar:
    st.markdown("### 🏥 Vocabulary Collections")
    
    vocab_type = st.radio(
        "Select Vocabulary:",
        list(VOCABULARY_INFO.keys()),
        help="Choose which medical vocabulary to search"
    )
    
    render_sidebar_info()

# Load data based on selection
df = load_vocabulary_data(vocab_type)

if df.empty:
    st.error("❌ Could not load vocabulary data. Please check file availability.")
    st.stop()

# Search interface
render_search_box()

col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    search_query = st.text_input(
        "",
        placeholder="🔍 Search by concept ID, name, Vietnamese name, or code...",
        help="Enter keywords to search across all fields",
        key=f"search_{vocab_type}"
    )

with col2:
    show_mapped_only = st.checkbox(
        "✅ Mapped only", 
        value=True,
        help="Show only records with Vietnamese translations"
    )

with col3:
    rows_to_show = st.selectbox("📄 Show", ROWS_PER_PAGE_OPTIONS, index=1)

# Apply search and filters
if search_query:
    df_filtered = search_dataframe(df, search_query)
else:
    df_filtered = df

if show_mapped_only:
    df_filtered = apply_filters(df_filtered, show_mapped_only=True)

# Get statistics
stats = get_search_statistics(df, df_filtered)

# Display statistics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(render_metric_card(stats['total_results'], "Results Found", "#667eea"), unsafe_allow_html=True)

with col2:
    st.markdown(render_metric_card(stats['mapped_count'], "With Vietnamese", "#4CAF50"), unsafe_allow_html=True)

with col3:
    st.markdown(render_metric_card(f"{stats['coverage']:.1f}%", "Coverage", "#FF9800"), unsafe_allow_html=True)

with col4:
    st.markdown(render_metric_card(stats['unique_domains'], "Domains", "#9C27B0"), unsafe_allow_html=True)

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
    column_config = configure_dataframe_display()
    
    st.dataframe(
        df_display,
        use_container_width=True,
        height=600,
        column_config=column_config
    )
    
    # Action buttons
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        csv_data = df_filtered.to_csv(index=False).encode('utf-8')
        vocab_name = VOCABULARY_INFO[vocab_type]["name"].lower()
        st.download_button(
            "⬇️ Download Results",
            data=csv_data,
            file_name=f"{vocab_name}_search_results.csv",
            mime="text/csv",
            help="Download current search results as CSV"
        )
    
    with col2:
        if st.button("🔄 Clear Filters"):
            st.rerun()
    
    with col3:
        vocab_name = VOCABULARY_INFO[vocab_type]["name"]
        st.markdown(f"**Last updated:** Data contains {len(df):,} total {vocab_name} concepts")

else:
    render_no_results()

# Footer
render_footer()
