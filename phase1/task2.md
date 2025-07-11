# Task 2: Develop Three Use Cases
- Write three use case descriptions, one paragraph each:
  - **U1 (Main Use Case):** Data cleaning is necessary and sufficient.
  - **U0 (Zero Cleaning Use Case):** Dataset is already good enough.
  - **U2 (Never Enough Use Case):** No amount of cleaning will make the data suitable.
- For U1, define 1–3 sample queries (or analysis goals) that demonstrate why cleaning is needed.
- Clearly justify why D does or doesn’t support each use case without cleaning.


## U1 (Main Use Case):
We will measure the most popular dishes by for each decade that data is collected in the NYPL library.
We will answer questions like:
- What are the items that have the most longevity and staying power on menus throughout the ages
- What items were popular only for a short while before more or less disappearing from menus
Cleaning is necessary for this as the dishes table is extremely dirty.
Dish names are repeated in many different forms with Coffee itself appearing in 600+ different dish types.

## U0 (Zero Cleaning Use Case):
How has the size of menus changed over the decades.
Are menus growing larger or smaller or are their sizes remaining stable?
We can answer these queries by checking the mean, median, and mode of the number of items on a menu through the years.
This requires no cleaning of the data since menu and menu items are cleanly linked in the dataset.

## U2 (Never Enough Use Case):
Any sort of data analysis that requires geography to be taken into account.
For e.g.:
- Are menus in certain parts of the world larger than others?
- How has the median price of an item changed in different parts of the world (or even the US itself)

The reason none of these questions can be answered reliably is because the "Place" column in the Menu table is filled with all kinds of inconsistent data.
Some times it refers to the city and state. Other times it refers to a ship or cruise.
Yet other times, it is left blank.
No amount of data wrangling and cleaning will allow us to derive useful results from the dataset for this usecase.

