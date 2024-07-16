#!/usr/bin/env python
# coding: utf-8

# # PyCity Schools Analysis
# 
# - Your analysis here
#   
# ---

# In[1]:


# Dependencies and Setup
import pandas as pd
from pathlib import Path

# File to Load (Remember to Change These)
school_data_to_load = Path("Resources/schools_complete.csv")
student_data_to_load = Path("Resources/students_complete.csv")

# Read School and Student Data File and store into Pandas DataFrames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset.
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])
school_data_complete.head()


# ## District Summary

# In[8]:


# Calculate the total number of unique schools
school_count = school_data_complete["school_name"].nunique()
school_count


# In[9]:


# Calculate the total number of students
student_count = school_data_complete["student_name"].count()
student_count


# In[10]:


# Calculate the total budget
total_budget = school_data["budget"].sum()
total_budget


# In[11]:


# Calculate the average (mean) math score
average_math_score = school_data_complete["math_score"].mean()
average_math_score


# In[12]:


# Calculate the average (mean) reading score
average_reading_score = school_data_complete["reading_score"].mean()
average_reading_score


# In[13]:


# Use the following to calculate the percentage of students who passed math (math scores greather than or equal to 70)
passing_math_count = school_data_complete[(school_data_complete["math_score"] >= 70)].count()["student_name"]
passing_math_percentage = passing_math_count / float(student_count) * 100
passing_math_percentage


# In[14]:


# Calculate the percentage of students who passed reading (hint: look at how the math percentage was calculated)
#school_data_complete - first one is defining data frame Im using , then [school_data_complete["reading_score"] defines what in the datafram I am trying to find.]
passing_reading_count = school_data_complete[(school_data_complete["reading_score"] >= 70)].count()["student_name"]
passing_reading_percentage = passing_reading_count / float(student_count) * 100
passing_reading_percentage


# In[15]:


# Use the following to calculate the percentage of students that passed math and reading
passing_math_reading_count = school_data_complete[
    (school_data_complete["math_score"] >= 70) & (school_data_complete["reading_score"] >= 70)
].count()["student_name"]
overall_passing_rate = passing_math_reading_count /  float(student_count) * 100
overall_passing_rate


# In[16]:


# Create a high-level snapshot of the district's key metrics in a DataFrame
district_summary = pd.DataFrame(
    {"Total Schools": [school_count],
     "Total Students": [student_count],
     "Total Budget": [total_budget],
     "Average Math Score": [average_math_score],
     "Average Reading Score": [average_reading_score],
     "% Passing Math": [passing_math_percentage],
     "% Passing Reading": [passing_reading_percentage],
     "% Overall Passing": [overall_passing_rate]
     
    })

# Formatting
district_summary["Total Students"] = district_summary["Total Students"].map("{:,}".format)
district_summary["Total Budget"] = district_summary["Total Budget"].map("${:,.2f}".format)

# Display the DataFrame
district_summary


# ## School Summary

# In[81]:


budget_per_student = total_budget / student_count
budget_per_student


# In[17]:


# Use the code provided to select the type per school from school_data
school_types = school_data.set_index(["school_name"])["type"]
school_types


# In[18]:


# Calculate the total student count per school from school_data
per_school_counts = school_data.set_index(["school_name"])["size"]
per_school_counts


# In[19]:


# Calculate the total school budget and per capita spending per school from school_data
per_school_budget = school_data.set_index(["school_name"])["budget"]
per_school_budget
per_school_capita = (per_school_budget / per_school_counts)
per_school_capita


# In[20]:


# Calculate the average test scores per school from school_data_complete
per_school_math = school_data_complete.groupby(school_data_complete["school_name"])["math_score"].mean()
per_school_math
per_school_reading = school_data_complete.groupby(school_data_complete["school_name"])["reading_score"].mean()
per_school_reading


# In[21]:


# Calculate the number of students per school with math scores of 70 or higher from school_data_complete
students_passing_math = school_data_complete[(school_data_complete["math_score"] >= 70)]
school_passing_math = students_passing_math.groupby(students_passing_math["school_name"]).size()
school_passing_math


# In[22]:


# Calculate the number of students per school with reading scores of 70 or higher from school_data_complete
students_passing_reading = school_data_complete[(school_data_complete["reading_score"] >= 70)]
school_students_passing_reading = students_passing_reading.groupby(students_passing_reading["school_name"]).size()
school_students_passing_reading


# In[23]:


