# --- Step 0: Load Libraries ---
import pandas as pd
from sqlalchemy import create_engine

# --- Step 1: Load Data ---
# Load the Uber dataset from the CSV file into a pandas DataFrame
df = pd.read_csv("data/uber_data.csv")

# --- Step 2: Datetime Dimension Table Construction ---
# Convert pickup and dropoff columns to datetime format for consistency and further feature extraction
df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])

# Remove duplicate records and reset index to ensure integrity and uniqueness
df = df.drop_duplicates().reset_index(drop=True)

# Assign a unique trip identifier based on row index
df['trip_id'] = df.index

# Create a datetime dimension table by selecting and deduplicating relevant timestamp columns
datetime_dim = df[['tpep_pickup_datetime', 'tpep_dropoff_datetime']].drop_duplicates().reset_index(drop=True)

# Extract pickup datetime features: hour, day, month, year, and weekday
datetime_dim['pick_hour'] = datetime_dim['tpep_pickup_datetime'].dt.hour
datetime_dim['pick_day'] = datetime_dim['tpep_pickup_datetime'].dt.day
datetime_dim['pick_month'] = datetime_dim['tpep_pickup_datetime'].dt.month
datetime_dim['pick_year'] = datetime_dim['tpep_pickup_datetime'].dt.year
datetime_dim['pick_weekday'] = datetime_dim['tpep_pickup_datetime'].dt.weekday

# Extract dropoff datetime features: hour, day, month, year, and weekday
datetime_dim['drop_hour'] = datetime_dim['tpep_dropoff_datetime'].dt.hour
datetime_dim['drop_day'] = datetime_dim['tpep_dropoff_datetime'].dt.day
datetime_dim['drop_month'] = datetime_dim['tpep_dropoff_datetime'].dt.month
datetime_dim['drop_year'] = datetime_dim['tpep_dropoff_datetime'].dt.year
datetime_dim['drop_weekday'] = datetime_dim['tpep_dropoff_datetime'].dt.weekday

# Assign a unique identifier for each datetime record
datetime_dim['datetime_id'] = datetime_dim.index

# Reorganize the columns to match the desired dimension schema
datetime_dim = datetime_dim[[
    'datetime_id', 'tpep_pickup_datetime', 'tpep_dropoff_datetime', 
    'pick_hour', 'pick_day', 'pick_month', 'pick_year', 'pick_weekday', 
    'drop_hour', 'drop_day', 'drop_month', 'drop_year', 'drop_weekday'
]]

# --- Step 3: Passenger Count Dimension Table ---
# Create a dimension table for passenger count with unique values and an assigned ID
passenger_count_dim = df[['passenger_count']].drop_duplicates().reset_index(drop=True)
passenger_count_dim['passenger_count_id'] = passenger_count_dim.index
passenger_count_dim = passenger_count_dim[['passenger_count_id', 'passenger_count']]

# --- Step 4: Trip Distance Dimension Table ---
# Create a dimension table for trip distance with unique values and an assigned ID
trip_distance_dim = df[['trip_distance']].drop_duplicates().reset_index(drop=True)
trip_distance_dim['trip_distance_id'] = trip_distance_dim.index
trip_distance_dim = trip_distance_dim[['trip_distance_id', 'trip_distance']]

# --- Step 5: Rate Code Dimension Table ---
# Define the rate code types for clarity and assign a name to each rate code ID
rate_code_type = {
    1:"Standard Rate",
    2:"JFK",
    3:"Newark",
    4:"Nassau of Westchester",
    5:"Negotiated fare",
    6:"Group ride"
}

# Create a dimension table for rate codes with unique values and assigned names based on the rate code ID
rate_code_dim = df[['RatecodeID']].drop_duplicates().reset_index(drop=True)
rate_code_dim['rate_code_id'] = rate_code_dim.index
rate_code_dim['rate_code_name'] = rate_code_dim['RatecodeID'].map(rate_code_type)
rate_code_dim = rate_code_dim[['rate_code_id', 'RatecodeID', 'rate_code_name']]

