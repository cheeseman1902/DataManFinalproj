import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import plotly.express as px
import matplotlib.pyplot as plt


st.set_page_config(layout="wide")
st.title("Group 8 Final Project")
conn = sqlite3.connect("Mental_Health_data.db")
cursor = conn.cursor()

st.header('Tabbed Questions by person')
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Julia", "David", "Koise", "Chris", "Mac"])

with tab1:
    st.header("Julia's Questions")
    
    query_profiling = """
    SELECT *
    FROM Answer 
    WHERE QuestionId = 9 AND AnswerText = 1
    # There are 1,400 rows satisfying the criteria as employees from the techs corporate compared to the total database amount of 3,000, so the valid employees percentage = 1,400 / 3,000 = 46.67%.

    SELECT *
    FROM Answer
    WHERE UserID IN (
        SELECT UserID
        FROM Answer
        WHERE (QuestionID = 9 AND AnswerText = 1)
        OR (QuestionID = 13 AND AnswerText = 1)
        GROUP BY UserID
        HAVING COUNT(DISTINCT QuestionID) = 2
    )
    ORDER BY UserID ASC
    # There are 909 persons satisfying working in the Techs Corporate and primary role is the IT-relative.

    SELECT 
        CASE 
            WHEN LOWER(AnswerText) = 'male' THEN 'Male'
            WHEN LOWER(AnswerText) = 'female' THEN 'Female'
            ELSE 'Others'
        END AS AnswerCategory,
        COUNT(*) AS response_count
    FROM Answer
    WHERE QuestionID = 2
    AND UserID IN (
        SELECT UserID
        FROM Answer
        WHERE (QuestionID = 9 AND AnswerText = 1)
        OR (QuestionID = 13 AND AnswerText = 1)
        GROUP BY UserID
        HAVING COUNT(DISTINCT QuestionID) = 2
    )
    GROUP BY AnswerCategory
    ORDER BY response_count DESC
    # Among these 909 persons, 606 are male, 255 are female, and other 49 are sexual minorities.
    # This is a male-dominated field and seeks ambitious personalities. We could make reasonable assumptions that acknowledging mental health issues is a shame inside IT companies' culture.
    """

    # Queries for each question
    query_1 = """
    WITH Counts AS (
        SELECT 
            CASE 
                WHEN A1.AnswerText = '1' THEN 'IT Company'
                WHEN A1.AnswerText = '0' THEN 'Non-IT Company'
            END AS CompanyType,
            CASE 
                WHEN A2.AnswerText = 'Yes' THEN 'Yes'
                WHEN A2.AnswerText = 'No' THEN 'No'
                ELSE 'Uncertain'
            END AS MentalHealthIssue,
            COUNT(*) AS Count
        FROM Answer A1
        JOIN Answer A2 ON A1.UserID = A2.UserID
        WHERE A1.QuestionID = 9 -- IT company
        AND A2.QuestionID = 33 -- Current mental health disorder
        GROUP BY CompanyType, MentalHealthIssue
    ),
    Totals AS (
        SELECT 
            CompanyType,
            SUM(Count) AS TotalCount
        FROM Counts
        GROUP BY CompanyType
    )
    SELECT 
        C.CompanyType,
        C.MentalHealthIssue,
        C.Count,
        (C.Count * 100.0 / T.TotalCount) AS Percentage
    FROM Counts C
    JOIN Totals T ON C.CompanyType = T.CompanyType;
    """

    query_2 = """
    WITH Counts AS (
        SELECT 
            CASE 
                WHEN A1.AnswerText = '1' THEN 'IT Company'
                WHEN A1.AnswerText = '0' THEN 'Non-IT Company'
            END AS CompanyType,
            A2.AnswerText AS WorkInterferenceLevel,
            COUNT(*) AS Count
        FROM Answer A1
        JOIN Answer A2 ON A1.UserID = A2.UserID
        WHERE A1.QuestionID = 9  -- IT company
        AND A2.QuestionID = 92 -- Mental health condition interferes with work
        AND A2.AnswerText IN ('Never', 'Rarely', 'Sometimes', 'Often') -- Valid answers
        GROUP BY CompanyType, WorkInterferenceLevel
    ),
    Totals AS (
        SELECT 
            CompanyType,
            SUM(Count) AS TotalCount
        FROM Counts
        GROUP BY CompanyType
    )
    SELECT 
        C.CompanyType,
        C.WorkInterferenceLevel,
        C.Count,
        (C.Count * 100.0 / T.TotalCount) AS Percentage
    FROM Counts C
    JOIN Totals T ON C.CompanyType = T.CompanyType;
    """

    query_10 = """
    WITH Counts AS (
        SELECT 
            CASE 
                WHEN A1.AnswerText = '1' THEN 'IT Company'
                WHEN A1.AnswerText = '0' THEN 'Non-IT Company'
            END AS CompanyType,
            CASE 
                WHEN A2.AnswerText = 'Yes' THEN 'Yes'
                WHEN A2.AnswerText = 'No' THEN 'No'
                ELSE 'Uncertain'
            END AS Response,
            COUNT(*) AS Count
        FROM Answer A1
        JOIN Answer A2 ON A1.UserID = A2.UserID
        WHERE A1.QuestionID = 9 -- IT company
        AND A2.QuestionID = 10 -- Mental health benefits
        GROUP BY CompanyType, Response
    ),
    Totals AS (
        SELECT 
            CompanyType,
            SUM(Count) AS TotalCount
        FROM Counts
        GROUP BY CompanyType
    )
    SELECT 
        C.CompanyType,
        C.Response,
        C.Count,
        (C.Count * 100.0 / T.TotalCount) AS Percentage
    FROM Counts C
    JOIN Totals T ON C.CompanyType = T.CompanyType;
    """

    # Execute queries and load results into DataFrames
    results_1 = pd.read_sql_query(query_1, conn)
    results_2 = pd.read_sql_query(query_2, conn)
    results_10 = pd.read_sql_query(query_10, conn)

    # Streamlit UI
    st.title("Mental Health Data Analysis")
    st.write("This application visualizes mental health data across IT and Non-IT companies.")

    # Question One: Current mental health disorder (Question 33)
    st.subheader("Question One: Current Mental Health Disorder")
    st.dataframe(results_1)

    st.bar_chart(
        data=results_1.set_index("MentalHealthIssue").pivot(columns="CompanyType", values="Percentage"),
        use_container_width=True,
    )

    question_1_comment = st.text_area(
        """Add your comments or observations for Question One:
        The SQL results present that the IT company employee's mental health disorder answer "yes" percentage is lower than those from non-IT companies.
        It could be interpreted as:
        1. IT company pays more attention to their employees' mental health status and will discover it and solve it at the early stage.
        2. IT company has a more fierce competition environment, where a "yes" response might damage the respondent's career path and reputation among colleagues and direct supervisors."""
    )

    # Question Two: Work Interference Level (Question 92)
    st.subheader("Question Two: Mental Health Work Interference")
    st.dataframe(results_2)

    st.bar_chart(
        data=results_2.set_index("WorkInterferenceLevel").pivot(columns="CompanyType", values="Percentage"),
        use_container_width=True,
    )

    # Add a text box for additional comments
    question_2_comment = st.text_area(
        "Add your comments or observations for Question Two: "
        "According to Question 92, there are similar levels of responses from the IT and non-IT companies saying the 'sometimes' and 'often' mental health will interfere with working productivity, with the sum proportion around 60%. "
        "That means mental health will cause negative impacts on working no matter what kind of corporate and industry we are."
    )

    # Question One Addition: Mental Health Benefits (Question 10)
    st.subheader("Question One Addition: Mental Health Benefits")
    st.dataframe(results_10)

    st.bar_chart(
        data=results_10.set_index("Response").pivot(columns="CompanyType", values="Percentage"),
        use_container_width=True,
    )

    # Add a text box for additional comments
    question_10_comment = st.text_area(
        """Add your comments or observations for Question One Addition:
        For the two opposite explanations of the results of Question 9, we look through Question 10 and make conclusions that the first assumption could be rejected due to 'including the mental health into the corporate insurance plan' being lower in IT companies compared to that in non-IT companies.
        Another reasonable explanation is that, except for the wolf culture and intensive competition in IT companies, almost one third of the employees have no clear idea of their mental health support resources and lack awareness of discovering and solving mental health problems."""
    )

    # Add a text box for conclusion and business insights
    business_comment = st.text_area(
        """Therefore, as the human resource and direct managers of IT companies, they had better appropriately define the mental health and its importance to their employees, for their personal well-being or corporate-level consistently outstanding performances.
        Additionally, they should provide more acceptable and non-intrusive methods to offer timely support and consultancy.
        As employees of IT companies, they had better build awareness and mindset of the mental health effects on their personal life and career paths, and seek help proactively if feeling overwhelmed or experiencing physical reactions to extreme anxiety, instead of pretending non-existence or delaying treatment due to over-concern about colleagues' and supervisors' negative comments."""
    )

