import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.header("Group 8 Final Project")
conn = sqlite3.connect("Mental_Health_data.db")
cursor = conn.cursor()

st.subheader('Tabbed Questions by person')
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Julia", "Mac", "David", "Koise", "Chris"])

with tab1:
    st.header("Julia's Questions")

with tab2:
	st.header("Mac's Questions")
	age_query = '''
	SELECT 
		AnswerText, 
		COUNT(AnswerText) as Count
	FROM 
		Answer a 
	WHERE 
		QuestionID = 1
	GROUP BY 
		AnswerText 
	ORDER BY 
		COUNT(AnswerText) DESC
    LIMIT 3
	'''
	age_df = pd.read_sql_query(age_query, conn)
	Count = age_df['Count']
	chart = px.bar(age_df, x='AnswerText', y='Count', title= "Count of Top 3 ages who participated in the survey for all years.", labels={'Count': 'Count', 'AnswerText': 'Age'})
	st.subheader("What are the Top 3 ages of those who took the survey in all years?")
	st.caption("Here we can see that the Top 3 ages for those who partook in the survey are 30, 29, and 32.")
	st.plotly_chart(chart)
	query30 = '''
		SELECT 
			COUNT(a.AnswerText) AS Count
		FROM 
			Answer a
		WHERE 
			a.QuestionID = 34 
			AND a.AnswerText = 'Yes' 
			AND EXISTS (
				SELECT 1 
				FROM Answer a2 
				WHERE a2.QuestionID = 1 
				AND a2.AnswerText = '30' 
				AND a2.UserID = a.UserID
			)
		'''
	amount = pd.read_sql_query(query30, conn)

	query29 = '''
		SELECT 
			COUNT(a.AnswerText) AS Count
		FROM 
			Answer a
		WHERE 
			a.QuestionID = 34 
			AND a.AnswerText = 'Yes' 
			AND EXISTS (
				SELECT 1 
				FROM Answer a2 
				WHERE a2.QuestionID = 1 
				AND a2.AnswerText = '29'
				AND a2.UserID = a.UserID
			)
		'''
	amount2 = pd.read_sql_query(query30, conn)

	query32 = '''
		SELECT 
			COUNT(a.AnswerText) AS Count
		FROM 
			Answer a
		WHERE 
			a.QuestionID = 34 
			AND a.AnswerText = 'Yes' 
			AND EXISTS (
				SELECT 1 
				FROM Answer a2 
				WHERE a2.QuestionID = 1 
				AND a2.AnswerText = '32' 
				AND a2.UserID = a.UserID
			)
		'''
	amount3 = pd.read_sql_query(query32, conn)
	total_30 = age_df.loc[age_df['AnswerText'] == '30', 'Count'].values[0]
	yes_30 = amount['Count'].iloc[0]
	total_29 = age_df.loc[age_df['AnswerText'] == '29', 'Count'].values[0]
	yes_29 = amount2['Count'].iloc[0]
	total_32 = age_df.loc[age_df['AnswerText'] == '32', 'Count'].values[0]
	yes_32 = amount3['Count'].iloc[0]
	percentage1 = (yes_30/total_30)*100
	percentage2 = (yes_29/total_29)*100
	percentage3 = (yes_32/total_32)*100
	x = ['30', '29','32']
	y = [percentage1,percentage2,percentage3]
	st.subheader("Of these age groups, what percentage have been diagnosed with a mental health disorder?")
	st.caption("Interestingly, the higher ages have a smaller percentage of having been diagnosed with a mental health disorder. This almost seems to suggest that younger participants in this survey have a higher chance of having been diagnosed.")
	data = pd.DataFrame({
		'Age': x,
		'Percentage': y
	})

	# Create the bar chart
	percentage_chart = px.bar(data, x='Age', y='Percentage', 
				title='Percentage of People who said they have been diagnosed with a mental health disorder by age',
				labels={'Percentage': 'Percentage (%)', 'Age': 'Age'},
				text='Percentage')  # Add text labels to the bars

	# Enhance the chart (optional)
	percentage_chart.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
	percentage_chart.update_layout(yaxis=dict(title='Percentage (%)', range=[0, 100]), 
						xaxis=dict(title='Age'),
						showlegend=False)
	st.plotly_chart(percentage_chart)
	
with tab3:
    st.header("David's Questions")
    
    davidquery = """
		SELECT a.AnswerText, COUNT(a.AnswerText)
		FROM Answer as a
		LEFT Join Question as q
		on a.QuestionID = q.questionid
		WHERE a.QuestionID = 93
		GROUP BY AnswerText;	
		"""
    cursor.execute(davidquery)
    results = cursor.fetchall()
    results = pd.DataFrame(results)
    results.columns = ["Answers", "Count"]
    st.subheader("Do you work remotely (outside of an office) at least 50% of the time?")
    st.dataframe(results, use_container_width=True)
    davidquery2 = '''
			SELECT a.AnswerText, COUNT(a.AnswerText)
			FROM Answer as a
			LEFT Join Question as q
			on a.QuestionID = q.questionid
			WHERE a.QuestionID = 118
			GROUP BY AnswerText;	
			'''
    cursor.execute(davidquery2)
    results = cursor.fetchall()
    results = pd.DataFrame(results)
    results.columns = ["Answers", "Count"]
    st.subheader("Do you work remotely?")
    st.dataframe(results, use_container_width=True) 
    davidquery3 = '''
		SELECT a.AnswerText, COUNT(a.AnswerText)
		FROM Answer as a
		LEFT Join Question as q
		on a.QuestionID = q.questionid
		WHERE a.QuestionID = 31
		GROUP BY AnswerText;	
		'''
    cursor.execute(davidquery3)
    results = cursor.fetchall()
    results = pd.DataFrame(results)
    results.drop([0])
    results.columns = ["Answers", "Count"]
    st.subheader("Have your observations of how another individual who discussed a mental health disorder made you less likely to reveal a mental health issue yourself in your current workplace?")
    st.dataframe(results, use_container_width=True) 
    davidquery4 = '''
		SELECT a.AnswerText, COUNT(a.AnswerText)
		FROM Answer as a
		LEFT Join Question as q
		on a.QuestionID = q.questionid
		WHERE a.QuestionID = 56
		GROUP BY AnswerText;	
		'''
    cursor.execute(davidquery2)
    results = cursor.fetchall()
    results = pd.DataFrame(results)
    results.columns = ["Answers", "Count"]
    st.subheader("Have you observed or experienced an unsupportive or badly handled response to a mental health issue in your current or previous workplace?")
    st.dataframe(results, use_container_width=True) 
    davidquery5 = '''
		SELECT a.AnswerText, COUNT(a.AnswerText)
		FROM Answer as a
		LEFT Join Question as q
		on a.QuestionID = q.questionid
		WHERE a.QuestionID = 83
		GROUP BY AnswerText;
		'''
    cursor.execute(davidquery2)
    results = cursor.fetchall()
    results = pd.DataFrame(results)
    results.columns = ["Answers", "Count"]
    st.subheader("Have you observed or experienced supportive or well handled response to a mental health issue in your current or previous workplace?")
    st.dataframe(results, use_container_width=True)
	

