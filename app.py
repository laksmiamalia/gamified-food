import streamlit as st
import pandas as pd
import plotly.express as px
from cluster_descriptions import cluster_descriptions  # Import the dictionary

# Load your data
df = pd.read_csv('clustered_games.csv')

# Calculate the proportion of each cluster
cluster_counts = df['Cluster'].value_counts().reset_index()
cluster_counts.columns = ['Cluster', 'Count']

# Streamlit app layout
st.title('Game Clustering App')

# Pie chart showing the proportion of each cluster
pie_chart = px.pie(cluster_counts, names='Cluster', values='Count', title='Proportion of Each Cluster')
st.plotly_chart(pie_chart)

# Dropdown to select cluster
selected_cluster = st.selectbox(
    'Select Cluster',
    options=df['Cluster'].unique(),
    format_func=lambda x: f'Cluster {x}'
)

# Bar chart based on the selected cluster
filtered_df = df[df['Cluster'] == selected_cluster]
bar_chart = px.bar(filtered_df, x='Genre', y='Global_Sales',
                   title=f'Global Sales for Cluster {selected_cluster}',
                   labels={'Global_Sales': 'Global Sales', 'Genre': 'Genre'})
st.plotly_chart(bar_chart)

# Display cluster description
description = cluster_descriptions.get(selected_cluster, "Description not available.")
st.subheader('Cluster Description')
st.write(description)

# Lookup section
st.subheader('Lookup Game Clusters')
game_name = st.text_input('Enter game name')
if st.button('Search'):
    result_df = df[df['Name'].str.contains(game_name, case=False, na=False)]
    if not result_df.empty:
        st.write(result_df[['Name', 'Cluster']])
    else:
        st.write('No matching game found.')

# Display the head of the table
st.subheader('Sample of Clustered Games')
st.write(df.head(5))

# Link to download the full dataset
st.markdown("[Download Full Dataset](./clustered_games.csv)")
