# Data Cleaning Summary

## Description of Data Cleaning Performed

This document outlines the high-level data cleaning steps applied to the NYPL "What's on the Menu?" dataset. These operations were essential for ensuring data integrity, consistency, and analytical reliability, particularly in support of Use Case U1: analyzing the longevity and popularity of dishes across time.

---

## 1. Fixing Foreign Key Violations

### Description:
Removed records with invalid foreign key relationships:
- MenuPage.menu_id not found in Menu
- MenuItem.menu_page_id not found in MenuPage
- MenuItem.dish_id not found in Dish

### Rationale:
Invalid foreign key references would lead to orphaned records and distort relational integrity, preventing accurate aggregation and analysis.

### Relevance to U1:
Required — U1 depends on correct linkage between dishes and the menus they appear on. Orphaned or broken links would result in incomplete or inaccurate counts of dish appearances over time.

---

## 2. Deduplication of Rows

### Description:
Checked for and removed duplicate rows in:
- MenuPage
- MenuItem
- Combined dish_id and menu_page_id in MenuItem to prevent the same dish from appearing on multiple pages erroneously.

### Rationale:
Redundant rows inflate statistics, especially in aggregate analyses such as counting the frequency of dish appearances.

### Relevance to U1:
Required — Dish popularity calculations would be skewed if the same dish was counted multiple times across duplicate entries or multiple pages.

---

## 3. Page Number Validity and Uniqueness

### Description:
- Replaced null or invalid page_number values with 1.
- Removed duplicate page numbers within the same menu_id.

### Rationale:
Ensures that page sequencing within each menu is logical and unambiguous.

### Relevance to U1:
Not strictly required — While not essential to dish popularity, maintaining clean pagination supports any future UI/UX or page-based visualizations and reinforces schema validity.

---

## 4. Removal of Fully Null Columns

### Description:
Dropped columns where all values were null:
- Menu.keywords, language, location_type
- Dish.description

### Rationale:
These columns contained no usable information and contributed noise to the dataset.

### Relevance to U1:
Not required — These columns were not needed for U1, but removing them improves processing speed and reduces storage.

---

## 5. Primary Key Validations

### Description:
Checked and enforced uniqueness and non-null constraints on primary keys across all tables.

### Rationale:
Maintaining unique primary keys is foundational to any relational database schema and prevents ambiguous joins.

### Relevance to U1:
Required — Ensures every row represents a unique, valid entity that can be reliably referenced or aggregated.

---

## 6. Date Standardization and Correction

### Description:
- Standardized Menu.date to a valid datetime format and restricted to 1800–2025.
- Validated and capped Dish.first_appeared and last_appeared to 2025.
- Ensured first_appeared ≤ last_appeared (fixed violations).
- Corrected MenuItem.created_at to not exceed updated_at.

### Rationale:
Invalid or inconsistent date fields can undermine time-series analysis and lead to misleading results.

### Relevance to U1:
Required — Accurate temporal data is central to measuring longevity and popularity trends over decades.
