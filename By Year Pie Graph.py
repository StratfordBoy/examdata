import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# Load the CSV file without specifying a delimiter
df = pd.read_csv('new_Gary paper analysis question bank.csv')

# Create a Dash app
app = dash.Dash(__name__)

# Create a dropdown menu for year selection
year_options = [{'label': str(year), 'value': year} for year in range(2018, 2024)]
year_dropdown = dcc.Dropdown(id='year-dropdown', options=year_options, value=2018)

# Create a graph component to display the pie chart
graph_component = dcc.Graph(id='year-pie-chart')

# Define the app layout
app.layout = html.Div([
    html.H1('Percentage of P1 Chapters by Year'),
    year_dropdown,
    graph_component
])

# Define the callback function to update the graph
@app.callback(
    Output('year-pie-chart', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_graph(year):
    # Filter the DataFrame for the selected year
    year_df = df[df['Year-Month-Question'].str.startswith(str(year))]

    # Create a pie chart for the percentage of chapters
    chapter_counts = year_df['Textbook'].value_counts()
    chapter_percentages = chapter_counts / chapter_counts.sum() * 100
    fig_chapter = go.Figure(data=[go.Pie(labels=chapter_percentages.index, values=chapter_percentages.values, hole=0.3)])
    fig_chapter.update_layout(title=f'Percentage of Chapters in {year}')

    return fig_chapter

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)