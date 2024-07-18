import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import argparse

# Load the dataset
file_path = '/Users/ryangalitzdorfer/Downloads/MCAA/All_Data_2018.csv' 
data = pd.read_csv(file_path, low_memory=False)

# Convert price columns to numeric, removing any non-numeric characters
data['Current Price'] = pd.to_numeric(data['Current Price'].replace('[\$,]', '', regex=True))
data['Original List Price'] = pd.to_numeric(data['Original List Price'].replace('[\$,]', '', regex=True))

# Convert DOM column to numeric, handling errors by coercing to NaN
data['DOM'] = pd.to_numeric(data['DOM'], errors='coerce')

# Convert date columns to datetime
data['Closed Date'] = pd.to_datetime(data['Closed Date'])
data['List Date'] = pd.to_datetime(data['List Date'])

# Create a Dash application
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Real Estate Data Dashboard"),
    
    dcc.Dropdown(
        id='county-dropdown',
        options=[{'label': county, 'value': county} for county in data['County'].unique()],
        value=[],
        multi=True,
        placeholder="Select Counties"
    ),
    
    dcc.Dropdown(
        id='town-dropdown',
        options=[{'label': town, 'value': town} for town in data['Area'].unique()],
        value=[],
        multi=True,
        placeholder="Select Towns"
    ),
    
    dcc.Dropdown(
        id='school-dropdown',
        options=[{'label': school, 'value': school} for school in data['School District'].unique()],
        value=[],
        multi=True,
        placeholder="Select School Districts"
    ),
    
    dcc.Dropdown(
        id='timeframe-dropdown',
        options=[
            {'label': '1 Month', 'value': '1M'},
            {'label': '3 Months', 'value': '3M'},
            {'label': '6 Months', 'value': '6M'},
            {'label': '1 Year', 'value': '1Y'},
            {'label': 'Custom', 'value': 'Custom'}
        ],
        value='1M',
        placeholder="Select Timeframe"
    ),
    
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=data['Closed Date'].min(),
        end_date=data['Closed Date'].max(),
        display_format='YYYY-MM-DD'
    ),
    
    dcc.Graph(id='closed-sales-graph'),
    dcc.Graph(id='median-price-graph'),
    dcc.Graph(id='average-price-graph'),
    dcc.Graph(id='sp-lp-percentage-graph'),
    dcc.Graph(id='dom-graph')
])

# Callback to filter data based on dropdown selections
@app.callback(
    [Output('closed-sales-graph', 'figure'),
     Output('median-price-graph', 'figure'),
     Output('average-price-graph', 'figure'),
     Output('sp-lp-percentage-graph', 'figure'),
     Output('dom-graph', 'figure')],
    [Input('county-dropdown', 'value'),
     Input('town-dropdown', 'value'),
     Input('school-dropdown', 'value'),
     Input('timeframe-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_graphs(selected_counties, selected_towns, selected_schools, selected_timeframe, start_date, end_date):
    filtered_df = data.copy()
    
    if selected_counties:
        filtered_df = filtered_df[filtered_df['County'].isin(selected_counties)]
    if selected_towns:
        filtered_df = filtered_df[filtered_df['Area'].isin(selected_towns)]
    if selected_schools:
        filtered_df = filtered_df[filtered_df['School District'].isin(selected_schools)]
    
    # Filter data based on timeframe
    if selected_timeframe != 'Custom':
        end_date = filtered_df['Closed Date'].max()
        if selected_timeframe == '1M':
            start_date = end_date - pd.DateOffset(months=1)
        elif selected_timeframe == '3M':
            start_date = end_date - pd.DateOffset(months=3)
        elif selected_timeframe == '6M':
            start_date = end_date - pd.DateOffset(months=6)
        elif selected_timeframe == '1Y':
            start_date = end_date - pd.DateOffset(years=1)
    
    filtered_df = filtered_df[(filtered_df['Closed Date'] >= start_date) & (filtered_df['Closed Date'] <= end_date)]

    # Print statements for debugging
    print("Filtered DataFrame:", filtered_df)
    print("Selected Counties:", selected_counties)
    print("Selected Towns:", selected_towns)
    print("Selected Schools:", selected_schools)
    print("Selected Timeframe:", selected_timeframe)
    print("Start Date:", start_date)
    print("End Date:", end_date)

    # Calculations for outputs
    closed_sales = filtered_df['Closed Date'].count()
    median_price = filtered_df['Current Price'].median()
    average_price = filtered_df['Current Price'].mean()
    sp_lp_percentage = ((filtered_df['Current Price'] / filtered_df['Original List Price']) * 100).mean()
    dom = filtered_df['DOM'].mean()

    # Print calculations for debugging
    print("Closed Sales:", closed_sales)
    print("Median Price:", median_price)
    print("Average Price:", average_price)
    print("SP/LP Percentage:", sp_lp_percentage)
    print("Days on Market:", dom)

    closed_sales_fig = px.bar(x=['Closed Sales'], y=[closed_sales], title='Closed Sales')
    median_price_fig = px.bar(x=['Median Price'], y=[median_price], title='Median Price')
    average_price_fig = px.bar(x=['Average Price'], y=[average_price], title='Average Price')
    sp_lp_percentage_fig = px.bar(x=['SP/LP %'], y=[sp_lp_percentage], title='SP/LP Percentage')
    dom_fig = px.bar(x=['Days on Market'], y=[dom], title='Days on Market')

    return closed_sales_fig, median_price_fig, average_price_fig, sp_lp_percentage_fig, dom_fig

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the Dash app on a specified port.')
    parser.add_argument('--port', type=int, default=8052, help='Port to run the Dash app on')
    args = parser.parse_args()
    app.run_server(debug=True, port=args.port)