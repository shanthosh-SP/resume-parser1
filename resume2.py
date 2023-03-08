import streamlit as st
import os
from github import Github
import pandas as pd
import github3
import nltk
import spacy
import en_core_web_sm
import pandas as pd
from pathlib import Path
import fitz

# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('universal_tagset')
# nltk.download('maxent_ne_chunker')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('brown')
from resume_parser import resumeparse
from pyresparser import ResumeParser

gh = github3.login(username="shanthosh", password="Sandy$$$12345")

def file_selector(folder_path='Resumes'):
	st.title("File Uploader")
	filename=os.listdir(folder_path)
	selected_filename=st.selectbox('select a file',filename)
	return os.path.join(folder_path,selected_filename)
filename=file_selector()

if st.button("Process"):
	
	st.write("You selected `%s` " %filename)
	


	Skills_extraction=ResumeParser(filename).get_extracted_data()
	
	extract_for_YoE=resumeparse.read_file(filename)
	#st.write("Name of the Candidate: ",Skills_extraction['name'])
#st.write("Skills----",Skills_extraction['skills'])
	#st.write("Years of Experience-----",extract_for_YoE['total_exp'])

	Skills_extracted=Skills_extraction['skills']
	
	#st.write(extract_for_YoE)
	#st.write('=====')
	#st.write(Skills_extraction)
	skills_reqd_DS=['machine learning','data mining','predictive modeling', 'statistical analysis', 'data visualization', 'natural language processing', 'big data', 'data warehousing', 'sql', 'python/r programming', 'deep learning', 'artificial intelligence', 'data analytics', 'a/b testing', 'feature engineering', 'etl processes', 'time series analysis', 'regression analysis', 'cluster analysis', 'decision trees','power bi']
	skills_reqd_HR=['ats','applicant tracking systems','job postings', 'sourcing','source' ,'interviewing skills', 'hiring process', 'job descriptions', 'talent acquisition', 'diversity and inclusion', 'background checks', 'onboarding','hr consulting' ,'recruiting','recruiter','shortlisting','interviewing','end to end recruitment','deadline','reporting','hire','walk-in drives','phone interviewing',' candidate management systems','decisionmaking','management','psychology','monitoring''cms','screening resumes','lateral']
	skills_reqd_sales=['sales', 'account management', 'client relationship management', 'sales forecasting', 'sales strategy', 'sales negotiations', 'pipeline management', 'territory management', 'customer acquisition', 'sales performance', 'sales reporting','website sales','cilents','metrics','inside sales','strategic content development','presales executives','cold calling','executive',' marketing','business development','crm','market research', 'website sales', 'inside sales','negotiations','customer service']

	Skills_extracted=[x.lower() for x in Skills_extracted]
	Skills_extracted=[num.strip(' ') for num in Skills_extracted]
	Skills_extracted=[num.strip(')') for num in Skills_extracted]
	Skills_extracted=[num.strip('(') for num in Skills_extracted]

