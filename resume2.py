import streamlit as st
import os
import pandas as pd
import re
import nltk
import spacy
import en_core_web_sm
import pandas as pd
import os
import docx
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
import docx2txt

def file_selector(folder_path='Resumes'):
	filename=os.listdir(folder_path)
	selected_filename=st.selectbox('select a file',filename)
	return os.path.join(folder_path,selected_filename)
filename=file_selector()

if st.button("Process"):
	if filename.endswith(".pdf"):
	
		st.write("You selected `%s` " %filename)

		Skills_extraction=ResumeParser(filename).get_extracted_data()
		
		extract_for_YoE=resumeparse.read_file(filename)
		st.write(extract_for_YoE['total_exp'])
		st.write("Name of the Candidate: ",Skills_extraction['name'])
		st.write("Skills----",Skills_extraction['skills'])
		st.write("Years of Experience-----",extract_for_YoE['total_exp'])

		Skills_extracted=Skills_extraction['skills']
	

		skills_reqd_DS=['machine learning','data mining','predictive modeling', 'statistical analysis', 'data visualization', 'natural language processing', 'big data', 'data warehousing', 'sql', 'python/r programming', 'deep learning', 'artificial intelligence', 'data analytics', 'a/b testing', 'feature engineering', 'etl processes', 'time series analysis', 'regression analysis', 'cluster analysis', 'decision trees','power bi']
		skills_reqd_HR=['ats','applicant tracking systems','job postings', 'sourcing','source' ,'interviewing skills', 'hiring process', 'job descriptions', 'talent acquisition', 'diversity and inclusion', 'background checks', 'onboarding','hr consulting' ,'recruiting','recruiter','shortlisting','interviewing','end to end recruitment','deadline','reporting','hire','walk-in drives','phone interviewing',' candidate management systems','decisionmaking','management','psychology','monitoring''cms','screening resumes','lateral']
		skills_reqd_sales=['sales', 'account management', 'client relationship management', 'sales forecasting', 'sales strategy', 'sales negotiations', 'pipeline management', 'territory management', 'customer acquisition', 'sales performance', 'sales reporting','website sales','cilents','metrics','inside sales','strategic content development','presales executives','cold calling','executive',' marketing','business development','crm','market research', 'website sales', 'inside sales','negotiations','customer service']

		Skills_extracted=[x.lower() for x in Skills_extracted]
		Skills_extracted=[num.strip(' ') for num in Skills_extracted]
		Skills_extracted=[num.strip(')') for num in Skills_extracted]
		Skills_extracted=[num.strip('(') for num in Skills_extracted]
		
		res={'skills_reqd_DataScientist':[],'skills_reqd_HR':[],'skills_reqd_sales':[]}
		for i in Skills_extracted:
			if i in skills_reqd_DS:
				res['skills_reqd_DataScientist'].append(str(i))
			if i in skills_reqd_HR:
				res['skills_reqd_HR'].append(str(i))
			if i in skills_reqd_sales:
				res['skills_reqd_sales'].append(str(i))
		st.write("The Skills that get Matched with our Keywords",res)
	   

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
		#a=extract_for_YoE['total_exp']
		#st.write(a)


		sal_data=pd.read_csv(r"Sal_data.csv")
		sal_data.info()

		sal_data=pd.DataFrame(sal_data)
		

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
		resume_dir = "Resumes"
		a=extract_for_YoE['total_exp']
		for filename in os.listdir(folder_path):
    # Extract the experience level from the resume
    # (assuming that you have already implemented this step)
			experience_level = resumeparse.read_file(filename)

    # Determine the folder where the resume should be stored
			if experience_level['total_exp']<= 2:
				folder_name = "junior"
			elif 2<experience_level['total_exp']<=4:
				folder_name = "mid"
			elif 4<experience_level['total_exp']<=10:
				folder_name = "senior"
			else:
				folder_name = "expert"

    # Create the folder if it doesn't exist
			folder_path = os.path.join("https://github.com/shanthosh-SP/resume-parser1/tree/main/Categories", folder_name)
			os.makedirs(folder_path, exist_ok=True)

    # Move the resume to the appropriate folder	
			resume_path = os.path.join(resume_dir, filename)
			new_resume_path = os.path.join(folder_path, filename)
			os.rename(resume_path, new_resume_path)
	elif filename.endswith(".doc") or filename.endswith(".docx"):

		doc = docx.Document(filename)
		text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
