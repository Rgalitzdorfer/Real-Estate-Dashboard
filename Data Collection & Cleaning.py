#Import Libraries
import pandas as pd #DataFrame
import os #Operating System
import re #Regular Expressions

#Define Folder Path 
folder_path = '/Users/ryangalitzdorfer/Downloads/MCAA'
output_file = os.path.join(folder_path, 'All_Data_2018.csv')

#List All CSV Files 
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

#Data Cleaning
columns_to_delete = ['Styles of Residence', 'St', 'HVAC Type', 'Seller Concessions Amt', 'Lot Square Footage', 'Type'] #Useless Columns
columns_to_rename = { #Rename
    'Area NYSWIS Code': 'Area',
    'County Or Parish': 'County',
    'Beds Total': 'Beds',
    'Baths Total': 'Baths',
    'Num of Garage Spaces': 'Garage',
    'School District Name': 'School District'
}

#Lists of Towns in Monroe County to Keep
monroe_county_towns = [
    "Brighton", "Chili", "Clarkson", "East Rochester", "Gates", "Greece", "Hamlin",
    "Henrietta", "Irondequoit", "Mendon", "Ogden", "Parma", "Penfield", "Perinton",
    "Pittsford", "Riga", "Rochester", "Rush", "Sweden", "Wheatland", "Webster"
]

#Lists of Schools in Monroe County to Keep
monroe_county_schools = [
    "Brighton", "Brockport", "Byron-Bergen", "Caledonia-Mumford", "Churchville-Chili",
    "East Irondequoit", "East Rochester", "Fairport", "Gates-Chili", "Greece", "Hilton",
    "Holley", "Honeoye Falls-Lima", "Kendall", "Penfield", "Pittsford", "Rush-Henrietta",
    "Spencerport", "Victor", "Wayne", "Webster", "West-Irondequoit", "Wheatland-Chili"
]

#Lists of Towns in Wayne County to Keep
wayne_county_towns = [
    "Arcadia", "Butler", "Galen", "Huron", "Lyons", "Macedon", "Marion", "Ontario",
    "Palmyra", "Rose", "Savannah", "Sodus", "Walworth", "Williamson", "Wolcott"
]

#Lists of Schools in Wayne County to Keep
wayne_county_schools = [
    "Cato-Meridian", "Clyde-Savannah", "Gananda", "Lyons", "Marion", "Newark", "North Rose-Wolcott",
    "Palmyra-Macedon", "Penfield", "Phelps-Clifton Springs", "Port Byron", "Red Creek", "Sodus",
    "Victor", "Wayne"
]

#Initialize Empty List
dataframes = []

#Iterate Through Each CSV File 
for file in csv_files:
    file_path = os.path.join(folder_path, file) #Construct the Full File Path
    df = pd.read_csv(file_path) #Read the CSV File 

    # Print Original Unique Towns & Schools 
    if 'County' in df.columns:
        monroe_df = df[df['County'].str.contains('Monroe', na=False)]
        wayne_df = df[df['County'].str.contains('Wayne', na=False)]
        #Error Detection
        if not monroe_df.empty:
            print(f"\nOriginal unique Monroe county areas in file: {file}")
            print(monroe_df['Area'].unique())
            print("\nOriginal unique Monroe county school districts in file:")
            print(monroe_df['School District'].unique())
        #Error Detection
        if not wayne_df.empty:
            print(f"\nOriginal unique Wayne county areas in file: {file}")
            print(wayne_df['Area'].unique())
            print("\nOriginal unique Wayne county school districts in file:")
            print(wayne_df['School District'].unique())

    #Apply Earlier Data Cleaning Functions
    df.drop(columns=[col for col in columns_to_delete if col in df.columns], inplace=True)
    df.rename(columns={k: v for k, v in columns_to_rename.items() if k in df.columns}, inplace=True)
    #Standardize
    if 'Area' in df.columns:
        df['Area'] = df['Area'].apply(lambda x: re.sub(r'-\d+', '', str(x)).strip())
    #Filter the Dataframe for Useful Towns & Schools
    df = df[df['Area'].isin(monroe_county_towns + wayne_county_towns)]
    df = df[df['School District'].isin(monroe_county_schools + wayne_county_schools)]
    dataframes.append(df) #Add to List

#Combine DataFrames
combined_df = pd.concat(dataframes, ignore_index=True)
#Separate Counties
monroe_combined_df = combined_df[combined_df['County'].str.contains('Monroe', na=False)]
wayne_combined_df = combined_df[combined_df['County'].str.contains('Wayne', na=False)]

#Print Statements for Error Detection
print("\nUnique Monroe County Towns:")
print(monroe_combined_df['Area'].unique())
print("\nUnique Monroe County Schools:")
print(monroe_combined_df['School District'].unique())
print("\nUnique Wayne County Towns:")
print(wayne_combined_df['Area'].unique())
print("\nUnique Wayne County Schools:")
print(wayne_combined_df['School District'].unique())

#Compare Unique Towns & Schools to Required List
missing_monroe_towns = set(monroe_county_towns) - set(monroe_combined_df['Area'].unique())
missing_wayne_towns = set(wayne_county_towns) - set(wayne_combined_df['Area'].unique())
missing_monroe_schools = set(monroe_county_schools) - set(monroe_combined_df['School District'].unique())
missing_wayne_schools = set(wayne_county_schools) - set(wayne_combined_df['School District'].unique())
#Print Statements for Error Detection
print("\nMissing Monroe County Towns:")
print(missing_monroe_towns)
print("\nMissing Wayne County Towns:")
print(missing_wayne_towns)
print("\nMissing Monroe County Schools:")
print(missing_monroe_schools)
print("\nMissing Wayne County Schools:")
print(missing_wayne_schools)

#Save to New CSV file
combined_df.to_csv(output_file, index=False)

#Convert Columns to Numeric & Datetime Formats
combined_df['Current Price'] = pd.to_numeric(combined_df['Current Price'].replace('[\$,]', '', regex=True)) #Replace $
combined_df['Original List Price'] = pd.to_numeric(combined_df['Original List Price'].replace('[\$,]', '', regex=True)) #Replace $
combined_df['DOM'] = pd.to_numeric(combined_df['DOM'], errors='coerce')
combined_df['Closed Date'] = pd.to_datetime(combined_df['Closed Date'])
combined_df['List Date'] = pd.to_datetime(combined_df['List Date'])
print(f"All Files Have Been Combined, Cleaned, Renamed, & Saved to {output_file}") #Print Statement
