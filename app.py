import streamlit as st
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

# Function to extract text from the uploaded PDF file
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text()
    return text

# Function to calculate a matching score based on keywords
def calculate_score(resume_text, job_description):
    # Convert both resume and job description to lowercase for case-insensitive comparison
    resume_text = resume_text.lower()
    job_description = job_description.lower()

    # Split job description into keywords (you can customize this with more advanced logic)
    job_keywords = set(job_description.split())

    # Split resume text into words
    resume_words = set(resume_text.split())

    # Find matching keywords
    matching_keywords = job_keywords.intersection(resume_words)

    # Calculate score as percentage of keywords matched
    if len(job_keywords) == 0:
        return 0  # Avoid division by zero
    score = (len(matching_keywords) / len(job_keywords)) * 100

    return round(score, 2), matching_keywords

# Streamlit app
st.title("Smart ATS ")
st.text("Improve Your Resume ATS")

# Input for job description
jd = st.text_area("Paste the Job Description")

# File uploader for resume
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

# On submission
if st.button("Submit"):
    if uploaded_file is not None:
        # Extract resume text from the PDF
        resume_text = input_pdf_text(uploaded_file)

        # Calculate score and matching keywords
        score, matching_keywords = calculate_score(resume_text, jd)

        # Extract the file name of the uploaded resume
        cv_file_name = uploaded_file.name

        # Display the result in the format "CV File Name : Score"
        st.subheader(f"CV File Name: {cv_file_name}")
        st.subheader(f"Score: {score}%")
        st.text(f"Matching Keywords: {', '.join(matching_keywords) if matching_keywords else 'None'}")
