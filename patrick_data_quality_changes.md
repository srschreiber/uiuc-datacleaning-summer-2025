
# Data Quality Improvement Report

## Summary Table of Data Quality Changes

| Constraint / Column                              | Table         | Violations Before | Violations After | Cells Changed |
|--------------------------------------------------|---------------|-------------------|------------------|---------------|
| Foreign Key: `MenuPage.menu_id`                  | MenuPage      | 5,803             | 0                | 5,803         |
| Foreign Key: `MenuItem.menu_page_id`             | MenuItem      | 5,373             | 0                | 5,373         |
| Foreign Key: `MenuItem.dish_id`                  | MenuItem      | 244               | 0                | 244           |
| Page Number Validity (`< 1` or NULL)             | MenuPage      | 945               | 0                | 945           |
| Duplicate `page_number` within same `menu_id`    | MenuPage      | 62                | 0                | 62            |
| MenuItem on Multiple Pages (duplicate dish-page) | MenuItem      | 19,935            | 0                | 19,935        |
| Fully Null Column: `Menu.keywords`               | Menu          | 1                 | 0                | 17,545        |
| Fully Null Column: `Menu.language`               | Menu          | 1                 | 0                | 17,545        |
| Fully Null Column: `Menu.location_type`          | Menu          | 1                 | 0                | 17,545        |
| Fully Null Column: `Dish.description`            | Dish          | 1                 | 0                | 423,397       |
| Date Format: `Menu.date`                         | Menu          | 586               | 0                | 586           |
| Date Range: `Dish.first_appeared`                | Dish          | 11                | 0                | 11            |
| Date Range: `Dish.last_appeared`                 | Dish          | 179               | 0                | 179           |
| `MenuItem.created_at > updated_at` (Inversion)   | MenuItem      | 2,843             | 0                | 2,843         |
| Primary Key Nulls or Duplicates                  | All tables    | 0                 | 0                | 0             |

## Integrity Constraint (IC) Violation Report Comparison

| IC Type                                | Violations Before | Violations After | Improvement (%) |
|----------------------------------------|-------------------|------------------|-----------------|
| Foreign Key Violations (all FK checks) | 11,420            | 0                | 100%            |
| Primary Key Nulls/Duplicates           | 0                 | 0                | 0%              |
| Duplicate Rows (MenuPage/MenuItem)     | 0                 | 0                | 0%              |
| Page Number Validity                   | 945               | 0                | 100%            |
| Page Number Uniqueness within Menu     | 62                | 0                | 100%            |
| MenuItem on Multiple Pages (duplicates)| 19,935            | 0                | 100%            |
| Fully Null Columns                     | 4 columns         | 0 columns        | 100%            |
| Date Violations (all date checks)      | 3,619             | 0                | 100%            |

## Demonstration of Data Quality Improvements

1. **Foreign Key Consistency**: All orphan records (MenuPage with invalid Menu, MenuItem with invalid MenuPage/Dish) have been removed — **11,420 invalid references fixed**.
2. **Page Number Integrity**: Invalid page numbers (<1 or null) and duplicate page numbers within a menu were fixed — **1,007 violations corrected**.
3. **Eliminated MenuItem-Dish duplicates across pages** — **19,935 overcounts eliminated**, ensuring no double counting of dish appearances.
4. **Reduced Schema Complexity**: Removed **4 fully null columns**, cleaning up **476,032 unnecessary cells**.
5. **Date Standardization**: All date-related inconsistencies (format, out-of-range years, inversion) — **3,619 violations corrected**.
6. **Primary Keys Validation**: No null or duplicate primary keys were found, confirmed integrity is intact.
7. **Overall IC Violation Reduction**: From **~35,000+ IC violations** → **0 remaining violations** (100% cleaned).

---

