import streamlit as st
import PyPDF2
import spacy

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Predefined skills list (expand as needed)
skills_list = ["Python", "Java", "Machine Learning", "Cloud", "SQL", "AI", "Deep Learning", "Data Structures"]

# ------------------- Utility Functions -------------------

def extract_text_from_pdf(uploaded_file):
    """Extract text from uploaded PDF file."""
    text = ""
    if uploaded_file is not None:
        uploaded_file.seek(0)  # reset pointer
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

def extract_skills(text):
    """Find skills from text using predefined list."""
    if not text:
        return []
    return [skill for skill in skills_list if skill.lower() in text.lower()]

def compare_resume_with_jd(resume_text_input, jd_text_input):
    """Compare resume skills with job description skills."""
    resume_skills = extract_skills(resume_text_input)
    jd_skills = extract_skills(jd_text_input)
    missing_skills = [skill for skill in jd_skills if skill not in resume_skills]
    return resume_skills, jd_skills, missing_skills

def ats_score(resume_skills, jd_skills):
    """Calculate ATS match score."""
    if not jd_skills:
        return 0
    score = len(set(resume_skills) & set(jd_skills)) / len(jd_skills) * 100
    return round(score, 2)

# ------------------- Streamlit UI -------------------

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

# Sidebar navigation
st.sidebar.title("Navigation")
st.sidebar.markdown("📄 Upload Resume")
st.sidebar.markdown("📝 Paste Job Description")
st.sidebar.markdown("📊 View Results")

# Hero section
st.markdown(
    """
    <style>
    .hero {
        text-align: center;
        padding: 25px;
        background-color: #0f4c75;
        color: white;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
    <div class="hero">
        <h1>📄 AI Resume Analyzer</h1>
        <p>Upload your resume, paste a job description, and get instant ATS insights.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Layout with columns
col1, col2 = st.columns(2)

with col1:
    resume_file = st.file_uploader("Upload Resume (PDF)", type="pdf", key="resume_file")

with col2:
    jd_text = st.text_area("Paste Job Description", key="jd_text")

# ------------------- Main Logic -------------------

if resume_file is not None and jd_text.strip() != "":
    with st.spinner("Analyzing your resume..."):
        resume_text = extract_text_from_pdf(resume_file)
        if resume_text:
            resume_skills, jd_skills, missing = compare_resume_with_jd(resume_text, jd_text)
            score = ats_score(resume_skills, jd_skills)

            st.success("✅ Analysis Complete!")

            # Results section
            st.subheader("Results")
            st.write("**Resume Skills Found:**", resume_skills)
            st.write("**Job Description Skills:**", jd_skills)
            st.write("**Missing Skills:**", missing)

            st.metric("ATS Match Score", f"{score}%")
            st.progress(score / 100)

            # Download report
            report = f"ATS Score: {score}%\n\nResume Skills: {resume_skills}\n\nJD Skills: {jd_skills}\n\nMissing Skills: {missing}"
            st.download_button("📥 Download Report", report, file_name="resume_report.txt")
        else:
            st.warning("Could not extract text from the uploaded PDF.")
else:
    st.info("Please upload a resume and paste a job description to begin.")
