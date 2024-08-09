import streamlit as st
import pandas as pd
import plotly.express as px

# Load your data
df = pd.read_csv('clustered_games.csv')

# Calculate the proportion of each cluster
cluster_counts = df['Cluster'].value_counts().reset_index()
cluster_counts.columns = ['Cluster', 'Count']

# Streamlit app layout
st.title('Game Clustering App')

# Dropdown to select cluster
selected_cluster = st.selectbox(
    'Select a Cluster',
    options=df['Cluster'].unique(),
    index=0
)

# Pie chart showing the proportion of each cluster
pie_chart = px.pie(cluster_counts, names='Cluster', values='Count', title='Proportion of Each Cluster')
st.plotly_chart(pie_chart)

# Filtered data for the selected cluster
filtered_df = df[df['Cluster'] == selected_cluster]

# Bar chart for the selected cluster
bar_chart = px.bar(filtered_df, x='Genre', y='Global_Sales',
                   title=f'Global Sales for Cluster {selected_cluster}',
                   labels={'Global_Sales': 'Global Sales', 'Genre': 'Genre'})
st.plotly_chart(bar_chart)

# Lookup section
st.header("Lookup Game Clusters")
game_name = st.text_input('Enter game name')
if st.button('Search'):
    if game_name:
        result_df = df[df['Name'].str.contains(game_name, case=False, na=False)]
        if not result_df.empty:
            st.write(result_df[['Name', 'Cluster']])
        else:
            st.write("No matching game found.")

# Display the head of the table
st.header("Sample of Clustered Games")
st.dataframe(df.head(5))

# Download link for the full dataset
st.markdown("[Download Full Dataset](clustered_games.csv)", unsafe_allow_html=True)