# Use the provided code to calculate the number of students per school that passed both math and reading with scores of 70 or higher
students_passing_math_and_reading = school_data_complete[
    (school_data_complete["reading_score"] >= 70) & (school_data_complete["math_score"] >= 70)
]
school_students_passing_math_and_reading = students_passing_math_and_reading.groupby(["school_name"]).size()
school_students_passing_math_and_reading


# In[24]:


# Use the provided code to calculate the passing rates
per_school_passing_math = school_passing_math / per_school_counts * 100
per_school_passing_reading = school_students_passing_reading / per_school_counts * 100
overall_passing_rate = school_students_passing_math_and_reading / per_school_counts * 100
overall_passing_rate


# In[46]:


# Create a DataFrame called `per_school_summary` with columns for the calculations above.
per_school_summary = pd.DataFrame (
    {
     "School Type": school_types,
     "School Size": per_school_counts,
     "School Budget": per_school_budget,
     "Budget per Student": per_school_capita,
     "Average Math Score": per_school_math,
     "Average Reading Score": per_school_reading,
     "% Passing Math": per_school_passing_math,
     "% Passing Reading": per_school_passing_reading,
     "Overall Passing Rate (%)": overall_passing_rate
     
        
    }
)
per_school_summary


# In[47]:


# Formatting
per_school_summary["School Budget"] = per_school_summary["School Budget"].map("${:,.2f}".format)
per_school_summary["Budget per Student"] = per_school_summary["Budget per Student"].map("${:,.2f}".format)

# Display the DataFrame
per_school_summary


# ## Highest-Performing Schools (by % Overall Passing)

# In[83]:


# Sort the schools by `% Overall Passing` in descending order and display the top 5 rows.
top_schools = per_school_summary.sort_values(
    by = "Overall Passing Rate (%)",
    ascending = False)

top_schools


# ## Bottom Performing Schools (By % Overall Passing)

# In[82]:


# Sort the schools by `% Overall Passing` in ascending order and display the top 5 rows.
bottom_schools = per_school_summary.sort_values(
    by = "Overall Passing Rate (%)",
    ascending = True)

bottom_schools


# ## Math Scores by Grade

# In[50]:


# Use the code provided to separate the data by grade
ninth_graders = school_data_complete[(school_data_complete["grade"] == "9th")]
tenth_graders = school_data_complete[(school_data_complete["grade"] == "10th")]
eleventh_graders = school_data_complete[(school_data_complete["grade"] == "11th")]
twelfth_graders = school_data_complete[(school_data_complete["grade"] == "12th")]

# Group by `school_name` and take the mean of the `math_score` column for each.
ninth_grade_math_scores = ninth_graders["math_score"].mean()
tenth_grader_math_scores = tenth_graders["math_score"].mean()
eleventh_grader_math_scores = eleventh_graders["math_score"].mean()
twelfth_grader_math_scores = twelfth_graders["math_score"].mean()

# Combine each of the scores above into single DataFrame called `math_scores_by_grade`
math_scores_by_grade = pd.DataFrame({
    "9th Grade Math Scores": [ninth_grade_math_scores],
    "10th Grade Math Scores": [tenth_grader_math_scores],
    "11th Grade Math Scores": [eleventh_grader_math_scores],
    "12th Grade Math Scores": [twelfth_grader_math_scores]
})

# Minor data wrangling
math_scores_by_grade.index.name = None

# Display the DataFrame
math_scores_by_grade


# ## Reading Score by Grade 

# In[51]:


# Use the code provided to separate the data by grade
ninth_graders = school_data_complete[(school_data_complete["grade"] == "9th")]
tenth_graders = school_data_complete[(school_data_complete["grade"] == "10th")]
eleventh_graders = school_data_complete[(school_data_complete["grade"] == "11th")]
twelfth_graders = school_data_complete[(school_data_complete["grade"] == "12th")]


# Group by `school_name` and take the mean of the the `reading_score` column for each.
ninth_grade_reading_scores = ninth_graders["reading_score"].mean()
tenth_grader_reading_scores = tenth_graders["reading_score"].mean()
eleventh_grader_reading_scores = eleventh_graders["reading_score"].mean()
twelfth_grader_reading_scores = twelfth_graders["reading_score"].mean()

# Combine each of the scores above into single DataFrame called `reading_scores_by_grade`
reading_scores_by_grade = pd.DataFrame({
    "9th Grade Reading Scores": [ninth_grade_reading_scores],
    "10th Grade Reading Scores": [tenth_grader_reading_scores],
    "11th Grade Reading Scores": [eleventh_grader_reading_scores],
    "12th Grade Reading Scores": [twelfth_grader_reading_scores]
})

