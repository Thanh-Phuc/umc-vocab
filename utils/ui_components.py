import streamlit as st


def render_custom_css():
    """Render custom CSS styles for the application."""
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


def render_header():
    """Render the main application header."""
    st.markdown("""
    <div class="main-header">
        <h1>🔍 UMC Vocabulary Search Portal</h1>
        <p>Search and explore medical vocabularies with Vietnamese translations</p>
    </div>
    """, unsafe_allow_html=True)


def render_search_box():
    """Render the search interface section."""
    st.markdown("""
    <div class="search-box">
        <h3>🔍 Search Interface</h3>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar_info():
    """Render informational content in sidebar."""
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


def render_metric_card(value, label, color="#667eea"):
    """Render a metric card with custom styling."""
    return f"""
    <div class="metric-container">
        <h3 style="color: {color}; margin: 0;">{value:,}</h3>
        <p style="margin: 0; color: #666;">{label}</p>
    </div>
    """


def render_no_results():
    """Render no results found message."""
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


def render_footer():
    """Render application footer."""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🏥 <strong>UMC Vocabulary Search Portal</strong> | Medical terminology search with Vietnamese translations</p>
    </div>
    """, unsafe_allow_html=True)


def configure_dataframe_display():
    """Configure dataframe column display settings."""
    return {
        "concept_id": st.column_config.NumberColumn("Concept ID", width="small"),
        "concept_name": st.column_config.TextColumn("English Name", width="large"),
        "concept_name_vi": st.column_config.TextColumn("Vietnamese Name", width="large"),
        "domain_id": st.column_config.TextColumn("Domain", width="small"),
        "vocabulary_id": st.column_config.TextColumn("Vocabulary", width="small"),
        "concept_class_id": st.column_config.TextColumn("Class", width="small"),
        "standard_concept": st.column_config.TextColumn("Standard", width="small"),
        "concept_code": st.column_config.TextColumn("Code", width="medium")
    }
