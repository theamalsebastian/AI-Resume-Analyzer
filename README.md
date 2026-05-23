# 📄 AI Resume Analyzer

An AI-powered web app that analyzes resumes against job descriptions, highlights missing skills, and simulates ATS scoring.

## 🚀 Features
- Upload resume (PDF)
- Paste job description
- Extract skills using NLP
- ATS score simulation
- Downloadable report

## 🛠️ Tech Stack
- Python
- Streamlit
- SpaCy
- PyPDF2

## ⚡ Installation
```bash
git clone https://github.com/theamalsebastian/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
pip install -r requirements.txt
python -m spacy download en_core_web_sm
streamlit run app.py
