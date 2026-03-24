# Test Coverage Dashboard

## Features
- File-wise test coverage analysis
- Visual dashboard using Streamlit
- Highlights low coverage files

## Run Instructions
1. Install dependencies:
   pip install -r requirements.txt

2. Run tests:
   coverage run -m pytest

3. Generate report:
   coverage json -o coverage.json

4. Start dashboard:
   streamlit run app.py