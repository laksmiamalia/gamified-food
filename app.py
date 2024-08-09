from flask import Flask, send_file
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px

# Initialize Flask
server = Flask(__name__)

# Initialize Dash
app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/')

# Load your data
df = pd.read_csv('clustered_games.csv')

# Calculate the proportion of each cluster
cluster_counts = df['Cluster'].value_counts().reset_index()
cluster_counts.columns = ['Cluster', 'Count']

# Define layout
app.layout = html.Div([
    # Dropdown to select cluster
    dcc.Dropdown(
        id='cluster-dropdown',
        options=[{'label': f'Cluster {i}', 'value': i} for i in df['Cluster'].unique()],
        value=df['Cluster'].unique()[0]
    ),

    # Pie chart showing the proportion of each cluster
    dcc.Graph(id='pie-chart'),

    # Graph based on the selected cluster
    dcc.Graph(id='cluster-graph'),

    # Lookup section
    html.H2("Lookup Game Clusters"),
    dcc.Input(id='game-search', type='text', placeholder='Enter game name'),
    html.Button('Search', id='search-button', n_clicks=0),
    html.Div(id='search-result'),

    # Display the head of the table
    html.H2("Sample of Clustered Games"),
    dash_table.DataTable(
        id='game-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.head(5).to_dict('records'),
        style_table={'overflowX': 'auto'},
        style_header={
            'backgroundColor': 'rgb(30, 30, 30)',
            'color': 'white'
        },
        style_cell={
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white'
        }
    ),

    # Link to download the full dataset
    html.A("Download Full Dataset", href='/download_csv')
])

# Callback to update the pie chart and bar chart based on dropdown selection
@app.callback(
    Output('pie-chart', 'figure'),
    Output('cluster-graph', 'figure'),
    [Input('cluster-dropdown', 'value')]
)
def update_graphs(selected_cluster):
    # Update pie chart
    pie_chart = px.pie(cluster_counts, names='Cluster', values='Count', title='Proportion of Each Cluster')

    # Update bar chart
    filtered_df = df[df['Cluster'] == selected_cluster]
    bar_chart = px.bar(filtered_df, x='Genre', y='Global_Sales',
                       title=f'Global Sales for Cluster {selected_cluster}',
                       labels={'Global_Sales': 'Global Sales', 'Genre': 'Genre'})

    return pie_chart, bar_chart

# Callback to search for a game
@app.callback(
    Output('search-result', 'children'),
    [Input('search-button', 'n_clicks')],
    [State('game-search', 'value')]
)
def search_game(n_clicks, game_name):
    if n_clicks > 0 and game_name:
        result_df = df[df['Name'].str.contains(game_name, case=False, na=False)]
        if not result_df.empty:
            return html.Ul([html.Li(f"{row['Name']} - Cluster {row['Cluster']}") for idx, row in result_df.iterrows()])
        else:
            return html.P("No matching game found.")
    return ""

# Route to download the full CSV file
@server.route('/download_csv')
def download_csv():
    return send_file('clustered_games.csv',
                     mimetype='text/csv',
                     attachment_filename='clustered_games.csv',
                     as_attachment=True)

if __name__ == '__main__':
    server.run(debug=True)