with tab4:
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

        st.header("Filters")
        selected_years = st.multiselect(
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

with tab5:
    st.header("Chris's Questions")

# question -- How does the percentage of tech workers diagnosed with a mental health condition differ between employees and the self-employed?
# employment status - have seeked treatment for mental health
query = '''
SELECT 
	CASE 
		WHEN AnswerText = 1 THEN 'Self-Employed'
		WHEN AnswerText = 0 THEN 'Employed'
	END AS EmploymentStatus,
	COUNT(*) AS 'Has Been Diagnosed with a Mental Health Disorder'
FROM Answer
WHERE QuestionID = 5
	AND AnswerText IN (0,1)
	AND UserID IN (
    SELECT UserID
    FROM Answer
    WHERE QuestionID = 34 AND AnswerText = 'Yes'
  )
GROUP BY EmploymentStatus;
'''
df = pd.read_sql_query(query, conn)

# employment status - have not seeked mental health treatment
query2 = '''
SELECT 
	CASE 
		WHEN AnswerText = 1 THEN 'Self-Employed'
		WHEN AnswerText = 0 THEN 'Employed'
	END AS EmploymentStatus,
	COUNT(*) AS 'Has Not Been Diagnosed with a Mental Health Disorder'
FROM Answer
WHERE QuestionID = 5
	AND AnswerText IN (0,1)
	AND UserID IN (
    SELECT UserID
    FROM Answer
    WHERE QuestionID = 34 AND AnswerText = 'No'
  )
GROUP BY EmploymentStatus;
'''
df2 = pd.read_sql_query(query2, conn)

# question - How do the percentages of tech employees who have sought treatment for a mental health condition differ by gender?
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

#merge employment dataframes to get percentage and data table
df_employment_combined = pd.merge(df, df2, on='EmploymentStatus')
df_employment_combined['Total'] = (df_employment_combined['Has Been Diagnosed with a Mental Health Disorder'] + df_employment_combined['Has Not Been Diagnosed with a Mental Health Disorder'])
df_employment_combined['Percentage Who Have Been Diagnosed'] = (df_employment_combined['Has Been Diagnosed with a Mental Health Disorder'] / df_employment_combined['Total'] * 100)
#merge gender dataframes to get percentage and data table
df_gender_combined = pd.merge(df3, df4, on='Gender')
df_gender_combined['Total'] = (df_gender_combined['Have Sought Mental Health Treatment'] + df_gender_combined['Have Not Sought Mental Health Treatment'])
df_gender_combined['Percentage Who Have Sought Mental Health Treatment'] = (df_gender_combined['Have Sought Mental Health Treatment'] / df_gender_combined['Total'] * 100)
with tab5:
    st.subheader("How do the percentages of tech employees seeking treatment for mental health conditions differ by gender?")
    st.text("From this chart, there are distinct differences among the gender demographics. Female tech workers reported the highest rate of seeking treatment at 72.9%, followed by those identifying as other at 62.4%, and male tech workers at 51.1%. Among the three genders surveyed—male, female, and other—the percentage of individuals seeking mental health support is notably high. This data backs the commonly told claim that men are less likely to seek treatment for mental health concerns.")
    selected_gender = st.multiselect("Select Gender to Show", options=df_gender_combined['Gender'].unique(), default=df_gender_combined['Gender'].unique())
    filtered_gender = df_gender_combined[df_gender_combined['Gender'].isin(selected_gender)]
    basic_bar_5 = px.bar(filtered_gender, x='Gender', y='Percentage Who Have Sought Mental Health Treatment')
    st.plotly_chart(basic_bar_5)
    with st.expander("See Data Table"):
        st.write(df_gender_combined)
with tab5:
     st.subheader("How does the percentage of tech workers diagnosed with a mental health condition differ between employees and the self-employed?")
     st.text("Observing this chart, there is a negligible difference in the percentages of self-employed and employed tech workers diagnosed with a mental health disorder. Employed individuals show a slightly higher rate at 65.6% compared to 62.5% for the self-employed. Both groups exhibit strikingly high rates of mental health diagnoses.")
     basic_bar_6 = px.bar(df_employment_combined, x='EmploymentStatus', y='Percentage Who Have Been Diagnosed')
     st.plotly_chart(basic_bar_6)
     with st.expander("See Data Table"):
        st.write(df_employment_combined)