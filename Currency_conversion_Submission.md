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

### 3. Missing Value (NaN) Management

- Detected missing or NaN values in both float and non-float columns using `.isna()`, `pd.isna()`, and related utilities.
- Dropped rows or columns with excessive missingness, or imputed default values as needed.

### 4. Joining and Merging Data

- Merged/joined DataFrames on one or more columns, including support for join keys with different names (using `merge()` with `left_on`/`right_on`).
- Facilitated robust integration of data across files and tables.

### 5. Currency Conversion to USD with Historic Rates

- Used the **forex-python** library to fetch live and historical FX rates.
- Converted prices from source currencies to USD, leveraging each record’s transaction date for accurate historical rates.
- Ensured date columns were properly converted to `datetime` before processing.

### 6. Inflation Adjustment

- Applied inflation adjustment to USD-valued prices using the `cpi` library.
- Normalized amounts to a common comparison year (e.g., 2025) for consistent analysis across time.

### 7. Data Wrangling Techniques

- Identified and dropped NaN values, or rows/columns, as necessary.
- Used pandas idioms such as `dropna`, `sort_values`, and column subset selection for efficient cleanup.
- Retrieved specific rows for inspection and debugging.
- Employed robust error handling and type checking (e.g., calling `.isna()` on Series, or `pd.isna()` for scalars).

### 8. Extensibility & Automation

- Modularized cleaning workflows, separating task-level cleaning (“inner” workflows) from orchestration and data management (“outer” workflows).
- Where applicable, incorporated prompt-based or API-driven normalization for complex text fields.

## Final Output

The final, cleaned dataset:

- Contains price values converted to USD (using forex-python and proper historic FX rates) and adjusted for inflation
- Features standardized column names and data types
- Is free from unwanted rows, duplicate records, and excessive missing values
- Is fully prepared for downstream analytics, visualization, or further data science tasks

## Tools and Libraries Used

- **pandas**: Data wrangling and manipulation
- **tarfile, requests**: Handling archives and retrieving data from web sources
- **forex-python**: Currency conversion, including historic conversion rates
- **cpi**: Inflation adjustment
- **numpy**: NaN/missing value checks
- *(Optional)* Azure OpenAI: Advanced text normalization (where appropriate)

---

This structured and modular workflow ensures accuracy, repeatability, and transparency, providing a trustworthy foundation for subsequent analytics and applications.