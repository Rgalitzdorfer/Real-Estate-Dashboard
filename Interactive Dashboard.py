#Import Libraries
import pandas as pd #DataFrame Manipulation 
import dash #Dash
from dash import dcc, html #Dash Components
from dash.dependencies import Input, Output #Callback
import plotly.graph_objects as go #Import Plotly Graph Objects
import argparse #Argparse 

#Load the Dataset
file_path = '/Users/ryangalitzdorfer/Downloads/MCAA/All_Data_2018.csv' #Define File Path
data = pd.read_csv(file_path, low_memory=False) #Load CSV File into DataFrame

#Additional Data Cleaning
data['Current Price'] = pd.to_numeric(data['Current Price'].replace('[\\$,]', '', regex=True)) #Clean & Convert 
data['Original List Price'] = pd.to_numeric(data['Original List Price'].replace('[\\$,]', '', regex=True)) #Clean & Convert 
data['DOM'] = pd.to_numeric(data['DOM'], errors='coerce') #Convert to Numeric
data['Closed Date'] = pd.to_datetime(data['Closed Date']) #Convert to Datetime
data['List Date'] = pd.to_datetime(data['List Date']) #Convert to Datetime

#Create a Dash App
app = dash.Dash(__name__) 
#Layout of Dashboard
app.layout = html.Div([ #Define Layout
    html.H1("Real Estate Data Dashboard"), #Title of Dashboard
    #Select Counties
    dcc.Dropdown( 
        id='county-dropdown',
        options=[{'label': county, 'value': county} for county in data['County'].unique()],
        value=[],
        multi=True,
        placeholder="Select Counties"
    ),
    #Select Towns
    dcc.Dropdown(  
        id='town-dropdown',
        options=[{'label': town, 'value': town} for town in data['Area'].unique()],
        value=[],
        multi=True,
        placeholder="Select Towns"
    ),
    #Select School District
    dcc.Dropdown(  
        id='school-dropdown',
        options=[{'label': school, 'value': school} for school in data['School District'].unique()],
        value=[],
        multi=True,
        placeholder="Select School Districts"
    ),
    #Select TimeFrame
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
    #Select Date for Above Specifications
    dcc.DatePickerRange(  
        id='date-picker-range',
        start_date=data['Closed Date'].min(),
        end_date=data['Closed Date'].max(),
        display_format='YYYY-MM-DD'
    ),
    #Graphs for Each TimeFrame
    dcc.Graph(id='closed-sales-graph'), #Closed Sales
    dcc.Graph(id='median-price-graph'), #Median Price
    dcc.Graph(id='average-price-graph'), #Average Price
    dcc.Graph(id='sp-lp-percentage-graph'), #SP/LP Percentage
    dcc.Graph(id='dom-graph') #Days on Market
])

#Filter Data Based on Dropdown Selections
@app.callback(  #Define Callback
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
def update_graphs(selected_counties, selected_towns, selected_schools, selected_timeframe, start_date, end_date): #Callback Function Definition
    filtered_df = data.copy()  
    #Error Detection
    if selected_counties: #Selected Counties
        filtered_df = filtered_df[filtered_df['County'].isin(selected_counties)]
    if selected_towns: #Selected Towns
        filtered_df = filtered_df[filtered_df['Area'].isin(selected_towns)]
    if selected_schools: #Selected Schools
        filtered_df = filtered_df[filtered_df['School District'].isin(selected_schools)]
    #Error Detection for TimeFrame
    if selected_timeframe != 'Custom': 
        end_date = filtered_df['Closed Date'].max() #Set End Date to Latest Date
        if selected_timeframe == '1M':  
            start_date = end_date - pd.DateOffset(months=1)
        elif selected_timeframe == '3M':  
            start_date = end_date - pd.DateOffset(months=3)
        elif selected_timeframe == '6M':  
            start_date = end_date - pd.DateOffset(months=6)
        elif selected_timeframe == '1Y': 
            start_date = end_date - pd.DateOffset(years=1)
    filtered_df = filtered_df[(filtered_df['Closed Date'] >= start_date) & (filtered_df['Closed Date'] <= end_date)] #Filter Data by Date Range

    #Print Statements for Debugging
    print("Filtered DataFrame:", filtered_df) 
    print("Selected Counties:", selected_counties) 
    print("Selected Towns:", selected_towns)  
    print("Selected Schools:", selected_schools)  
    print("Selected Timeframe:", selected_timeframe) 
    print("Start Date:", start_date)  
    print("End Date:", end_date)  

    #Data Manipulation
    filtered_df = filtered_df.sort_values('Closed Date') #Sort by 'Closed Date'
    num_intervals = 5 
    interval_size = len(filtered_df) // num_intervals #Get 5 Evenly Spaced Points (Each 20% of Data)
    agg_df_list = [] #Initialize 
    for i in range(num_intervals): #Loop Through Intervals
        start_index = i * interval_size #Start Index
        end_index = (i + 1) * interval_size if i < num_intervals - 1 else len(filtered_df) #End Index
        interval_df = filtered_df.iloc[start_index:end_index] #Slice
        #Aggregate Data for Interval
        agg_data = { 
            'Closed Date': interval_df['Closed Date'].iloc[-1],
            'Closed Sales': interval_df['Closed Date'].count(),
            'Median Price': interval_df['Current Price'].median(),
            'Average Price': interval_df['Current Price'].mean(),
            'SP/LP Percentage': (interval_df['Current Price'] / interval_df['Original List Price'] * 100).mean(),
            'Days on Market': interval_df['DOM'].mean()
        }
        agg_df_list.append(pd.DataFrame([agg_data])) #Add to List

    agg_df = pd.concat(agg_df_list, ignore_index=True) #Combine DataFrames
    print("Aggregated DataFrame:", agg_df) #Print for Debugging

    #Create Graphs & Layouts for Each Metric
    closed_sales_fig = go.Figure(go.Scatter(x=agg_df['Closed Date'], y=agg_df['Closed Sales'], mode='lines+markers')) #Closed Sales Graph
    closed_sales_fig.update_layout(title='Closed Sales') #Graph Layout
    median_price_fig = go.Figure(go.Scatter(x=agg_df['Closed Date'], y=agg_df['Median Price'], mode='lines+markers')) #Median Price Graph
    median_price_fig.update_layout(title='Median Price') #Graph layout
    average_price_fig = go.Figure(go.Scatter(x=agg_df['Closed Date'], y=agg_df['Average Price'], mode='lines+markers')) #Average Price Graph
    average_price_fig.update_layout(title='Average Price') #Graph Layout
    sp_lp_percentage_fig = go.Figure(go.Scatter(x=agg_df['Closed Date'], y=agg_df['SP/LP Percentage'], mode='lines+markers')) #SP/LP Percentage Graph
    sp_lp_percentage_fig.update_layout(title='SP/LP Percentage') #Graph Layout
    dom_fig = go.Figure(go.Scatter(x=agg_df['Closed Date'], y=agg_df['Days on Market'], mode='lines+markers')) #Days on Market Graph
    dom_fig.update_layout(title='Days on Market') #Graph Layout
    return closed_sales_fig, median_price_fig, average_price_fig, sp_lp_percentage_fig, dom_fig #Return Graphs

#Main Function
if __name__ == '__main__':  
    parser = argparse.ArgumentParser(description='Run the Dash app on a specified port.')  
    parser.add_argument('--port', type=int, default=8064, help='Port to run the Dash app on') #Add Port Argument, Change # When Reopening
    args = parser.parse_args() #Parse Command-Line Arguments
    app.run_server(debug=True, port=args.port) #Run Dash App 
