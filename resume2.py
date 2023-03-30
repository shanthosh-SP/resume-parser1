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
    st.write(Skills_extraction)
    extract_for_YoE = resumeparse.read_file(resume_file)
    st.write(extract_for_YoE)
    if Skills_extraction['name'] is null:
        images = convert_from_path(resume_file)
        # Process each image and extract text
        for i, image in enumerate(images):
            # Convert the image to grayscale
            image = image.convert('L')

            # Use pytesseract to extract text from the image
            resume_file = pytesseract.image_to_string(image)
    Skills_extracted = Skills_extraction['skills']
    Skills_extracted = [x.lower().strip() for x in Skills_extracted]
    res = {'DataScientist': [], 'HR': [], 'Sales': []}
    for skill in Skills_extracted:
        if skill in ['machine learning','data mining','predictive modeling', 
                      'statistical analysis', 'data visualization', 'natural language processing', 'big data', 'data warehousing', 'sql', 
                      'python/r programming', 'deep learning', 'artificial intelligence', 'data analytics', 'a/b testing', 'feature engineering', 
                      'etl processes', 'time series analysis', 'regression analysis',
                     'cluster analysis',
                     'decision trees','power bi']:

            res['DataScientist'].append(skill)
        if skill in ['ats','applicant tracking systems','job postings', 'sourcing','source' ,'interviewing skills', 'hiring process', 'job descriptions', 'talent acquisition', 'diversity and inclusion', 'background checks', 'onboarding','hr consulting' ,'recruiting','recruiter','shortlisting','interviewing','end to end recruitment','deadline','reporting','hire','walk-in drives','phone interviewing',' candidate management systems','decisionmaking','management','psychology','monitoring''cms','screening resumes','lateral']:
            res['HR'].append(skill)
        if skill in ['sales', 'account management', 'client relationship management', 'sales forecasting', 'sales strategy', 'sales negotiations', 'pipeline management', 'territory management', 'customer acquisition', 'sales performance', 'sales reporting','website sales','cilents','metrics','inside sales','strategic content development','presales executives','cold calling','executive',' marketing','business development','crm','market research', 'website sales', 'inside sales','negotiations','customer service']:
            res['Sales'].append(skill)
    
    return res, extract_for_YoE['total_exp']

def predict_job_role(skills):
    if skills['HR'] > skills['DataScientist'] and skills['HR'] > skills['Sales']:
        return "HR"
    elif skills['DataScientist'] > skills['HR'] and skills['DataScientist'] > skills['Sales']:
        return "DataScientist"
    elif skills['Sales'] > skills['HR'] and skills['Sales'] > skills['DataScientist']:
        return "Sales"
    else:
        return "Undetermined"

def select_salary_data():
    sal_data = pd.read_csv("Sal_data.csv")
    return sal_data

def get_salary_for_experience(sal_data, job_role, experience):
    if experience < 2:
        yoe = "0-2"
    elif 2<experience <= 4:
        yoe = "3-4"
    elif 4<experience <=10 :
        yoe = "5-10"
    elif experience >= 11:
        yoe = "10+"
    else:
        yoe = str(experience) + "-" + str(experience + 1)
    st.write(sal_data.loc[(sal_data['Job Role'] == job_role) & (sal_data['YoE'] == yoe)])
    return sal_data.loc[(sal_data['Job Role'] == job_role) & (sal_data['YoE'] == yoe)]

def display_salary_prediction(sal_data, job_role, experience):
    salary_data = get_salary_for_experience(sal_data, job_role, experience)
#     st.write("Salary prediction:")
#     st.write(salary_data)

def process_resume_file(resume_file):
    if resume_file.endswith(".pdf"):
        skills, experience = extract_skills(resume_file)
        job_role = predict_job_role(skills)
        sal_data = select_salary_data()
        display_salary_prediction(sal_data, job_role, experience)
#         st.write(experience, sal_data)
        st.write(f"He is specialised in {job_role}")
    elif resume_file.endswith(".doc") or resume_file.endswith(".docx"):
        text = docx2txt.process(resume_file)
        pattern = r"(\d+)\+?\s*(years?|yrs)"
        matches = re.findall(pattern, text, re.IGNORECASE)
        experience = int(matches[0][0]) if matches else 0
        st.write(f"Years of experience in {resume_file}: {experience}")
        skills, _ = extract_skills(resume_file)
        job_role = predict_job_role(skills)
        sal_data = select_salary_data()
        st.write("The skills that get matched with our keywords:", skills)
        #st.write("Job role prediction: Undetermined")
        display_salary_prediction(sal_data, job_role, experience)
        #st.write(experience, sal_data)
        st.write(f"He is specialised in {job_role}")

# main code
resume_file = select_resume_file()
if st.button("Process"):
    process_resume_file(resume_file)

