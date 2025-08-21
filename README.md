# UMC Vocabulary Search Portal

A web-based medical terminology search engine with Vietnamese translation support for SNOMED CT, LOINC, and ICD-10 vocabularies.

## Features

- 🔍 **Multi-vocabulary Search**: Search across SNOMED CT, LOINC, and ICD-10 terminologies
- 🌐 **Bilingual Support**: Search in both English and Vietnamese with real-time translation mapping
- 📊 **Real-time Statistics**: Coverage metrics and mapping quality indicators
- 🎨 **Modern UI**: Google-like search interface with responsive design
- 📥 **Data Export**: Download search results as CSV files
- ⚡ **Performance Optimized**: Cached data loading and pagination for large datasets

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/umc-vocabulary-search.git
cd umc-vocabulary-search
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Data Setup

Place your vocabulary files in the `data/` directory:

```
data/
├── df_grouped_SNOMED.csv
├── data_snomed_vi.csv
├── df_grouped_LOINC.csv
├── tong_hop_loinc_2025-08-20_07-23-07.csv
├── df_grouped_ICD10.csv
└── Danh mục ICD-10 kcb.xlsx
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8501`

3. Select a vocabulary type from the sidebar

4. Enter search terms in the search box

5. Use filters to refine results

6. Download results as needed

## File Structure

```
├── app.py                 # Main Streamlit application
├── config.py             # Configuration settings
├── utils/
│   ├── __init__.py
│   ├── data_loader.py    # Data loading utilities
│   ├── search.py         # Search functionality
│   └── ui_components.py  # UI helper functions
├── styles/
│   └── custom.css        # Custom CSS styles
├── data/                 # Vocabulary data files (not included in repo)
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Configuration

Edit `config.py` to modify:
- Data file paths
- UI settings
- Search parameters
- Display options

## Supported Vocabularies

- **SNOMED CT**: Systematized Nomenclature of Medicine Clinical Terms
- **LOINC**: Logical Observation Identifiers Names and Codes  
- **ICD-10**: International Classification of Diseases, 10th Revision

## Search Features

- **Exact Match**: Search by concept ID for precise results
- **Partial Match**: Keyword search across all text fields
- **Bilingual Search**: Search in both English and Vietnamese
- **Field-specific Search**: Target specific columns (ID, name, code)
- **Real-time Filtering**: Instant results as you type

## Technical Details

- **Framework**: Streamlit
- **Language**: Python 3.8+
- **Data Processing**: pandas
- **Styling**: Custom CSS with modern design
- **Performance**: Caching and pagination for large datasets

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

- **Organization**: University Medical Center (UMC)
- **Department**: Medical Informatics
- **Purpose**: Healthcare terminology standardization in Vietnam

## Acknowledgments

- SNOMED International for SNOMED CT terminology
- Regenstrief Institute for LOINC standards
- World Health Organization for ICD-10 classification
- Vietnamese Ministry of Health for translation standards
