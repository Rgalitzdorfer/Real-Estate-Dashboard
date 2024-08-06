# Real Estate Dashboard Overview
In collaboration with Monroe County Appraisal Associates (MCAA), this project builds an application that allows users to quickly and accurately evaluate several metrics for unique counties, towns, school districts, and timeframes within the Greater Rochester Area. All real estate data since 2018 was originally downloaded and concatenated from the Multiple Listing Service (MLS), a database that tracks every sale within New York. Useful metrics were cleaned and standardized to ensure accurate results for each selection. Each output provides results from the drop-down menu with an accompanying graph, utilizing the selected timeframe to perform a time series analysis on any given combination of county, town, and school district. This analytic tool built with Plotly & Dash expedites every appraisal report's 'Neighborhood Evaluation' section by providing a condensed bundle of information to evaluate market conditions. It may also be used to identify trending neighborhoods within the local real estate market, giving homebuyers the necessary information to make informed decisions.

### 4 Drop-Down Options:
1. County
2. Town
3. School District
4. Timeframe (Used for Time Series Analysis)
### Outputs from Drop-Down Selections:
1. Closed Sales (Tracks Number of Sales)
2. Median Price
3. Average Price
4. Days on Market (Tracks Buyer demand)
5. Sales Price/List Price (Tracks Willingness to Pay Above 'Market Price')

# Code Breakdown
## Libraries Used
### Pandas (DataFrame Manipulation)
### Dash (Web Applications)
### Plotly (Interactive Visualizations)

## Data Collection & Cleaning (1)
This file is responsible for accumulating all sales from the Greater Rochester Area (Monroe, Ontario, Wayne, & Livingston County) since 2018. All results were then merged into one DataFrame to allow for easier manipulation and further analysis. Data Cleaning & Preprocessing included selecting pertinent towns and school districts, standardizing names, converting columns to required formats, and sorting by certain data. These conversions and adjustments preserved the quality of the data and ensured its usefulness when creating an interactive application.

## Interactive Dashboard (2)
This code takes the condensed and cleaned data from the previous file and creates a drop-down selection using Dash to provide users with advanced metrics for any given combination of inputs. Users could select all sales from different counties, towns, school districts, and create customized timeframes to visualize neighborhood trends over variable time periods. Different timeframe selections include 1 year, 6 months, 3 months, 1 month, and a customizable date range. Every combination of these 4 inputs provides different results including the amount of closed sales, days on markets, average price, median price, and SP/LP over the specified timeframe. This information is then analyzed to provide an accurate assessment of local real estate conditions, which is used to give houses an accurate valuation.
