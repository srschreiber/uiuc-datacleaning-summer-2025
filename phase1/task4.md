# Task 4: Initial Data Cleaning Plan
U1: 
- What are the items that have the most longevity and staying power on menus throughout the ages
- How did the cost of popular dishes change over time wrt inflation?

S1: 
The dataset D consists of four tables: `Menu`, `MenuPage`, `MenuItem`, and `Dish`. The main use case U1 focuses on analyzing the longevity and popularity of dishes over time. This requires cleaning the `Dish` table to ensure that dish names are standardized, as many dishes appear in various forms. The `MenuItem` table will also need to be cleaned to ensure accurate linking to the `Dish` table. We also need to ensure there is no double counting, e.g. all the one to many relationships are properly maintained and determine a strategy for deciding which record to keep in case of duplicates.

S2:
We will run a profiling analysis on the dataset to identify quality problems such as:
- Duplicate dish names and variations in naming conventions or languages (like Coffee vs café).
- Violated foreign key constraints between `MenuItem` and `Dish`, `Menu` and `MenuPage`, `MenuPage` and `MenuItem`. For example, does a Menu Page really belong to a Menu? 
- Violated primary key constraints, such as null or duplicate IDs.
- Inconsistent date formats and missing dates in the `Menu` table.
- Anomalies in price data, such as unrealistic values or ranges. 

S3: 
We will use the following tools for data cleaning:
- **OpenRefine** for identifying and resolving simple issues such as case normalization, data violations, clustering + collapsing dish names
- **Azure OpenAI** to normalize dish names standardized to English without brand names or modifiers
- **SQL** for validating foreign key relationships and ensuring data integrity across tables.
- **Python** for more complex data transformations, such as merging duplicate dish records and handling missing values.

S4:
After cleaning, we will evaluate the dataset D′ by:
- Checking for the absence of duplicate dish names and ensuring that all dish names are standardized.
- Validating that all foreign key relationships are intact and correctly linked.
- Ensuring that there are no null or duplicate IDs in primary key columns.
- Confirming that date formats are consistent and that missing dates have been addressed.
- Demonstrating that the new dataset contains fewer dishes due to normalization which can be more accurately analyzed.

S5:
We will summarize the changes from D to D′ by:
- Documenting the number of dish names standardized and the reduction in duplicates.
- Listing the foreign key relationships that were corrected or established.
- Reporting on the number of records cleaned, including any removed or merged records.
- Providing statistics on the consistency of date formats and the handling of missing values.
- Summarizing how many currencies were converted to USD and the impact on price data.

## Project Task Assignments

### Sam (Focus on popular Dishes usecase)
- Standardize dish names using Azure OpenAI and collapse the dish names, updating the FK constraints.
- Overwrite the Dish's times appeared, menus appeared, first appeared, and last appeared columns with the 
values after the standardization.
- Summarize the changes made to the dataset and document the cleaning process.

### Fahad (Focus on price of popular Dishes over time usecase)

- Convert all currency to USD (maybe use forex)
```
from forex_python.converter import CurrencyRates
from datetime import datetime

cr = CurrencyRates()
date_obj = datetime(2020, 1, 1)
cr.get_rate('EUR', 'USD', date_obj)
```
- Update MenuItem prices to reflect the conversion to USD.
- Update Dish's lowest_price and highest_price columns with the converted values.
- Summarize the changes made to the dataset and document the cleaning process.

### Patrick (Focus on data integrity and consistency)
- Detect foreign key violations, such as MenuPage belongs to one Menu, MenuItem belongs to one MenuPage, and MenuItem has a valid dish and filter them out
- Fix duplicate MenuPage, and MenuItem appearing on multiple pages.
- Remove columns with 100% null values.
- Detect duplicate primary keys 
- Clean the menu date formats and ensure they are reasonable
- Summarize the changes made to the dataset and document the cleaning process.
