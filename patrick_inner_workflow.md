# Inner Workflow Model (W2): Data Integrity Cleaning Workflow

## Workflow Name: Data Integrity & Consistency Cleaning (W2)

This document describes the detailed inner workflow (W2) of the data cleaning process used to enforce data integrity and consistency across the Menu, MenuPage, MenuItem, and Dish tables from the NYPL "What's on the Menu?" dataset.

---

## Workflow Overview

**Input Files:**

- Menu.csv
- MenuPage.csv
- MenuItem.csv
- Dish.csv

**Output Files:**

- Cleaned Menu.csv
- Cleaned MenuPage.csv
- Cleaned MenuItem.csv
- Cleaned Dish.csv
- cleaning\_log.txt

---

## Workflow Phases and Steps

### Phase 1: Data Loading

- **Step 1.1:** Load CSV files into Pandas DataFrames.
  - Inputs: Raw CSV files
  - Output: Loaded DataFrames (menu, menupage, menuitem, dish)

### Phase 2: Data Profiling & Integrity Checks

- **Step 2.1:** Validate Foreign Key Constraints

  - MenuPage.menu\_id must exist in Menu.id: Remove MenuPage records with invalid menu\_id 
  - MenuItem.menu\_page\_id must exist in MenuPage.id: Remove MenuItem records with invalid menu\_page\_id
  - MenuItem.dish\_id must exist in Dish.id: Remove MenuItem records with invalid dish\_id
  - Log violations removed

- **Step 2.2:** Detect Duplicate Rows

  - Check for duplicate rows in MenuPage and MenuItem tables by using drop\_duplicates() on MenuPage and MenuItem
  - Log if any duplicates found and removed

- **Step 2.3:** Validate Page Number Integrity

  - Fix MenuPage.page\_number < 1 or NULL to 1
  - Ensure MenuPage.page\_number uniqueness within the same menu\_id and drop rows with duplicate page\_number values within same menu\_id
  - Log changes made

- **Step 2.4:** Detect MenuItems appearing on multiple pages

  - Deduplicate MenuItem based on (dish\_id, menu\_page\_id)
  - Log changes made

- **Step 2.5:** Remove Fully Null Columns

  - Identify and drop columns that are 100% NULL in Menu, MenuPage, MenuItem, Dish tables
  - Log columns dropped

- **Step 2.6:** Validate Primary Key Integrity

  - Remove records with NULL primary key values in each table
  - Remove duplicate primary key records in each table
  - Log violations removed

- **Step 2.7:** Validate and Clean Date Fields

  - Parse to datetime, ensure Menu.date is within [1800-2025], coerce invalid formats to NULL
  - Correct Dish.first\_appeared and Dish.last\_appeared to be within valid year range [1800-2025]
  - If Dish.first\_appeared > Dish.last\_appeared, make first\_appeared = last\_appeared
  - Similarly, ensure MenuItem.created\_at <= updated\_at
  - Log changes made

---

## Phase 3: Output & Logging

- **Step 3.1:** Save Cleaned DataFrames

  - Export cleaned Menu, MenuPage, MenuItem, Dish tables to CSV files

- **Step 3.2:** Generate Cleaning Log

  - Summarize all violations found and corrections applied
  - Output to cleaning\_log.txt

---

## Tools & Justification

| Tool            | Purpose                                                     |
| --------------- | ----------------------------------------------------------- |
| Python (Pandas) | Data loading, profiling, cleaning, and export operations    |
| Python File I/O | Logging cleaning actions into a structured text log file    |
| CSV Files       | File-based input/output ensures compatibility & portability |

---

## Workflow Outputs

- **Cleaned CSV Files:**

  - Menu.csv
  - MenuPage.csv
  - MenuItem.csv
  - Dish.csv

- **Cleaning Log File:**

  - cleaning\_log.txt (detailed summary of all changes applied)