#st.write("Skills",Skills_extracted)
	res={'skills_reqd_DataScientist':[],'skills_reqd_HR':[],'skills_reqd_sales':[]}
	for i in Skills_extracted:
		if i in skills_reqd_DS:
			res['skills_reqd_DataScientist'].append(str(i))
		if i in skills_reqd_HR:
			res['skills_reqd_HR'].append(str(i))
		if i in skills_reqd_sales:
			res['skills_reqd_sales'].append(str(i))
	#st.write(res)
   

	HR=0
	DS=0
	sales=0
	x=1
	c="He is Specialised in"
	b=""
	for i,j in res.items():

		if x==1:
			DS=len(j)
		if x==2:
			HR=len(j)
		if x==3:
			sales=len(j)
		x+=1
	if (HR>DS and HR>sales):
		b="HR"
		print('He is applicable for HR role')
	if (DS>HR and DS>sales):
		b="DataScientist"
		print('He is applicable for DataScientist role')
	if (sales>HR and sales>DS):
		b="Sales"
		print('He is applicable for Sales role')

	st.write(c+' '+b)


	sal_data=pd.read_csv(r"Sal_data.csv")
	sal_data.info()

	sal_data=pd.DataFrame(sal_data)
	a=extract_for_YoE['total_exp']

	st.write(a,b)

	def final(a,b):
		
		if a<=2 and b=="DataScientist":
			color_and_shape = sal_data.loc[(sal_data['Job Role'] == "DataScientist") & (sal_data['YoE'] == "0-2")]
			st.write(color_and_shape)


		if 2<a<=4 and b=="DataScientist":
			color_and_shape = sal_data.loc[(sal_data['Job Role'] == "DataScientist") & (sal_data['YoE'] == "2-4")]
			st.write(color_and_shape)
			

		if 4< a<=10 and b=="DataScientist":
			color_and_shape = sal_data.loc[(sal_data['Job Role'] == "DataScientist") & (sal_data['YoE'] == "5-10")]
			st.write(color_and_shape)
		if a>=11 and b=="DataScientist":
			color_and_shape = sal_data.loc[(sal_data['Job Role'] == "DataScientist") & (sal_data['YoE'] == "10+")]
			st.write(color_and_shape)
					
		if a<=2 and b=="HR":
			color_and_shape = sal_data.loc[(sal_data['Job Role'] == "HR") & (sal_data['YoE'] == "0-2")]
			st.write(color_and_shape)
			

		if 2<a<=4 and b=="HR":
			color_and_shape = sal_data.loc[(sal_data['Job Role'] == "HR") & (sal_data['YoE'] == "3-4")]
			st.write(color_and_shape)
			

		if 4<a<=10 and b=="HR":
			color_and_shape = sal_data.loc[(sal_data['Job Role'] == "HR") & (sal_data['YoE'] == "5-10")]
			st.write(color_and_shape)
	
		if a>=11 and b=="HR":
			color_and_shape = sal_data.loc[(sal_data['Job Role'] == "HR") & (sal_data['YoE'] == "10+")]
			st.write(color_and_shape)
		if a<=2 and b=="Sales":
			color_and_shape = sal_data.loc[(sal_data['Job Role'] == "Sales") & (sal_data['YoE'] == "0-2")]
			st.write(color_and_shape)
		if 2<a <=4 and b=="Sales":
			color_and_shape = sal_data.loc[(sal_data['Job Role'] == "Sales") & (sal_data['YoE'] == "3-4")]
			st.write(color_and_shape)

		if 4<a <=10 and b=="Sales":
			color_and_shape = sal_data.loc[(sal_data['Job Role'] == "Sales") & (sal_data['YoE'] == "5-10")]
			st.write(color_and_shape)


		if a>=11 and b=="Sales":
			color_and_shape = sal_data.loc[(sal_data['Job Role'] == "Sales") & (sal_data['YoE'] == "10+")]
			st.write(color_and_shape)

		
	final(extract_for_YoE['total_exp'],b)
	
	

# Initialize a PyGithub instance
	g = Github("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")