# Minor data wrangling

reading_scores_by_grade.index.name = None

# Display the DataFrame
reading_scores_by_grade


# ## Scores by School Spending

# In[52]:


# Establish the bins
spending_bins = [0, 585, 630, 645, 680]
labels = ["<$585", "$585-630", "$630-645", "$645-680"]
# Create a copy of the school summary since it has the "Per Student Budget"
school_spending_df = per_school_summary.copy()
school_spending_df


# In[53]:


school_spending_df.dtypes
# Use `pd.cut` to categorize spending based on the bins.
school_spending_df["Spending Ranges (Per Student)"] = pd.cut(
    per_school_capita,
    bins=spending_bins, 
    labels=labels
)


# In[54]:


school_spending_df


# In[57]:


#  Calculate averages for the desired columns.
spending_math_scores = school_spending_df.groupby(["Spending Ranges (Per Student)"])["Average Math Score"].mean()
spending_reading_scores = school_spending_df.groupby(["Spending Ranges (Per Student)"])["Average Reading Score"].mean()
spending_passing_math = school_spending_df.groupby(["Spending Ranges (Per Student)"])["% Passing Math"].mean()
spending_passing_reading = school_spending_df.groupby(["Spending Ranges (Per Student)"])["% Passing Reading"].mean()
overall_passing_spending = school_spending_df.groupby(["Spending Ranges (Per Student)"])["Overall Passing Rate (%)"].mean()


# In[61]:


# Assemble into DataFrame
spending_summary = pd.DataFrame({
    "Average Math Score": spending_math_scores,
    "Average Reading Score": spending_reading_scores,
    "Average Passing Math": spending_passing_math,
    "Average Passing Reading": spending_passing_reading,
    "Average Overall Pass Rate" : overall_passing_spending
})


# Display results
spending_summary


# ## Scores by School Size

# In[64]:


# Establish the bins.
size_bins = [0, 1000, 2000, 5000]
labels = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]
school_size_scores_df = per_school_summary.copy()
school_size_scores_df


# In[67]:


# Categorize the spending based on the bins

# Use `pd.cut` on the "Total Students" column of the `per_school_summary` DataFrame.

school_size_scores_df["School Size"] = pd.cut( 
    per_school_counts,
    bins=size_bins, 
    labels=labels
    
)
school_size_scores_df


# In[71]:


# Calculate averages for the desired columns.
size_math_scores = school_size_scores_df.groupby(["School Size"])["Average Math Score"].mean()
size_reading_scores = school_size_scores_df.groupby(["School Size"])["Average Reading Score"].mean()
size_passing_math = school_size_scores_df.groupby(["School Size"])["% Passing Math"].mean()
size_passing_reading = school_size_scores_df.groupby(["School Size"])["% Passing Reading"].mean()
size_overall_passing = school_size_scores_df.groupby(["School Size"])["Overall Passing Rate (%)"].mean()



# In[74]:


# Create a DataFrame called `size_summary` that breaks down school performance based on school size (small, medium, or large).
# Use the scores above to create a new DataFrame called `size_summary`
size_summary = pd.DataFrame({
    "Average Math Score": size_math_scores,
    "Average Reading Score": size_reading_scores,
    "Average Math Pass Rate": size_passing_math,
    "Average Reading Pass Rate": size_passing_reading,
    "Overall Pass Rate": size_overall_passing
})

# Display results
size_summary


# ## Scores by School Type

# In[76]:


# Group the per_school_summary DataFrame by "School Type" and average the results.
average_math_score_by_type = per_school_summary.groupby(["School Type"])["Average Math Score"].mean()
average_reading_score_by_type = per_school_summary.groupby(["School Type"])["Average Reading Score"].mean()
average_percent_passing_math_by_type = per_school_summary.groupby(["School Type"])["% Passing Math"].mean()
average_percent_passing_reading_by_type = per_school_summary.groupby(["School Type"])["% Passing Reading"].mean()
average_percent_overall_passing_by_type = per_school_summary.groupby(["School Type"])["Overall Passing Rate (%)"].mean()


# In[78]:


# Assemble the new data by type into a DataFrame called `type_summary`
type_summary = pd.DataFrame({
    "Average Math Score": average_math_score_by_type,
    "Average Reading Score": average_reading_score_by_type,
    "Average Passing Math Rate": average_percent_passing_math_by_type,
    "Average Passing Reading Rate": average_percent_passing_reading_by_type,
    "Average Overall Passing Rate": average_percent_overall_passing_by_type
})

# Display results
type_summary


# In[ ]:




