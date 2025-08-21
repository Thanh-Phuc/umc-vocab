#!/usr/bin/env python3
"""
Setup script for UMC Vocabulary Search Portal
"""

import os
import subprocess
import sys
from pathlib import Path


def create_virtual_environment():
    """Create a virtual environment for the project."""
    print("Creating virtual environment...")
    subprocess.run([sys.executable, "-m", "venv", "venv"])
    print("✅ Virtual environment created successfully!")


def install_requirements():
    """Install required packages."""
    print("Installing requirements...")
    
    # Determine the correct pip path based on OS
    if os.name == 'nt':  # Windows
        pip_path = "venv/Scripts/pip"
    else:  # Unix/Linux/MacOS
        pip_path = "venv/bin/pip"
    
    subprocess.run([pip_path, "install", "-r", "requirements.txt"])
    print("✅ Requirements installed successfully!")


def create_data_directory():
    """Create data directory if it doesn't exist."""
    data_dir = Path("data")
    if not data_dir.exists():
        data_dir.mkdir()
        print("✅ Data directory created!")
        
        # Create a README in the data directory
        with open(data_dir / "README.md", "w") as f:
            f.write("""# Data Directory

Place your vocabulary files here:

## Required Files:
- `df_grouped_SNOMED.csv` - SNOMED CT main vocabulary
- `data_snomed_vi.csv` - SNOMED CT Vietnamese translations
- `df_grouped_LOINC.csv` - LOINC main vocabulary  
- `tong_hop_loinc_2025-08-20_07-23-07.csv` - LOINC Vietnamese translations
- `df_grouped_ICD10.csv` - ICD-10 main vocabulary
- `Danh mục ICD-10 kcb.xlsx` - ICD-10 Vietnamese translations

## File Structure:
```
data/
├── df_grouped_SNOMED.csv
├── data_snomed_vi.csv
├── df_grouped_LOINC.csv
├── tong_hop_loinc_2025-08-20_07-23-07.csv
├── df_grouped_ICD10.csv
└── Danh mục ICD-10 kcb.xlsx
```

Note: Data files are not included in the repository due to size and licensing constraints.
""")
        print("📁 Please add your vocabulary data files to the 'data/' directory")
    else:
        print("✅ Data directory already exists!")


def main():
    """Main setup function."""
    print("🔍 UMC Vocabulary Search Portal Setup")
    print("=" * 50)
    
    try:
        create_virtual_environment()
        install_requirements() 
        create_data_directory()
        
        print("\n" + "=" * 50)
        print("✅ Setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Add your vocabulary data files to the 'data/' directory")
        print("2. Update the BASE_DIR path in config.py if needed")
        print("3. Activate virtual environment:")
        
        if os.name == 'nt':  # Windows
            print("   venv\\Scripts\\activate")
        else:  # Unix/Linux/MacOS
            print("   source venv/bin/activate")
            
        print("4. Run the application:")
        print("   streamlit run app.py")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