# Get the repository
	repo = g.get_repo("shanthosh-sp/resume-parser1")
	if 2<a<=4:
		file_path = "Categories/Intermediate"
		file_name = filename
		with open(filename, 'rb') as f:
			pdf_data = f.read()
			pdf_reader = fitz.open("pdf", pdf_data)
			num_pages = pdf_reader.page_count
		for page_num in range(num_pages):
			page_obj = pdf_reader.load_page(page_num)
			page_contents = page_obj.get_text("text").encode('utf-8')
			repo.create_file(f"{file_path}/{file_name}",f"Added {file_name}",file_content,branch="main")
	
	
	if a<=2:
		with open(filename, 'rb') as f:
			pdf_data = f.read()
			pdf_reader = fitz.open("pdf", pdf_data)
			num_pages = pdf_reader.page_count
		for page_num in range(num_pages):
			page_obj = pdf_reader.load_page(page_num)
			page_contents = page_obj.get_text("text").encode('utf-8')
			folder_path = "categories/fresher/"	
		#file_contents = file_selector.read()
		#file_name = file_selector.name
			repo = gh.repository("shanthosh", "resume-parser1")
			repo.create_file(folder_path, filename, page_contents)
			st.write("Resume saved successfully.")
	if 2<a<=4:
		with open(filename, 'rb') as f:
			pdf_data = f.read()
			pdf_reader = fitz.open("pdf", pdf_data)
			num_pages = pdf_reader.page_count
		for page_num in range(num_pages):
			page_obj = pdf_reader.load_page(page_num)
			page_contents = page_obj.get_text("text").encode('utf-8')
			folder_path = "categories/fresher/"	
		#file_contents = file_selector.read()
		#file_name = file_selector.name
			try:
				repo = gh.repository("shanthosh-sp", "resume-parser1")
				repo.create_file(folder_path, filename, page_contents)
				st.write("Resume saved successfully.")
			except github3.exceptions.NotFoundError as e:
				st.write(f"Error: {e}")

	if 4<a<=10:
		
		with open(filename, 'rb') as f:
			pdf_data = f.read()
			pdf_reader = fitz.open("pdf", pdf_data)
			num_pages = pdf_reader.page_count
		for page_num in range(num_pages):
			page_obj = pdf_reader.load_page(page_num)
			page_contents = page_obj.get_text("text").encode('utf-8')
			folder_path = "categories/fresher/"	
		#file_contents = file_selector.read()
		#file_name = file_selector.name
			repo = gh.repository("shanthosh-SP", "resume-parser1")
			repo.create_file(folder_path, filename, page_contents)
			st.write("Resume saved successfully.")
	if a<=11:
		
		with open(filename, 'rb') as f:
			pdf_data = f.read()
			pdf_reader = fitz.open("pdf", pdf_data)
			num_pages = pdf_reader.page_count
		for page_num in range(num_pages):
			page_obj = pdf_reader.load_page(page_num)
			page_contents = page_obj.get_text("text").encode('utf-8')
			folder_path = "categories/fresher/"	
		#file_contents = file_selector.read()
		#file_name = file_selector.name
			try:
				repo = gh.repository("shanthosh-sp", "resume-parser1")
				repo.create_file(folder_path, filename, page_contents)
				st.write("Resume saved successfully.")
			except github3.exceptions.NotFoundError as e:
				st.write(f"Error: {e}")
	
	with st.form("myform"):
		Submit = st.form_submit_button(label='Submit')
		st.markdown("**The file is sucessfully Uploaded.**")
	
	if Submit:
		st.markdown("**The file is sucessfully Uploaded.**")
		if a<=2:
			folder_path = 'Categories/Fresher'
			fil=os.listdir(folder_path)
			save_path = Path(folder_path, selected_filename.name)
			with open(fil, mode='wb') as w:
				w.write(selected_file.getvalue())
			if fil.exists():
        			st.success(f'File {selected_filename.name} is successfully saved!')
		if 2<a<4:
			folder_path = 'Categories/Fresher'
			fil=os.listdir(folder_path)
			save_path = Path(folder_path, selected_filename.name)
			with open(fil, mode='wb') as w:
				w.write(selected_filename.getvalue())
			if fil.exists():
        			st.success(f'File {File.name} is successfully saved!')
		if 4<a<=10:
			folder_path = 'Categories/Fresher'
			fil=os.listdir(folder_path)
			save_path = Path(folder_path, selected_filename.name)
			with open(fil, mode='wb') as w:
				w.write(selected_filename.getvalue())
			if fil.exists():
        			st.success(f'File {selected_filename.name} is successfully saved!')
		if a>=11:
			save_folder = 'Categories/Advanced'
			save_path = Path(save_folder, selected_filename.name)
			with open(save_path, mode='wb') as w:
				w.write(selected_filename.getvalue())
			if save_path.exists():
        			st.success(f'File {selected_filename.name} is successfully saved!')
