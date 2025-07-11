# Task 1: Describe the Dataset

- Provide a relational schema or ER diagram of the dataset.
- Write a short narrative that explains:
  - The origin and source of the dataset.
  - What each column or attribute represents.
  - Any relevant metadata (e.g., time period covered, geographic scope, etc.).


## Relationship

### Menu

- id (PK)

- sponsor, event, venue, place, date, etc.

- Describes an overall menu event (e.g., hotel dinner).

### MenuPage

- id (PK)

- menu_id (FK to Menu)

- page_number, image_id, uuid, etc.

- Represents a specific page of a menu.

### MenuItem

- id (PK)

- menu_page_id (FK to MenuPage)

- dish_id (FK to Dish)

- price, high_price, xpos, ypos, created_at, updated_at

Represents a dish and its price on a specific menu page.

### Dish

- id (PK)

- name, description, first_appeared, highest_price, etc.

- Represents a unique dish concept across menus.
