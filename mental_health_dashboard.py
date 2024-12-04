import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
<<<<<<< Updated upstream:mental_health_dashboard.py
import plotly.express as px
=======
import matplotlib.pyplot as plt
>>>>>>> Stashed changes:import streamlit as st.py


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

<<<<<<< Updated upstream:mental_health_dashboard.py
with tab4:
    st.header("Koise's Questions")

=======
with tab4
    st.header("Koise's Questions")

def load_data():
    db_path = 'Mental_Health_data.db'
    conn = sqlite3.connect(db_path)

    query = """
    SELECT 
        Answer.SurveyID,
        Question.questionid AS QuestionID,
        Question.questiontext
    FROM 
        Answer
    JOIN 
        Question ON Answer.QuestionID = Question.questionid;
    """
    data = pd.read_sql(query, conn)
    conn.close()
    return data

# Quantify Trends
def quantify_trends(data):
    keywords = ['mental health', 'workplace', 'support', 'challenges', 'attitudes', 'stigma', 'awareness']
    relevant_data = data[data['questiontext'].str.contains('|'.join(keywords), case=False, na=False)]

    attitudes_data = relevant_data[relevant_data['questiontext'].str.contains('attitudes|workplace|mental health', case=False, na=False)]
    support_data = relevant_data[relevant_data['questiontext'].str.contains('support|challenges', case=False, na=False)]

    attitudes_trends = attitudes_data.groupby('SurveyID').size().reset_index(name='AttitudeResponses')
    support_trends = support_data.groupby('SurveyID').size().reset_index(name='SupportResponses')

    trends = pd.merge(attitudes_trends, support_trends, on='SurveyID', how='outer').fillna(0)
    trends['SurveyID'] = trends['SurveyID'].astype(int)
    return trends

# Visualization
def display_dashboard(trends):
    st.title("Attitudes and Employer Support")
    st.markdown("""
    ### Evolution of Mental Health Attitudes and Support Over Time
    This dashboard visualizes the trends in workplace attitudes toward mental health and the support provided by employers over the years.

    #### Insights:
    - **How have the attitudes towards mental health in the tech workplace evolved over time?**
      According to the data, the attitudes toward mental health in the tech workplace spiked in relevance in the year 2016. This suggests an increase in awareness and willingness to discuss mental health openly. After 2016, these attitudes sharply decreased, which suggests either the prioritization of mental health came and went as a fleeting trend, or that employees became satisfied with the employers' increased support concerning mental health. 

    - **How has the relationship between the frequency of challenges and perceived level of support from employers changed over time?**
      According to the data, the relationship has seemingly improved, as indications point to more employees reporting better support from employers. However, apart from a brief and minimal spike in 2017, employer support has remained largely stagnant. This indicates that other factors may be at play when considering the decrease in employee concerns surrounding mental health.
    """)

    st.sidebar.header("Filters")
    selected_years = st.sidebar.multiselect(
        "Select Survey Years", options=trends['SurveyID'].unique(), default=trends['SurveyID'].unique()
    )

    filtered_trends = trends[trends['SurveyID'].isin(selected_years)]

    fig, ax = plt.subplots()
    ax.plot(filtered_trends['SurveyID'], filtered_trends['AttitudeResponses'], marker='o', label="Attitudes")
    ax.plot(filtered_trends['SurveyID'], filtered_trends['SupportResponses'], marker='o', color='orange', label="Support")
    ax.set_title("Attitudes vs. Employer Support Over Time")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Responses")
    ax.legend()
    st.pyplot(fig)

    if not filtered_trends.empty:
        max_attitudes_year = filtered_trends.loc[filtered_trends['AttitudeResponses'].idxmax(), 'SurveyID']
        max_support_year = filtered_trends.loc[filtered_trends['SupportResponses'].idxmax(), 'SurveyID']
        st.markdown(f"""
        - **Year with Most Attitude Responses:** {max_attitudes_year}  
        - **Year with Most Support Responses:** {max_support_year}  
        """)
    else:
        st.markdown("No data available for the selected filters.")

if __name__ == "__main__":
    data = load_data()
    trends = quantify_trends(data)
    display_dashboard(trends)

>>>>>>> Stashed changes:import streamlit as st.py
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