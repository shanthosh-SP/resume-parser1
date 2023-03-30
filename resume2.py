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


def select_file(folder_path='Resumes'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)

def extract_skills(filename):
    if filename.endswith(".pdf"):
        skills_extracted = ResumeParser(filename).get_extracted_data()['skills']
        skills_extracted = [skill.lower().strip(' )(') for skill in skills_extracted]
        return skills_extracted
    return []

def get_job_role(skills_extracted):
    skills_reqd_ds = ["machine learning"]
    skills_reqd_hr = ["recruiting", "talent acquisition"]
    skills_reqd_sales = ["sales", "marketing"]
    count_ds = sum([1 for skill in skills_extracted if skill in skills_reqd_ds])
    count_hr = sum([1 for skill in skills_extracted if skill in skills_reqd_hr])
    count_sales = sum([1 for skill in skills_extracted if skill in skills_reqd_sales])
    if count_ds > count_hr and count_ds > count_sales:
        return "Data Scientist"
    elif count_hr > count_ds and count_hr > count_sales:
        return "HR"
    elif count_sales > count_ds and count_sales > count_hr:
        return "Sales"
    return ""

def display_salary_data(total_exp, job_role):
    salary_data = pd.read_csv("Sal_data.csv")
    salary_data = salary_data.loc[salary_data['Job Role'] == job_role]
    if total_exp <= 2:
        salary_data = salary_data.loc[salary_data['YoE'] == "0-2"]
    elif total_exp >= 11:
        salary_data = salary_data.loc[salary_data['YoE'] == "10+"]
    st.write(salary_data)

filename = select_file()
if st.button("Process"):
    skills_extracted = extract_skills(filename)
    job_role = get_job_role(skills_extracted)
    if job_role:
        st.write(f"He is specialized in {job_role}")
        total_exp = resumeparse.read_file(filename)['total_exp']
        display_salary_data(total_exp, job_role)
    else:
        st.write("No suitable job role found based on the skills extracted.")
