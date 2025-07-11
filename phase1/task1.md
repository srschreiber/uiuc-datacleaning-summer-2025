# Task 1: Describe the Dataset

## ER Diagram

![ER Diagram](../images/er_diagram.png)

## Description

## Origin and Source

This dataset originates from the **New York Public Library’s “What’s on the Menu?”** project, an initiative to **digitize historical menus** from the collection. The dataset contains **45,000 menus** spanning from the **1840s to the present**. As of November 2016, the transcribed database includes over **1.3 million dishes** extracted from **17,545 menus**. It consists of `Menu`, `MenuPage`, `MenuItem`, and `Dish` tables, form a relational database schema. One `Menu` can have multiple `MenuPage`s, each containing multiple `MenuItem`s, which reference a `Dish`. The dataset is available on [Kaggle](https://www.kaggle.com/datasets/nypl/whats-on-the-menu) and is updated twice monthly.

---

## Data Structure and Attributes

The dataset is organized into **four CSV files**: `Menu`, `MenuPage`, `MenuItem`, and `Dish`, representing a relational schema.

### Menu

Represents the overall menu document.

| Column | Description |
|--------|-------------|
| `id` | Unique identifier for the menu |
| `name` | Title of the menu |
| `sponsor` | Organization or host behind the menu |
| `event` | Name of the event |
| `venue` | Type of place (e.g., COMMERCIAL) |
| `place` | City and state/country (e.g. MILWAUKEE, [WI];) |
| `physical_description` | Format and dimensions (e.g., “CARD; 5.5X8.0”) |
| `occasion` | Occasion related to the menu (e.g., holiday) |
| `notes` | Any special notes (e.g., decoration style) |
| `call_number` | Library reference number |
| `keywords` | Keywords or tags (often null) |
| `language` | Language of the menu text |
| `date` | Date the menu was issued |
| `location` | Alternate location description |
| `location_type` | Type of location (may be null) |
| `currency` | Currency used (e.g., USD) |
| `currency_symbol` | Symbol (e.g., $) |
| `status` | Processing status (e.g., “complete”) |
| `page_count` | Number of scanned pages in the menu |
| `dish_count` | Number of dishes identified on the menu |

---

### MenuPage

Represents a **single page of a menu**.

| Column | Description |
|--------|-------------|
| `id` | Unique ID for the page |
| `menu_id` | Foreign key linking to the `Menu` |
| `page_number` | Page index (starting at 1) |
| `image_id` | Identifier for the scanned image |
| `full_height` | Image height in pixels |
| `full_width` | Image width in pixels |
| `uuid` | unique identifier for the page |

---

### MenuItem

Represents a **dish offering on a specific menu page**.

| Column | Description |
|--------|-------------|
| `id` | PK |
| `menu_page_id` | Foreign key to `MenuPage` |
| `dish_id` | Foreign key to `Dish` (canonical dish concept) |
| `price` | Listed price of the dish |
| `high_price` | Optional upper bound |
| `created_at` | Timestamp when the item was entered |
| `updated_at` | Timestamp of last update |
| `xpos`, `ypos` | Coordinates in range (0,1) of the item position on the scanned image |

---

### Dish

Represents a **a dish**.

| Column | Description |
|--------|-------------|
| `id` | Unique dish ID |
| `name` | Name of the dish (e.g., “Tomato Soup”) |
| `description` | Additional details (often null) |
| `menus_appeared` | Number of distinct menus the dish appeared on |
| `times_appeared` | Total appearances (can be more than `menus_appeared`) |
| `first_appeared` | Earliest known year it appeared |
| `last_appeared` | Most recent year seen |
| `lowest_price` | Minimum price seen |
| `highest_price` | Maximum price seen |

---

## Metadata Context

- **Time Period** - 1840s-present  
- **Number of Columns** - 45 total
- **File Size** - 152.68 MB, with the bulk occupied by the `Menu Item` table (118 MB)

---

