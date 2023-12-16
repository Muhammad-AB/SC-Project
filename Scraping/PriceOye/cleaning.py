# Script: Cleaner for PriceOye products
# Author: Muhammad Abdul Basit
# Date: 16/12/2023

# Script to clean and transform data from a CSV file and save it as a JSON file
# Uses pandas and json libraries for data manipulation

# Importing required libraries
import pandas as pd
import json

# Input and output file paths
input_file = "PriceOye_Smart Watches.csv"
output_file = "Cleaned_Watches.json"

# Metadata
Category = "Watch"
Vendor = 'PriceOye'
Vendor_url = 'https://priceoye.pk/'
Last_updated = None
Similar_products = None
Currency = 'PKR'
Address = None
Delivery_time_from = None
Delivery_time_to = None
Delivery_time_period = None
Delivery_time_unparsed = None
Delivery_fee = None
Brand = None
Description = None
Used = False
Warranty_duration = None
Warranty_period = None
Warranty_type = None
Delivery_detail = None


# Read CSV file into a pandas DataFrame
df = pd.read_csv(input_file)


# Data cleaning and transformation

# replace null values in Actual Price column with NaN
df['Actual Price'] = df['Actual Price'].replace('null', pd.np.nan)
# swap values in Actual Price and Discount Price columns where Actual Price is NaN
mask = df['Actual Price'].isna()
df.loc[mask, ['Actual Price', 'Discount Price']] = df.loc[mask, ['Discount Price', 'Actual Price']].values

# Replace "RS." with an empty string, and convert to float
df['Actual Price'] = df['Actual Price'].str.replace('Rs\.|\,', '', regex=True).astype(float)
df['Discount Price'] = df['Discount Price'].str.replace('Rs\.|\,', '', regex=True).astype(float)

# convert the 'URL' column to URL data type
df['URL'] = df['URL'].astype('str')
# Convert the "Title" column to string (str) data type
df['Title'] = df['Title'].astype(str)

# Convert "Image Link" column to list
# df['Image Link'] = df['Image Link'].apply(lambda x: x.split(',') if isinstance(x, str) else [])

# Convert the "Rating" column to float data type
df['Rating'] = df['Rating'].astype(float)

# remove the 'Ratings' string from the 'Review count' column
df['Review Count'] = df['Review Count'].str.replace(' Ratings', '')
# convert the 'Review count' column to integer data type
df['Review Count'] = df['Review Count'].astype(int)

# convert the JSON strings to Python objects
df['Comments'] = df['Comments'].apply(lambda x: json.loads(x))

df.loc[df['Comments'].apply(len) == 0, 'Comments'] = None
#df.loc[df['Image Link'].apply(len) == 0, 'Image Link'] = None

# convert the 'Availability' column to str data type
df['Availability'] = df['Availability'].astype(str)

# convert the JSON strings to Python objects
df['Specifications'] = df['Specifications'].apply(lambda x: json.loads(x))



# Create a new DataFrame with the desired columns and format
new_df = pd.DataFrame({
    'slug': df['URL'],
    'title': df['Title'],
    'currency': Currency,
    'original_price': df['Actual Price'],
    'discounted_price': df['Discount Price'],
    'address': Address,
    'delivery_time_from': Delivery_time_from,
    'delivery_time_to': Delivery_time_to,
    'delivery_time_period': Delivery_time_period,
    'delivery_time_unparsed': Delivery_time_unparsed,
    'delivery_fee': Delivery_fee,
    'imgs': df['Image Link'],
    'brand': Brand,
    'average_rating': df['Rating'],
    'num_ratings': df['Review Count'],
    'reviews': df['Comments'],
    'similer_products': Similar_products,
    'category': Category,
    'availability': df['Availability'],
    'vendor': Vendor,
    'vendor_url': Vendor_url,

    'warranty_duration': Warranty_duration,
    'warranty_period': Warranty_period,

    'last_updated': Last_updated,
    'description': Description,
    'specifications': df['Specifications'],
    'used': Used,

    'warranty_type': Warranty_type,

    'delivery_details': Delivery_detail
})

# Write the new DataFrame to a JSON file
new_df.to_json(output_file, orient='records')

# Print data types of selected columns
print(type(new_df.at[1, 'slug']))
print(type(new_df.at[1, 'title']))
print(type(new_df.at[1, 'imgs']))
print(type(new_df.at[1, 'average_rating']))
print(type(new_df.at[8, 'num_ratings']))
print("Comments:",type(new_df.at[8, 'reviews']))
print("Comments:",new_df['reviews'])
print("Availability:",type(new_df.at[8, 'availability']))
print("Specifications:",type(new_df.at[8, 'specifications']))
print("Used:",type(Used))

# Read the JSON file into a pandas DataFrame
output_df = pd.read_json(output_file, orient='records')

# Print the DataFrames and loaded JSON data
print(output_df)
with open(output_file, 'r') as file:
    data = json.load(file)
    print(data)

# Print the data types of the DataFrames
print(new_df.dtypes)
print(output_df.dtypes)

# print the first 5 rows of the df
#print(df.head(2))
