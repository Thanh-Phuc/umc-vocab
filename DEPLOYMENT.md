# Deployment Guide

## GitHub Repository Setup

### 1. Initialize Git Repository

```bash
cd /path/to/your/project
git init
git add .
git commit -m "Initial commit: UMC Vocabulary Search Portal"
```

### 2. Create GitHub Repository

1. Go to GitHub and create a new repository
2. Name it `umc-vocabulary-search`
3. Don't initialize with README (we already have one)

### 3. Connect Local Repository to GitHub

```bash
git remote add origin https://github.com/yourusername/umc-vocabulary-search.git
git branch -M main
git push -u origin main
```

## Local Development Setup

### 1. Quick Setup (Recommended)

```bash
python3 setup.py
```

This will:
- Create virtual environment
- Install dependencies
- Create data directory structure

### 2. Manual Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create data directory
mkdir data
```

### 3. Add Data Files

Copy your vocabulary files to the `data/` directory:
- `df_grouped_SNOMED.csv`
- `data_snomed_vi.csv`
- `df_grouped_LOINC.csv`
- `tong_hop_loinc_2025-08-20_07-23-07.csv`
- `df_grouped_ICD10.csv`
- `Danh mục ICD-10 kcb.xlsx`

### 4. Run Application

```bash
# Option 1: Use startup script (Unix/Linux/MacOS)
./start.sh

# Option 2: Manual start
source venv/bin/activate
streamlit run app.py
```

## Production Deployment

### 1. Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Select `app.py` as the main file
5. Add your data files through Streamlit Cloud interface

### 2. Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:

```bash
docker build -t umc-vocab-search .
docker run -p 8501:8501 umc-vocab-search
```

### 3. Heroku Deployment

Create `Procfile`:

```
web: sh setup.sh && streamlit run app.py
```

Create `setup.sh`:

```bash
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = \$PORT\n\
" > ~/.streamlit/config.toml
```

Deploy:

```bash
heroku create umc-vocab-search
git push heroku main
```

## Environment Variables

For production deployments, consider using environment variables:

```bash
# .env file
BASE_DIR=/path/to/data
DEBUG=False
PORT=8501
```

Update `config.py` to use environment variables:

```python
import os
from pathlib import Path

BASE_DIR = Path(os.getenv('BASE_DIR', '/default/path'))
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
```

## Security Considerations

1. **Data Files**: Never commit sensitive data files to GitHub
2. **Environment Variables**: Use `.env` files for sensitive configuration
3. **Access Control**: Implement authentication if needed
4. **HTTPS**: Use HTTPS in production
5. **Data Validation**: Validate all user inputs

## Monitoring

### Application Health

Add health check endpoint in `app.py`:

```python
import streamlit as st

def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
```

### Performance Monitoring

Consider integrating:
- Application Performance Monitoring (APM)
- Error tracking (Sentry)
- Usage analytics

## Maintenance

### Regular Updates

```bash
# Update dependencies
pip list --outdated
pip install -U package_name

# Update requirements.txt
pip freeze > requirements.txt
```

### Backup Strategy

1. Regular data backups
2. Configuration backups  
3. Database backups (if applicable)

### Version Management

Use semantic versioning:
- Major: Breaking changes
- Minor: New features
- Patch: Bug fixes

Example: `v1.2.3`

## Support

For issues and support:
1. Check the README.md
2. Review error logs
3. Create GitHub issues
4. Contact the development team

## License

This project is licensed under the MIT License - see the LICENSE file for details.
