# Workflow Design (W1) — Data Integrity and Cleaning Workflow

## Overview
This document outlines the design of our overall workflow (W1) for ensuring data integrity and consistency in the NYPL "What's on the Menu?" dataset. The workflow focuses on detecting and correcting structural data issues across four related tables (Menu, MenuPage, MenuItem, Dish) before moving to semantic cleaning phases. 

W1 is structured into clear phases: **Data Loading, Data Profiling (including Integrity Constraint Violation Checks), Data Cleaning, and Output Generation**. Each phase is composed of modular, traceable steps with defined input-output dependencies.

---

## Workflow Phases and Steps

### Phase 1: Data Loading (DL)
- **Step 1.1**: Load raw CSV files into Pandas DataFrames.
- **Step 1.2**: Load the same CSVs into an in-memory SQLite database to support SQL-based profiling.
- **Tools Used**: Python (Pandas, SQLite3)
- **Rationale**: 
  - Pandas provides efficient in-memory data structures for transformation and cleaning.
  - SQLite is lightweight and enables SQL-style data profiling without external database dependencies.

---

### Phase 2: Data Profiling & Integrity Constraint Violation Checks (DP)
- **Step 2.1**: Run SQL queries to detect:
  - Orphan foreign key references (MenuPage → Menu, MenuItem → MenuPage, MenuItem → Dish)
  - Duplicate primary keys in MenuPage, MenuItem, Dish
  - Duplicate `page_number` within the same menu
  - MenuItems appearing on multiple pages
  - Invalid page numbers (<1 or NULL)
  - Invalid dates in Menu.date, Dish first_appeared/last_appeared
  - MenuItem created_at > updated_at inconsistencies
  - Columns with 100% NULL values
- **Tools Used**: SQLite (SQL queries), Python (SQLite3 library)
- **Rationale**:
  - SQL is inherently suited for relational integrity checks and profiling.
  - Using SQLite allows for portable, efficient execution of complex queries directly on the CSV-loaded schema.
  - Python is used for executing the queries and generating a log of the query results. 

---

### Phase 3: Data Cleaning & Transformation (DC)
- **Step 3.1**: Remove orphan records violating foreign key constraints.
- **Step 3.2**: Deduplicate records in MenuPage and MenuItem tables.
- **Step 3.3**: Validate and fix MenuPage.page_number:
  - Ensure page_number ≥ 1
  - Ensure uniqueness of (menu_id, page_number) pairs
- **Step 3.4**: Ensure MenuItem does not appear on multiple pages (per dish_id).
- **Step 3.5**: Remove columns with 100% NULL values.
- **Step 3.6**: Validate and fix primary key constraints (no nulls, no duplicates).
- **Step 3.7**: Clean and standardize date formats across Menu, Dish, and MenuItem:
  - Date ranges clamped between 1800–2025
  - Ensure logical date order (first_appeared ≤ last_appeared)
  - Align MenuItem.created_at ≤ updated_at
- **Tools Used**: Python (Pandas)
- **Rationale**:
  - Pandas excels at batch data transformations and allows flexible, scriptable cleaning logic.
  - A modular function-based cleaning script ensures reproducibility and step-wise validation.

---

### Phase 4: Output Generation (OL)
- **Step 4.1**: Save cleaned dataframes as new CSV files.
- **Step 4.2**: Generate a detailed cleaning log summarizing all violations detected and corrected.
- **Tools Used**: Python (Pandas, File I/O)
- **Rationale**:
  - File-based outputs are practical for downstream analysis.
  - A persistent log ensures transparency of the cleaning process.

---

## Workflow Dependencies
- Data profiling (SQL checks) depends on successful data loading into SQLite.
- Cleaning steps are strictly dependent on profiling results (e.g., orphan detection precedes deduplication).
- Date fixes and primary key corrections occur after structural cleaning steps to avoid redundant operations.
- Outputs are generated only after all cleaning steps are completed.

---

## Why This Design & Toolset?
- **Python (Pandas)**: Versatile, scalable for structured data cleaning tasks.
- **SQLite (SQL Profiling)**: Allows precise, relational integrity checks using declarative SQL logic, lightweight setup.
- **Script-based Workflow**: Ensures modular, reproducible data cleaning process, adaptable for iterative refinement.
- **Log-Driven Auditing**: Guarantees traceability of all modifications applied to the dataset.

---