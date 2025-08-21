import pandas as pd
from config import SEARCH_COLUMNS


def search_dataframe(df, search_terms):
    """Search dataframe based on search terms for specific columns."""
    if not search_terms.strip():
        return df
    
    search_lower = search_terms.strip().lower()
    
    # Create mask for each searchable column
    masks = []
    for col in SEARCH_COLUMNS:
        if col in df.columns:
            if col == 'concept_id':
                # For concept_id, try exact match first, then convert to string for partial match
                try:
                    # Try exact numeric match
                    masks.append(df[col] == int(search_lower))
                except ValueError:
                    # If not numeric, convert column to string and search
                    masks.append(df[col].astype(str).str.lower().str.contains(search_lower, na=False))
            else:
                # For other columns, do case-insensitive partial match
                masks.append(df[col].astype(str).str.lower().str.contains(search_lower, na=False))
    
    # Combine all masks with OR operation
    if masks:
        combined_mask = masks[0]
        for mask in masks[1:]:
            combined_mask = combined_mask | mask
        return df[combined_mask]
    
    return df


def apply_filters(df, show_mapped_only=True):
    """Apply filters to the dataframe."""
    if show_mapped_only and 'concept_name_vi' in df.columns:
        df = df[df['concept_name_vi'].notna()]
    
    return df


def get_search_statistics(df, df_filtered):
    """Calculate search and mapping statistics."""
    total_results = len(df_filtered)
    mapped_count = df_filtered['concept_name_vi'].notna().sum() if 'concept_name_vi' in df_filtered.columns else 0
    coverage = (mapped_count / total_results * 100) if total_results > 0 else 0
    unique_domains = df_filtered['domain_id'].nunique() if 'domain_id' in df_filtered.columns else 0
    
    return {
        'total_results': total_results,
        'mapped_count': mapped_count, 
        'coverage': coverage,
        'unique_domains': unique_domains
    }