with tab2:
    st.header("David's Questions")
    st.subheader("Do people with mental health issues prefer working in-office or remote?")
    col1, col2 = st.columns(2)
    with col1:
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
        st.bar_chart(data=results, x='Answers', y='Count')
        with st.expander("See Data Table"):
            st.write(results)
    with col2:
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
        st.bar_chart(data=results, x='Answers', y='Count')
        with st.expander("See Data Table"):
            st.write(results)
    st.text('The graphs show that while most responders to the survey do not work remote the majority of the time, the majority of them work remote sometimes. This can perhaps be attributed to the shift in work environments following the pandemic, where many people transitioned to hybrid-style work patterns.')
    st.subheader('Have more positive or negative discussions surrounding mental health in the workplace been observed?')
    ncol1, ncol2, ncol3 = st.columns(3)
    st.text('The graphs show that survey responders have observed and experienced more negative workplace responses to mental health issues than positive ones. Notably, more than twice as many responders answered "no" or "not sure" to seeing negative responses than positive ones, which could suggest that a negative response can be more subtle or unnoticable than the alternative.')
    with ncol1:
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
        results = pd.DataFrame(results)[1:4]
        results.columns = ["Answers", "Count"]
        st.subheader("Have your observations of how another individual who discussed a mental health disorder made you less likely to reveal a mental health issue yourself in your current workplace?")
        fig = px.pie(results, values='Count', names='Answers', title = 'Less Likely to Report Mental Health Issues?')
        st.plotly_chart(fig)
        with st.expander("See Data Table"):
            st.write(results)        
    with ncol2:
        davidquery4 = '''
			SELECT a.AnswerText, COUNT(a.AnswerText)
			FROM Answer as a
			LEFT Join Question as q
			on a.QuestionID = q.questionid
			WHERE a.QuestionID = 56
			GROUP BY AnswerText;	
			'''
        cursor.execute(davidquery4)
        results = cursor.fetchall()
        results = pd.DataFrame(results)[1:6]
        results.columns = ["Answers", "Count"]
        st.subheader("Have you observed or experienced an unsupportive or badly handled response to a mental health issue in your current or previous workplace?")
        fig2 = px.pie(results, values='Count', names='Answers', title = 'Observed Negative Responses?')
        st.plotly_chart(fig2)
        with st.expander("See Data Table"):
            st.write(results)
    with ncol3:
        davidquery5 = '''
			SELECT a.AnswerText, COUNT(a.AnswerText)
			FROM Answer as a
			LEFT Join Question as q
			on a.QuestionID = q.questionid
			WHERE a.QuestionID = 83
			GROUP BY AnswerText;
			'''
        cursor.execute(davidquery5)
        results = cursor.fetchall()
        results = pd.DataFrame(results)[1:6]
        results.columns = ["Answers", "Count"]
        st.subheader("Have you observed or experienced supportive or well handled response to a mental health issue in your current or previous workplace?")
	
        fig3 = px.pie(results, values='Count', names='Answers', title = 'Observed Positive Responses?')
        st.plotly_chart(fig3)
        with st.expander("See Data Table"):
            st.write(results)
