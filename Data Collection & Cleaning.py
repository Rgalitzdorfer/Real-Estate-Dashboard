import pandas as pd
import os
import re

# Define the folder path and output file name
folder_path = '/Users/ryangalitzdorfer/Downloads/MCAA'
output_file = os.path.join(folder_path, 'All_Data_2018.csv')

# List all CSV files in the folder
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# Columns to be deleted
columns_to_delete = ['Styles of Residence', 'St', 'HVAC Type', 'Seller Concessions Amt', 'Lot Square Footage', 'Type']

# Columns to be renamed
columns_to_rename = {
    'Area NYSWIS Code': 'Area',
    'County Or Parish': 'County',
    'Beds Total': 'Beds',
    'Baths Total': 'Baths',
    'Num of Garage Spaces': 'Garage',
    'School District Name': 'School District'
}

# Initialize an empty list to hold dataframes
dataframes = []

# Iterate through each CSV file and read it into a dataframe
for file in csv_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_csv(file_path)
    
    # Delete the specified columns if they exist in the dataframe
    df.drop(columns=[col for col in columns_to_delete if col in df.columns], inplace=True)
    
    # Rename the specified columns if they exist in the dataframe
    df.rename(columns={k: v for k, v in columns_to_rename.items() if k in df.columns}, inplace=True)
    
    # Clean the 'Area' column by removing the hyphen and numbers
    if 'Area' in df.columns:
        df['Area'] = df['Area'].apply(lambda x: re.sub(r'-\d+', '', str(x)).strip())
    
    dataframes.append(df)

# Concatenate all dataframes into one
combined_df = pd.concat(dataframes, ignore_index=True)

# Print all unique areas
unique_areas = combined_df['Area'].unique()
print("Unique Areas:")
for area in unique_areas:
    print(area)

# Save the combined dataframe to a new CSV file
combined_df.to_csv(output_file, index=False)
combined_df['Current Price'] = pd.to_numeric(combined_df['Current Price'].replace('[\$,]', '', regex=True))
combined_df['Original List Price'] = pd.to_numeric(combined_df['Original List Price'].replace('[\$,]', '', regex=True))

# Convert DOM column to numeric, handling errors by coercing to NaN
combined_df['DOM'] = pd.to_numeric(combined_df['DOM'], errors='coerce')

# Convert date columns to datetime
combined_df['Closed Date'] = pd.to_datetime(combined_df['Closed Date'])
combined_df['List Date'] = pd.to_datetime(combined_df['List Date'])
print(f"All files have been combined, cleaned, renamed, and saved to {output_file}")
