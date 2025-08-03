# Phase II Report

## Currency Normalization Workflow

### Fahad Khan (mfkhan5@illinois.edu)

## Overview

This step involved cleaning, unifying, and standardizing datasets containing transaction records in various currencies and time periods. The primary objectives were:

- Resolve missing or invalid data
- Normalize and convert price values (including currency conversion and inflation adjustment)
- Prepare the cleaned, analysis-ready dataset

## Key Data Cleaning Steps

### 1. Data Ingestion & Structure

- Loaded raw data from CSV files within `.tar.gz` compressed archives.
- Utilized `pandas` for efficient reading, inspection, and transformation.

### 2. Standardization and Normalization

- Selected only relevant columns, dropping unnecessary ones.
- Standardized column names and ensured correct data types (e.g., converting date fields to pandas `datetime`).
- Removed duplicate records from the dataset.

#### Rationale for U1

- Needed to ensure that each menu_item was added at a valid dates and dropped invalid dates

### 3. Missing Value (NaN) Management

- Detected missing or NaN values in both float and non-float columns using `.isna()`, `pd.isna()`, and related utilities.
- Dropped rows or columns with excessive missing values, and/or imputed default values as needed.

#### Rationale for U1

- Needed to ensure that missing data is excluded from analysis

### 4. Joining and Merging Data

- Merged/joined DataFrames on one or more columns, including support for join keys with different names (using `merge()` with `left_on`/`right_on`).
- Facilitated robust integration of data across files and tables.

### Rationale for U1

- Data needed for this exercise was spread across many different files
- Menu_item needed to be joined with Dish to look up the dish name
- Menu_item needed to be joined to Menu_page so that the ultimate Menu could be determined via an additional join with the Menu table
- The Menu table had the currency, and data_recorded for the Menu_item

### 5. Converting Currency column to currency code

- Obtained list of currencies included in NYPL dataset
- Manually created look up table for ISO currency codes
- Looked up currency code and added as a new column 'curr_code'

#### Rationale for U1

- To convert currencies using any python library, the english language currency column needed to be converted to the ISO currency code

### 6. Currency Conversion to USD with Historic Rates

- Used the **forex-python** library to fetch live and historical FX rates.
- Converted prices from source currencies to USD, leveraging each record’s transaction date for accurate historical rates.

### 7. Inflation Adjustment

- Applied inflation adjustment to USD-valued prices using the `cpi` library.
- Normalized amounts to a common comparison year (2024) for consistent analysis across time.


### 8. Extensibility & Automation

- Modularized cleaning workflows, separating task-level cleaning (“inner” workflows) from orchestration and data management (“outer” workflows).
- Where applicable, incorporated prompt-based or API-driven normalization for complex text fields.

## Final Output

The final, cleaned dataset:

- Is written to CSV
- Contains price values converted to USD (using forex-python and proper historic FX rates) and adjusted for inflation
- Features standardized column names and data types
- Is free from unwanted rows, duplicate records, and missing values
    - 65% of the dataset was retained while the rest was dropped
    - Original dataset had 1,332,726 rows. Cleaned dataset had 875,767 rows
- Is fully prepared for downstream analytics, visualization, or further data science tasks

## Tools and Libraries Used

- **pandas**: Data wrangling and manipulation
- **tarfile**: Handling archives and retrieving data from web sources
- **forex-python**: Currency conversion, including historic conversion rates
- **cpi**: Inflation adjustment
- **numpy**: NaN/missing value checks