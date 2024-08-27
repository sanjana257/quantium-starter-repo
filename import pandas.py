import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Step 1: Load the data
df = pd.read_csv('data/formatted_output.csv')

# Ensure the 'date' column is in datetime format
df['date'] = pd.to_datetime(df['date'])

# Step 2: Create a Dash app
app = dash.Dash(__name__)

# Step 3: Create the layout with a header, radio buttons, and line chart
app.layout = html.Div(children=[
    html.H1(
        children='Pink Morsel Sales Visualizer',
        style={
            'textAlign': 'center',
            'color': '#2c3e50',
            'font-family': 'Arial, sans-serif'
        }
    ),
    
    # Radio buttons for region selection
    dcc.RadioItems(
        id='region-radio',
        options=[
            {'label': 'All', 'value': 'all'},
            {'label': 'North', 'value': 'north'},
            {'label': 'East', 'value': 'east'},
            {'label': 'South', 'value': 'south'},
            {'label': 'West', 'value': 'west'}
        ],
        value='all',  # Default selection
        labelStyle={'display': 'inline-block', 'margin-right': '15px'},
        style={
            'textAlign': 'center',
            'padding': '10px',
            'font-family': 'Arial, sans-serif',
            'color': '#34495e'
        }
    ),
    
    # Line chart to visualize sales data
    dcc.Graph(id='sales-line-chart'),

    html.Footer(
        children="Data visualization for Soul Foods",
        style={
            'textAlign': 'center',
            'margin-top': '50px',
            'font-family': 'Arial, sans-serif',
            'color': '#7f8c8d'
        }
    )
])

# Step 4: Create a callback to update the chart based on selected region
@app.callback(
    Output('sales-line-chart', 'figure'),
    [Input('region-radio', 'value')]
)
def update_line_chart(selected_region):
    if selected_region == 'all':
        filtered_df = df
    else:
        filtered_df = df[df['region'] == selected_region]
    
    fig = px.line(
        filtered_df,
        x='date',
        y='sales',
        title=f'Sales Over Time ({selected_region.capitalize()})'
    )
    
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Sales',
        template='plotly_dark',
        plot_bgcolor='#ecf0f1',
        paper_bgcolor='#ecf0f1'
    )
    
    return fig

# Step 5: Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
