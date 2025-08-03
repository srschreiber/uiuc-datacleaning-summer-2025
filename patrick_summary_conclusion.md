# Project Summary: Cleaning and Profiling the NYPL Menus Dataset

## Overview

Our project focused on cleaning and profiling the New York Public Library’s “What’s on the Menu?” dataset, which contains historical menu records from the 1840s to the present. The dataset comprises four relational tables: `Menu`, `MenuPage`, `MenuItem`, and `Dish`. The primary goal was to prepare this data for two use cases:

- **U1**: What are the items that have the most longevity and staying power on menus throughout the ages?
- **U1**: How did the cost of popular dishes change over time with respect to inflation?

## Summary of Work Completed

The task that I, Patrick Wu, completed consisted of several aspects:

### Data Profiling (Integrity Checks)
- SQL queries were developed and executed to identify:
  - Orphan records violating foreign key constraints.
  - Duplicate primary keys and row entries.
  - Page number inconsistencies and duplicates within the same menu.
  - Invalid or missing dates across all tables.
  - Logical inconsistencies like `created_at > updated_at`.
  - Columns that were entirely null.

### Data Cleaning (Python Script)
A systematic Python script was developed and executed to:
- Filter out foreign key violations (e.g., orphaned `MenuPage`, `MenuItem`, or `Dish` references).
- Ensure `page_number` values are valid (positive integers ≥ 1) and unique within a `menu_id`.
- Remove redundant records (duplicate rows) across `MenuPage` and `MenuItem`.
- Drop columns with 100% null values (e.g., `keywords`, `language`, `location_type`, `description`).
- Correct invalid or inconsistent date values:
  - Clipped dates outside the 1800–2025 range.
  - Corrected reversed `first_appeared` > `last_appeared`.
  - Standardized `created_at` timestamps to never exceed `updated_at`.

All changes were logged in `patrick_cleaning_log.txt` to maintain traceability and transparency.

## Overall Contributions by Patrick Wu

Patrick contributed significantly to ensuring data **integrity and consistency** by:
- Writing and executing comprehensive **SQL profiling queries** to uncover integrity constraint violations.
- Developing a robust and modular **Python data cleaning script** to enforce primary/foreign key rules, remove duplicate records, validate page numbers, and correct problematic date fields.
- Generating a detailed **cleaning log** that documents over **60,000+ individual corrections**, including:
  - 5,800+ foreign key issues fixed in `MenuPage`.
  - 19,900+ `MenuItem` duplicates across pages removed.
  - 2,800+ timestamp corrections in `MenuItem`.

These efforts ensured that the cleaned dataset (`D′`) is fully relationally consistent, primed for high-quality analysis, and significantly more reliable than the original (`D`).

## Lessons Learned

- **Data integrity checks are critical**: Many datasets, even those from reputable sources, may contain subtle but serious structural issues.
- **Relational validation is foundational**: Orphaned references and duplicate keys can silently undermine downstream analytics if left unchecked.
- **Comprehensive logging matters**: Systematically logging all changes during cleaning enhances reproducibility and accountability.
- **Multitool workflows work best**: Combining SQL (for diagnostics), Python (for fixes), and and tools (like modeling workflows to keep track of provenance) ensure that the project is completed efficiently and without delay. 
- **Iterative collaboration yields quality**: Cleaning this dataset required tight feedback loops between profiling, fixing, and verification. It was necessary to take iterative steps when cleaning this dataset to ensure transparency in tracking changes to the data. 

## Conclusion

This project successfully transformed a noisy and inconsistent dataset into a structurally sound, analyzable version that supports both descriptive and temporal analysis of menu trends. With Patrick’s strong contributions to data profiling and integrity repair, the dataset was well-prepared and ready for in-depth exploration of historical dish popularity and pricing trends. Altogether, the contributions of all three teammates to this project ensured a profound transformation of the dataset from its dirty and raw form to a clean and usable form. 
