import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import plotly.express as px


st.header("Group 8 Final Project")
conn = sqlite3.connect("Mental_Health_data.db")

st.subheader('Tabbed Questions by person')
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Julia", "Mac", "David", "Koise", "Chris"])

with tab1:
    st.header("Julia's Questions")

with tab2:
    st.header("Mac's Questions")
    age_query = '''
	SELECT 
		AnswerText, 
		COUNT(AnswerText)
	FROM 
		Answer a 
	WHERE 
		QuestionID = 1
	GROUP BY 
		AnswerText 
	ORDER BY 
		COUNT(AnswerText) DESC
	'''
    age_df = pd.read_sql_query(age_query, conn)
    

with tab3:
    st.header("David's Questions")

with tab4:
    st.header("Koise's Questions")

with tab5:
    st.header("Chris's Questions")

#Question -- How do mental health outcomes differ between self-employed individuals and employed individuals in the tech industry?
# employment status - have seeked treatment for mental health
query = '''
SELECT 
	CASE 
		WHEN AnswerText = 1 THEN 'Self-Employed'
		WHEN AnswerText = 0 THEN 'Employed'
	END AS EmploymentStatus,
	COUNT(*) AS 'Have Sought Mental Health Treatment'
FROM Answer
WHERE QuestionID = 5
	AND AnswerText IN (0,1)
	AND UserID IN (
    SELECT UserID
    FROM Answer
    WHERE QuestionID = 7 AND AnswerText = 1
  )
GROUP BY EmploymentStatus;
'''
df = pd.read_sql_query(query, conn)
print(df)

# employment status - have not seeked mental health treatment
query2 = '''
SELECT 
	CASE 
		WHEN AnswerText = 1 THEN 'Self-Employed'
		WHEN AnswerText = 0 THEN 'Employed'
	END AS EmploymentStatus,
	COUNT(*) AS 'Have Not Sought Mental Health Treatment'
FROM Answer
WHERE QuestionID = 5
	AND AnswerText IN (0,1)
	AND UserID IN (
    SELECT UserID
    FROM Answer
    WHERE QuestionID = 7 AND AnswerText = 0
  )
GROUP BY EmploymentStatus;
'''
df2 = pd.read_sql_query(query2, conn)
print(df2)

# gender -- have seeked help
query3 = '''
SELECT
	CASE
		WHEN AnswerText = 'Male'
			THEN 'Male'
		WHEN AnswerText = 'Female'
			THEN 'Female'
        WHEN AnswerText = -1
			THEN 'NA'
		ELSE
			'Other'
	END AS Gender,
	COUNT(*) AS 'Have Sought Mental Health Treatment'
FROM Answer
WHERE questionid = 2 AND Gender IN ('Male', 'Female', 'Other') AND UserID IN(
SELECT UserID
FROM Answer
WHERE questionid = 7 AND AnswerText = 1
)
GROUP BY Gender
'''
df3 = pd.read_sql_query(query3, conn)
print(df3)

# gender -- have not seeked help
query4 = '''
SELECT
	CASE
		WHEN AnswerText = 'Male'
			THEN 'Male'
		WHEN AnswerText = 'Female'
			THEN 'Female'
        WHEN AnswerText = -1
			THEN 'NA'
		ELSE
			'Other'
	END AS Gender,
	COUNT(*) AS 'Have Not Sought Mental Health Treatment'
FROM Answer
WHERE questionid = 2 AND Gender IN ('Male', 'Female', 'Other') AND UserID IN(
SELECT UserID
FROM Answer
WHERE questionid = 7 AND AnswerText = 0
)
GROUP BY Gender
'''

df4 = pd.read_sql_query(query4, conn)
print(df4)
conn.close()

df['EmploymentStatus'] = df['EmploymentStatus'].astype('string')
df['Have Sought Mental Health Treatment'] = df['Have Sought Mental Health Treatment'].astype('string')
print(df.info())

df2['EmploymentStatus'] = df2['EmploymentStatus'].astype('string')
df2['Have Not Sought Mental Health Treatment'] = df2['Have Not Sought Mental Health Treatment'].astype('string')

basic_bar = px.bar(df, x='EmploymentStatus', y='Have Sought Mental Health Treatment')
basic_bar2 = px.bar(df2, x='EmploymentStatus', y='Have Not Sought Mental Health Treatment')

col1, col2 = st.columns(2)

with tab5:
	st.subheader("Question 1")
	col1, col2 = st.columns(2)
	with col1:
		st.plotly_chart(basic_bar)
	with col2:
		st.plotly_chart(basic_bar2)