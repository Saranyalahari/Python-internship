# AI Code Reviewer

AI Code Reviewer is a Streamlit-based application that analyzes Python code and provides suggestions to improve code quality. It uses flake8, black, and radon to evaluate style, formatting, and complexity.

---

## Features
- Analyze Python code using flake8
- Format code using black
- Measure complexity using radon
- Display quality score and metrics
- Provide improvement suggestions
- Visualize results using charts
- Export reports in JSON and Markdown

---

## Requirements
- Python 3.x
- streamlit
- flake8
- black
- radon
- pandas
- plotly

---

## Installation
1. Clone or download the project
2. Open terminal in the project folder
3. Create virtual environment

python -m venv venv

4. Activate environment

venv\Scripts\activate

5. Install dependencies

pip install -r requirements.txt


---

## Usage
1. Run the application

streamlit run app.py

2. Open browser and go to

http://localhost:8501

3. Paste or upload Python code
4. View analysis results

---

## Project Structure

ai-code-reviewer/
│
├── app.py
├── requirements.txt
└── README.md


---

## Notes
- Supports only Python code
- Ensure all dependencies are installed
- Works offline after setup