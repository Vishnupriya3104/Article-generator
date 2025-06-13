import streamlit as st
import google.generativeai as genai
import PyPDF2

# 🔐 Load Gemini API key from Streamlit secrets
genai.configure(api_key=st.secrets["general"]["AIzaSyB4IjWrszJ5c50JyBBSSy5CTcgNSvvHQEw"])

# 🧠 Load Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

# 🖼️ Streamlit UI
st.title("📄 Resume Analyzer using Gemini AI")

uploaded_file = st.file_uploader("Upload your Resume (PDF or Text)", type=["pdf", "txt"])
job_role = st.text_input("Enter the Job Role you're applying for")

# 📄 Extract text from resume
def extract_text(file):
    if file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    else:
        return file.read().decode("utf-8")

# 🧠 Analyze the resume
if uploaded_file and job_role:
    resume_text = extract_text(uploaded_file)

    with st.spinner("Analyzing your resume..."):
        prompt = f"""
You are a professional resume analyzer.

Given the following resume and a target job role, do the following:
1. Extract and list the key technical and soft skills.
2. Summarize the candidate’s work experience in 3-4 bullet points.
3. Rate the alignment of this resume with the role of '{job_role}' on a scale of 1 to 10.
4. Suggest one improvement to better match the role.

Resume:
{resume_text}
"""
        response = model.generate_content(prompt)
        st.success("✅ Analysis Complete!")

        # Display results
        st.subheader("📌 Gemini AI Feedback")
        st.write(response.text)
