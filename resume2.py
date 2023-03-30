import streamlit as st
import os
import pandas as pd
import re
import nltk
import spacy
import en_core_web_sm
import docx
import requests
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('universal_tagset')
nltk.download('maxent_ne_chunker')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('brown')
from resume_parser import resumeparse
from pyresparser import ResumeParser
import docx2txt

def select_resume_file(folder_path='Resumes'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a resume file', filenames)
    return os.path.join(folder_path, selected_filename)

def extract_skills(resume_file):
    Skills_extraction = ResumeParser(resume_file).get_extracted_data()
    extract_for_YoE = resumeparse.read_file(resume_file)
    Skills_extracted = Skills_extraction['skills']
    Skills_extracted = [x.lower().strip() for x in Skills_extracted]
    res = {'Data Scientist': [], 'HR': [], 'Sales': []}
    for skill in Skills_extracted:
        if skill in ["machine learning"]:
            res['Data Scientist'].append(skill)
        if skill in ["recruiting", "talent acquisition"]:
            res['HR'].append(skill)
        if skill in ["sales", "marketing"]:
            res['Sales'].append(skill)
    return res, extract_for_YoE['total_exp']

def predict_job_role(skills):
    if skills['HR'] > skills['Data Scientist'] and skills['HR'] > skills['Sales']:
        return "HR"
    elif skills['Data Scientist'] > skills['HR'] and skills['Data Scientist'] > skills['Sales']:
        return "Data Scientist"
    elif skills['Sales'] > skills['HR'] and skills['Sales'] > skills['Data Scientist']:
        return "Sales"
    else:
        return "Undetermined"

def select_salary_data():
    sal_data = pd.read_csv("Sal_data.csv")
    return sal_data

def get_salary_for_experience(sal_data, job_role, experience):
    if experience <= 2:
        yoe = "0-2"
    elif experience >= 11:
        yoe = "10+"
    else:
        yoe = str(experience) + "-" + str(experience + 1)
    return sal_data.loc[(sal_data['Job Role'] == job_role) & (sal_data['YoE'] == yoe)]

def display_salary_prediction(sal_data, job_role, experience):
    salary_data = get_salary_for_experience(sal_data, job_role, experience)
    st.write("Salary prediction:")
    st.write(salary_data)

def process_resume_file(resume_file):
    if resume_file.endswith(".pdf"):
        skills, experience = extract_skills(resume_file)
        job_role = predict_job_role(skills)
        sal_data = select_salary_data()
        display_salary_prediction(sal_data, job_role, experience)
        st.write(f"He is specialised in {job_role}")
    elif resume_file.endswith(".doc") or resume_file.endswith(".docx"):
        text = docx2txt.process(resume_file)
        pattern = r"(\d+)\+?\s*(years?|yrs)"
        matches = re.findall(pattern, text, re.IGNORECASE)
        experience = int(matches[0][0]) if matches else 0
        st.write(f"Years of experience in {resume_file}: {experience}")
        skills, _ = extract_skills(resume_file)
        st.write("The skills that get matched with our keywords:", skills)
        st.write("Job role prediction: Undetermined")

# main code
resume_file = select_resume_file()
if st.button("Process"):
    process_resume_file(resume_file)