# Regular expression pattern to match years of experience
		pattern = r"(\d+)\+?\s*(years?|yrs)"
# Search for matches in the document text
		matches = re.findall(pattern, text, re.IGNORECASE)
# Extract the years of experience from the first match
		a= int(matches[0][0]) if matches else 0
		st.write(f"Years of experience in {filename}: {a}")

		Skills_extraction=ResumeParser(filename).get_extracted_data()
		extract_for_YoE=resumeparse.read_file(filename)
		
		st.write("Name of the Candidate: ",Skills_extraction['name'])
		st.write("Skills----",Skills_extraction['skills'])
		Skills_extracted=Skills_extraction['skills']

		skills_reqd_DS=['machine learning','data mining','predictive modeling', 'statistical analysis', 'data visualization', 'natural language processing', 'big data', 'data warehousing', 'sql', 'python/r programming', 'deep learning', 'artificial intelligence', 'data analytics', 'a/b testing', 'feature engineering', 'etl processes', 'time series analysis', 'regression analysis', 'cluster analysis', 'decision trees','power bi']
		skills_reqd_HR=['ats','applicant tracking systems','job postings', 'sourcing','source' ,'interviewing skills', 'hiring process', 'job descriptions', 'talent acquisition', 'diversity and inclusion', 'background checks', 'onboarding','hr consulting' ,'recruiting','recruiter','shortlisting','interviewing','end to end recruitment','deadline','reporting','hire','walk-in drives','phone interviewing',' candidate management systems','decisionmaking','management','psychology','monitoring''cms','screening resumes','lateral']
		skills_reqd_sales=['sales', 'account management', 'client relationship management', 'sales forecasting', 'sales strategy', 'sales negotiations', 'pipeline management', 'territory management', 'customer acquisition', 'sales performance', 'sales reporting','website sales','cilents','metrics','inside sales','strategic content development','presales executives','cold calling','executive',' marketing','business development','crm','market research', 'website sales', 'inside sales','negotiations','customer service']

		Skills_extracted=[x.lower() for x in Skills_extracted]
		Skills_extracted=[num.strip(' ') for num in Skills_extracted]
		Skills_extracted=[num.strip(')') for num in Skills_extracted]
		Skills_extracted=[num.strip('(') for num in Skills_extracted]
		
		res={'skills_reqd_DataScientist':[],'skills_reqd_HR':[],'skills_reqd_sales':[]}
		for i in Skills_extracted:
			if i in skills_reqd_DS:
				res['skills_reqd_DataScientist'].append(str(i))
			if i in skills_reqd_HR:
				res['skills_reqd_HR'].append(str(i))
			if i in skills_reqd_sales:
				res['skills_reqd_sales'].append(str(i))
		st.write("The Skills that get Matched with our Keywords",res)
	   

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
		#a=extract_for_YoE['total_exp']
		#st.write(a)


		sal_data=pd.read_csv(r"Sal_data.csv")
		sal_data.info()

		sal_data=pd.DataFrame(sal_data)
		

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

			
		final(a,b)

# 	nlp = spacy.load("en_core_web_sm")
# 	import codecs


# 	encodings = ['utf-8', 'utf-8-sig', 'cp1252', 'latin1', 'iso-8859-1']
# 	for enc in encodings:
# 		try:
# 			with codecs.open(filename, 'r', encoding=enc) as file:
# 				text = file.read()
# 				print(f"File '{filename}' opened with encoding '{enc}'.")
# 			break
# 		except UnicodeDecodeError:
# 			print(f"Could not open file '{filename}' with encoding '{enc}'. Trying next...")


# # Load a document from a file
# 	doc = nlp(open(filename, encoding=enc).read())

# # Extract the text from the document
# 	text = doc.text
# 	import re

# 	def extract_experience(text):

# 		pattern = re.compile(r'(?i)(\d+)[+ -]? *(?:year|yr)s?(?: of|\'|\’)?(?:\s|-)*(?:experience|exp)')
# 		match = pattern.search(text)
# 		if match:
# 			a=int(match.group(1))
# 			return print(a)
# 		else:
# 			return None