# --- Step 6: Pickup Location Dimension Table ---
# Create a dimension table for pickup locations with unique values for longitude and latitude
pickup_location_dim = df[['pickup_longitude', 'pickup_latitude']].drop_duplicates().reset_index(drop=True)
pickup_location_dim['pickup_location_id'] = pickup_location_dim.index
pickup_location_dim = pickup_location_dim[['pickup_location_id', 'pickup_longitude', 'pickup_latitude']]

# --- Step 7: Dropoff Location Dimension Table ---
# Create a dimension table for dropoff locations with unique values for longitude and latitude
dropoff_location_dim = df[['dropoff_longitude', 'dropoff_latitude']].drop_duplicates().reset_index(drop=True)
dropoff_location_dim['dropoff_location_id'] = dropoff_location_dim.index
dropoff_location_dim = dropoff_location_dim[['dropoff_location_id', 'dropoff_longitude', 'dropoff_latitude']]

# --- Step 8: Payment Type Dimension Table ---
# Define the payment types for clarity and assign a name to each payment type ID
payment_type_name = {
    1:"Credit card",
    2:"Cash",
    3:"No charge",
    4:"Dispute",
    5:"Unknown",
    6:"Voided trip"
}

# Create a dimension table for payment types with unique values and assigned names based on the payment type ID
payment_type_dim = df[['payment_type']].drop_duplicates().reset_index(drop=True)
payment_type_dim['payment_type_id'] = payment_type_dim.index
payment_type_dim['payment_type_name'] = payment_type_dim['payment_type'].map(payment_type_name)
payment_type_dim = payment_type_dim[['payment_type_id', 'payment_type', 'payment_type_name']]

# --- Step 9: Create Fact Table by Merging with Dimension Tables ---
fact_table = df \
    .merge(passenger_count_dim, on='passenger_count') \
    .merge(trip_distance_dim, on='trip_distance') \
    .merge(rate_code_dim, on='RatecodeID') \
    .merge(pickup_location_dim, on=['pickup_longitude', 'pickup_latitude']) \
    .merge(dropoff_location_dim, on=['dropoff_longitude', 'dropoff_latitude']) \
    .merge(datetime_dim, on=['tpep_pickup_datetime', 'tpep_dropoff_datetime']) \
    .merge(payment_type_dim, on='payment_type') \
    [['trip_id', 'VendorID', 'datetime_id', 'passenger_count_id',
      'trip_distance_id', 'rate_code_id', 'store_and_fwd_flag', 'pickup_location_id',
      'dropoff_location_id', 'payment_type_id', 'fare_amount', 'extra', 'mta_tax',
      'tip_amount', 'tolls_amount', 'improvement_surcharge', 'total_amount']]

# --- Step 10: Send Data to MySQL ---

create_engine('mysql+pymysql://root:**********@localhost/uber_project_db')"

# Send dimension tables to MySQL
passenger_count_dim.to_sql('passenger_count_dim', con=engine, if_exists='replace', index=False)
trip_distance_dim.to_sql('trip_distance_dim', con=engine, if_exists='replace', index=False)
rate_code_dim.to_sql('rate_code_dim', con=engine, if_exists='replace', index=False)
pickup_location_dim.to_sql('pickup_location_dim', con=engine, if_exists='replace', index=False)
dropoff_location_dim.to_sql('dropoff_location_dim', con=engine, if_exists='replace', index=False)
datetime_dim.to_sql('datetime_dim', con=engine, if_exists='replace', index=False)
payment_type_dim.to_sql('payment_type_dim', con=engine, if_exists='replace', index=False)
# Send fact table to MySQL
fact_table.to_sql('fact_table', con=engine, if_exists='replace', index=False)

print("Tables have been successfully loaded into MySQL.")
