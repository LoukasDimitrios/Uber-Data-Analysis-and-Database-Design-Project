# **Uber Data Analysis and Database Design Project**

## **Project Overview**
This project focuses on analyzing and processing a dataset of Uber trip data, aiming to construct a data warehouse schema composed of dimension and fact tables. The project is structured around the **Kimball methodology** for building a star schema. The dataset includes various attributes such as trip ID, passenger count, trip distance, fare amount, payment type, pickup and dropoff locations, and more. The main goal was to design an ETL process that converts raw data into a format suitable for analysis and reporting.

## **Process Overview**
The process consists of the following major steps:
1. **Data Cleaning and Preprocessing**: Importing and preparing the data for transformation and analysis.
2. **Dimensional Modeling**: Creating dimension tables that capture business-relevant entities, such as time (datetime), passenger count, trip distance, payment type, and locations.
3. **Fact Table Creation**: Combining the dimension tables with the raw trip data to create a fact table, which holds the core transactional data (trip details) and links to the dimension tables via foreign keys.
4. **Data Loading into MySQL**: Loading the processed data into a MySQL database, creating a well-structured schema for easy querying and reporting.

## **Step-by-Step Description**

### 1. **Loading and Preprocessing the Data**
The first step involved loading the raw Uber trip data from a CSV file. The data was inspected, cleaned, and transformed for further processing:
- **Datetime Processing**: The `pickup_datetime` and `dropoff_datetime` columns were converted into `datetime` format, allowing for easier manipulation and feature extraction.
- **Removing Duplicates**: Duplicates were removed to ensure data integrity.

### 2. **Dimension Tables Creation**
The following dimension tables were created from the dataset:

- **Datetime Dimension**: This table captures time-related attributes like the hour, day, month, and year of both pickup and dropoff times.
- **Passenger Count Dimension**: This table holds unique values for the passenger count, providing a reference for the number of passengers in each trip.
- **Trip Distance Dimension**: This table stores unique trip distance values, helping to normalize trip distances across the dataset.
- **Rate Code Dimension**: This table associates each trip's `RatecodeID` with a descriptive label (e.g., Standard Rate, JFK, Newark).
- **Location Dimensions (Pickup and Dropoff)**: These tables store unique combinations of pickup and dropoff locations using latitude and longitude coordinates.
- **Payment Type Dimension**: This table links each trip to a payment method (e.g., credit card, cash).

### 3. **Fact Table Construction**
Once the dimension tables were created, they were merged with the original trip data to create a **fact table**. This table includes:
- A unique `trip_id` for each record.
- Foreign keys to link to each of the dimension tables (e.g., `datetime_id`, `passenger_count_id`, `trip_distance_id`).
- Key metrics like `fare_amount`, `tip_amount`, and `total_amount`, which are the core facts of the dataset.

### 4. **Loading the Data into MySQL**
After constructing the fact and dimension tables, the final step was to load the data into a MySQL database. The process used the `pandas` library in Python to insert the data into MySQL tables via the `SQLAlchemy` engine:
- The fact table and dimension tables were created in the MySQL database.
- The tables were inserted into the database using the `to_sql()` function.
- The schema is now ready for analysis and querying.

## **Technologies Used**
- **Python**: For data manipulation, preprocessing, and ETL (using libraries like `pandas` and `sqlalchemy`).
- **MySQL**: For storing and querying the processed data in a structured database.
- **SQLAlchemy**: For connecting and interacting with the MySQL database from Python.
- **pandas**: For data manipulation and table creation.

## **Data Flow Diagram (Optional)**
You can include a diagram of the ETL process flow, if you have created one, to illustrate how the data moves from raw to processed form through the steps.

## **Running the Project**
### Requirements
- Python 3.x
- Required Python packages:
  ```bash
  pip install pandas mysql-connector-python sqlalchemy
