import streamlit as st
import pandas as pd
import numpy as np
import sqlite3


st.header("Group 8 Final Project")
conn = sqlite3.connect("Mental_Health_data.db")

st.subheader('Tabbed Questions by person')
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Julia", "Mac", "David", "Koise", "Chris"])

with tab1:
    st.header("Julia's Questions")

with tab2:
    st.header("Mac's Questions")

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