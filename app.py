
#------------------------------------------------------
import pandas as pd
import plotly.express as px
import streamlit as st

# Set the page configuration for the Streamlit app
st.set_page_config(page_title="Referee Stats", page_icon=":bar_chart:", layout="wide")

# Read the data from the Excel file
df = pd.read_excel('basic_data.xlsx')

#-------------- SIDEBAR ----------------------------
st.sidebar.header("Please Filter Here: ")
# ref = st.sidebar.multiselect(
# "Select the Ref:",
# options=df["ref"].unique(),
# default=df["ref"].unique()
# )
win_by = st.sidebar.multiselect(
"Select the Outcome:",
options=df["win_by"].unique(),
default=df["win_by"].unique()
)
# Get the top 10 most frequent values in the 'ref' column
top_10_refs = df['ref'].value_counts().head(10).index.tolist()

# Set the default value for the 'ref' filter in the sidebar to the top 10 most frequent values
ref = st.sidebar.multiselect(
"Select the Ref:",
options=df["ref"].unique(),
default=top_10_refs
)

# Filter the data based on the selected values in the sidebar
df_selection = df.query(
  "ref == @ref & win_by == @win_by"  
)

# ---- MAINPAGE ----
st.title(":bar_chart: Fight Outcomes by Finish Type")
st.markdown("##")

# Initialize an empty list to store the rows of the results DataFrame
results_rows = []
# Loop through the selected referees
for ref in ref:
    # Filter the data to only include rows where the 'ref' column matches the current referee
    filtered_df = df[df['ref'] == ref]

    # Group the data by the 'win_by' column and count the occurrences of each value
    win_by_counts = filtered_df.groupby('win_by')['win_by'].count()
    total_count = len(filtered_df)

    # Loop through the win_by values and add a row for each one to the results list
    for win_by_value in win_by:
        if win_by_value in win_by_counts.index:
            count = win_by_counts[win_by_value]
        else:
            count = 0
        # Calculate the percentage for the current win_by value
        percentage = count / total_count * 100
        results_rows.append({'ref': ref, 'win_by': win_by_value, 'count': count, 'percentage': percentage})

# Create a new DataFrame with the results rows
results_df = pd.DataFrame(results_rows)





fig = px.bar(results_df, x='ref', y='percentage', color='win_by', text='percentage',
title='Percentage of fights with each outcome for top 10 referees',height=600, width=800)
fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
fig.update_traces(textangle=-45, textposition='outside')
st.plotly_chart(fig)
st.dataframe(results_df)