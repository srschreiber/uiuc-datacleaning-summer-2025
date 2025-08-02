# Description of Data Cleaning Performed

## Dish and MenuItem Cleaning

We cleaned the dish names by identifying dishes that referred to the same item but had different names. For example, "Lamb kidneys with bacon, broiled" and "Lamb kidneys with bacon, broiled" were identified as refering to the same item. To do this, we:

1. Compute the vector embeddings using the `text-embedding-3-small` model for ~400,000 dish names.
2. Use FAISS to index the embeddings and perform similarity search to find K similar dishes.
3. Use union find to traverse neighborhoods of K similar dishes and merge if they are similar enough (95% cosine similarity).
4. Merge the dish names and pick its canonical name, the shortest representation of the dish name. Merge the columns: `menus_appeared, times_appeared, first_appeared,last_appeared, lowest_price, highest_price` by taking the sum, or min/max as appropriate.
5. Replace the MenuItem's dish ids with the new dish ids generated from the union find.

## Rational for Cleaning with Respect to U1

The use-case that this cleaning is intended to support is: "Measure the most popular dishes by for each decade that data is collected in the NYPL library"

This cleaning is necessary because many dishes may be incorrectly divided into multiple records due to various naming conventions or languages. This warps the `menus_appeared, times_appeared, first_appeared, last_appeared, lowest_price, and highest_price columns`, leading to inaccurate analysis of dish popularity over time. By standardizing dish names and merging similar records, we ensure that the data more accurately aggregates the dish appearances and prices, allowing for a clearer understanding of dish popularity trends. Embeddings were used over a simple edit distance approach because some dishes may have a relatively high edit distance while still being semantically similar. Furthermore, edit distance is not robust to language differences or naming conventions.

# Data Quality Changes

## Overall Record Changes

| Table       | # Records Modified |  % Modified | # Records Before | # Records After | % Changed |
|-------------|-------------------|------------------|-----------------|-------|--------------|
| Dish        | 93729  | 22.2%            | 422005              | 328276            | - 22.2% | 
| MenuItem    | 301945              | 23.1%              | 1307175            | 1307175            | 0% |

This indicates that 22.2% of Dishes were identified as duplicates and were consolidated into a single record. After cleaning the Dish table, 23% of MenuItems were updated to reflect the new Dish IDs, indicating that many MenuItems needed to be adjusted to point to the newly consolidated Dish records.

## Spot Checking a few Values
------------------------------------------
For Menu Item ID: 1383928
New Dish ID: 53126, Dish: Little Neck Clam Cream Stew
Old Dish ID: 511857.0, Dish: little neck clams stew with cream
----------------------------------------
For Menu Item ID: 1385314
New Dish ID: 4432, Dish: Hennessy Brandy
Old Dish ID: 437861.0, Dish: * * * Hennessy Brandy
----------------------------------------
For Menu Item ID: 1385710
New Dish ID: 241234, Dish: Tossed Salad with Thousand Island Dressing
Old Dish ID: 515515.0, Dish: Tossed salad greens with Thousand Island dressing
----------------------------------------
For Menu Item ID: 1385502
New Dish ID: 3098, Dish: Lamb kidneys broiled with bacon
Old Dish ID: 481194.0, Dish: Lamb kidneys with bacon, broiled
----------------------------------------
For Menu Item ID: 1385170
New Dish ID: 409234, Dish: Alaska Red Salmon Salad, Potato Salad, Tomato Slices
Old Dish ID: 514387.0, Dish: Alaska Red Salmon, Lemon Slice, Potato Salad, Tomato Slices, Lettuce
----------------------------------------
For Menu Item ID: 1385684
New Dish ID: 431200, Dish: Span Backwerk
Old Dish ID: 515491.0, Dish: Span. Backwerk.
----------------------------------------
For Menu Item ID: 1385691
New Dish ID: 6714, Dish: Eggs Shirred
Old Dish ID: 411239.0, Dish: Eggs, Shirred
For Menu Item ID: 1385694
New Dish ID: 2117, Dish: Minced ham, scrambled egg
Old Dish ID: 515500.0, Dish: Minced Ham, Scrambled with Eggs
----------------------------------------
For Menu Item ID: 1385442
New Dish ID: 2586, Dish: Delmonico Steak Mushrooms
Old Dish ID: 498696.0, Dish: Delmonico steak with mushroom ssauce
----------------------------------------
For Menu Item ID: 1384956
New Dish ID: 286007, Dish: Geflügelcrèmesuppe, Hamburger Zwiebelsteak mit Erbsen, Karotten und Kartoffelbrei
Old Dish ID: 479722.0, Dish: Geflügelcrèmesuppe, Hamburger Zwiebelsteak mit Erbsen, Karotten und Kartoffelbrei, Apfelschnitte
----------------------------------------

# Workflow Model

# Conclusion and Summary

## Lessons Learned

Certain data cleaning approaches can sound promising on small datasets but infeasible on larger datasets due to computational constraints or cost constraints. For example, I originally wanted to use a gpt model to normalize dish names to English without brand names or modifiers, but this was infeasible due to the high costs of using the model on such a large dataset. Instead, I realized generating embeddings was much cheaper and more efficient, allowing me to use FAISS to find similar dishes and merge them based on cosine similarity + Union Find.
