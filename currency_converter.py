import pandas as pd
import tarfile

# Extracting the tar file
with tarfile.open('dataset.tar.gz', 'r:gz') as tar:
    try:
        member = tar.getmember('dataset/MenuItem.csv')
        f = tar.extractfile(member)
        menu_item_df = pd.read_csv(f)
    except KeyError:
        print("MenuItem.csv not found in the tar file.")
    
    # Extracting other CSV files
    try:
        member = tar.getmember('dataset/Menu.csv')
        f = tar.extractfile(member)
        menu_df = pd.read_csv(f)
    except KeyError:
        print("Menu.csv not found in the tar file.")
    
    try:
        member = tar.getmember('dataset/MenuPage.csv')
        f = tar.extractfile(member)
        menu_page_df = pd.read_csv(f)
    except KeyError:
        print("MenuPage.csv not found in the tar file.")
    
    try:
        member = tar.getmember('dataset/Dish.csv')
        f = tar.extractfile(member)
        dish_df = pd.read_csv(f)
    except KeyError:
        print("Dish.csv not found in the tar file.")


#menu_item_df = pd.read_csv('MenuItem.csv')
#menu_df = pd.read_csv('Menu.csv')
#menu_page_df = pd.read_csv('MenuPage.csv')
#dish_df = pd.read_csv('Dish.csv')

# Merging the dataframes
df = pd.merge(menu_item_df, menu_page_df, left_on='menu_page_id', right_on='id', how='left')
df = pd.merge(df, menu_df, left_on='menu_id', right_on='id', how='left')

# Displaying the first few rows of the merged dataframe
print(df.head())

# drop unnecessary columns
df = df.drop(columns=['menu_page_id', 'created_at', 'xpos', 'ypos', 'id_y', 'keywords', 'menu_id', 'language', 'date', 'location', 'location_type', 'currency_symbol', 'status', 'page_count', 'dish_count'])

# Displaying the cleaned dataframe
print(df.columns)

# Renaming columns for clarity
df = df.rename(columns={
    'id_x': 'menu_item_id',
    'price': 'menu_item_price',
    'id_y': 'menu_page_id',
    'name_y': 'menu_page_name',
    'id': 'menu_id',
    'updated_at': 'date_recorded'
})




# keeping only relevant columns
df = df[['menu_item_id', 'menu_item_price', 'currency', 'dish_id', 'date_recorded']]

# Merging with Dish dataframe for date_recorded field
df = pd.merge(df, dish_df, left_on='dish_id', right_on='id', how='left')
df = df[['menu_item_id', 'menu_item_price', 'currency', 'dish_id', 'name', 'date_recorded']]

# Displaying the cleaned dataframe
print(df.head())

# Importing currency codes
curr_df = pd.read_csv('currency_codes.csv')

# Merging with currency codes
df = pd.merge(df, curr_df, left_on='currency', right_on='Currency Name', how='left')
df = df[['menu_item_id', 'menu_item_price', 'currency', 'dish_id', 'name', 'curr_code','date_recorded']]

# Converting 'date_recorded' to datetime format
df['date_recorded_pydt'] = pd.to_datetime(df['date_recorded'])

# Displaying the cleaned dataframe
print(df.head())


# Importing necessary libraries for currency conversion
from datetime import datetime
from forex_python.converter import CurrencyRates
import numpy as np

# Function to convert currency
def convert_to_usd(row):
    if row['curr_code'] == 'USD':
        #logging the conversion
        #print(f"No conversion needed for {row['menu_item_price']} USD on {row['date_recorded_pydt']}")

        return row['menu_item_price']
        
    elif pd.isna(row['curr_code']) or pd.isna(row['menu_item_price']):
        # Logging the missing currency code or price
        print(f"Missing currency code or price for row: {row}")
        return None
    
    else:
        try:
            print("loading c = CurrencyRates()")
            # Creating a CurrencyRates object
            c = CurrencyRates()

            # Converting the price to USD
            print(f"Attempting to convert {row['menu_item_price']} {row['curr_code']} to USD on {row['date_recorded_pydt']}")
            converted_price = c.convert(row['curr_code'], 'USD', row['menu_item_price'], row['date_recorded_pydt'].to_pydatetime())
            
            # Logging the conversion
            print(f"Converted {row['menu_item_price']} {row['curr_code']} to {converted_price} USD on {row['date_recorded_pydt']}")

            return converted_price
        except Exception as e:
            print(f"Error converting {row['menu_item_price']} {row['curr_code']} to USD: {e}")
            return None
        
#sort the dataframe by menu_item_id for troubleshooting
df = df.sort_values(by='menu_item_id')

# drop rows with missing currency codes or prices
df = df.dropna(subset=['curr_code', 'menu_item_price'])

c = CurrencyRates()
print(c.get_rates('USD').keys())  # Shows all supported codes against USD

# Applying the conversion function
#df['menu_item_price_usd'] = df.apply(convert_to_usd, axis=1)