with tab3:
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

with tab4:
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
with tab4:
    st.subheader("How do the percentages of tech employees seeking treatment for mental health conditions differ by gender?")
    st.text("From this chart, there are distinct differences among the gender demographics. Female tech workers reported the highest rate of seeking treatment at 72.9%, followed by those identifying as other at 62.4%, and male tech workers at 51.1%. Among the three genders surveyed—male, female, and other—the percentage of individuals seeking mental health support is notably high. This data backs the commonly told claim that men are less likely to seek treatment for mental health concerns.")
    selected_gender = st.multiselect("Select Gender to Show", options=df_gender_combined['Gender'].unique(), default=df_gender_combined['Gender'].unique())
    filtered_gender = df_gender_combined[df_gender_combined['Gender'].isin(selected_gender)]
    basic_bar_5 = px.bar(filtered_gender, x='Gender', y='Percentage Who Have Sought Mental Health Treatment')
    st.plotly_chart(basic_bar_5)
    with st.expander("See Data Table"):
        st.write(df_gender_combined)
with tab4:
     st.subheader("How does the percentage of tech workers diagnosed with a mental health condition differ between employees and the self-employed?")
     st.text("Observing this chart, there is a negligible difference in the percentages of self-employed and employed tech workers diagnosed with a mental health disorder. Employed individuals show a slightly higher rate at 65.6% compared to 62.5% for the self-employed. Both groups exhibit strikingly high rates of mental health diagnoses.")
     basic_bar_6 = px.bar(df_employment_combined, x='EmploymentStatus', y='Percentage Who Have Been Diagnosed')
     st.plotly_chart(basic_bar_6)
     with st.expander("See Data Table"):
        st.write(df_employment_combined)
with tab5:
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
	with st.expander("See Data Table"):
		st.write(age_df)
	query30 = '''
		SELECT 
			COUNT(a.AnswerText) AS Count_Yes
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
			COUNT(a.AnswerText) AS Count_Yes
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
			COUNT(a.AnswerText) AS Count_Yes
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
	yes_30 = amount['Count_Yes'].iloc[0]
	total_29 = age_df.loc[age_df['AnswerText'] == '29', 'Count'].values[0]
	yes_29 = amount2['Count_Yes'].iloc[0]
	total_32 = age_df.loc[age_df['AnswerText'] == '32', 'Count'].values[0]
	yes_32 = amount3['Count_Yes'].iloc[0]
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
	with st.expander("Data Table of those who said yes from 30, 29, 32 respectively"):
		st.write(amount)  # Shows the "Yes" count for age 30
		st.write(amount2) # Shows the "Yes" count for age 29
		st.write(amount3) # Shows the "Yes" count for age 32