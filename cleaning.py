import pandas as pd
import os
from datetime import datetime

RAW_FOLDER = 'raw_dataset'
CLEANED_FOLDER = 'cleaned_data'
LOG_PATH = 'cleaning_log.txt'
DATE_RANGE = (1800, 2025)

os.makedirs(CLEANED_FOLDER, exist_ok=True)

# Load datasets
menu = pd.read_csv(os.path.join(RAW_FOLDER, 'Menu.csv'))
menupage = pd.read_csv(os.path.join(RAW_FOLDER, 'MenuPage.csv'))
menuitem = pd.read_csv(os.path.join(RAW_FOLDER, 'MenuItem.csv'))
dish = pd.read_csv(os.path.join(RAW_FOLDER, 'Dish.csv'))

log = []

def log_change(task_name, column, num_violations_before, num_violations_after, cells_changed):
    log.append(f"[{task_name}] {column} — Violations Before: {num_violations_before}, After: {num_violations_after}, Cells Changed: {cells_changed}")

def fix_foreign_keys():
    task = "Foreign Key Violations"
    
    # MenuPage.menu_id must exist in Menu.id
    before = len(menupage)
    valid_menu_ids = set(menu['id'])
    menupage_clean = menupage[menupage['menu_id'].isin(valid_menu_ids)]
    after = len(menupage_clean)
    log_change(task, "MenuPage.menu_id", before - after, 0, before - after)

    # MenuItem.menu_page_id must exist in MenuPage.id
    before = len(menuitem)
    valid_page_ids = set(menupage_clean['id'])
    menuitem_clean = menuitem[menuitem['menu_page_id'].isin(valid_page_ids)]
    after = len(menuitem_clean)
    log_change(task, "MenuItem.menu_page_id", before - after, 0, before - after)

    # MenuItem.dish_id must exist in Dish.id
    before = len(menuitem_clean)
    valid_dish_ids = set(dish['id'])
    menuitem_clean = menuitem_clean[menuitem_clean['dish_id'].isin(valid_dish_ids)]
    after = len(menuitem_clean)
    log_change(task, "MenuItem.dish_id", before - after, 0, before - after)

    return menupage_clean, menuitem_clean

def drop_duplicates(df, name, subset=None):
    task = f"Duplicate Rows - {name}"
    before = len(df)
    df_clean = df.drop_duplicates(subset=subset)
    after = len(df_clean)
    log_change(task, "all columns", before - after, 0, before - after)
    return df_clean

def fix_page_numbers(menupage_df):
    task = "Page Number Validity"
    
    before_invalid = ((menupage_df['page_number'] < 1) | menupage_df['page_number'].isnull()).sum()
    changed = menupage_df['page_number'].apply(lambda x: 1 if pd.isnull(x) or x < 1 else x)
    cells_changed = (menupage_df['page_number'] != changed).sum()
    menupage_df['page_number'] = changed
    after_invalid = ((menupage_df['page_number'] < 1) | menupage_df['page_number'].isnull()).sum()
    
    log_change(task, "MenuPage.page_number", before_invalid, after_invalid, cells_changed)

    # Drop duplicate page_numbers within same menu
    before_dupes = menupage_df.duplicated(subset=['menu_id', 'page_number']).sum()
    menupage_df = menupage_df.drop_duplicates(subset=['menu_id', 'page_number'])
    log_change(task, "MenuPage.page_number (uniqueness)", before_dupes, 0, before_dupes)

    return menupage_df

def deduplicate_menuitems(menuitem_df):
    task = "MenuItem on Multiple Pages"
    
    before = len(menuitem_df)
    menuitem_df = menuitem_df.drop_duplicates(subset=['dish_id', 'menu_page_id'])
    after = len(menuitem_df)
    log_change(task, "MenuItem.dish_id & menu_page_id", before - after, 0, before - after)

    return menuitem_df

def remove_fully_null_columns(df_dict):
    task = "Remove 100% Null Columns"
    for name, df in df_dict.items():
        for col in df.columns:
            if df[col].isnull().all():
                df.drop(columns=[col], inplace=True)
                log_change(task, f"{name}.{col}", 1, 0, df.shape[0])
    return df_dict

def fix_primary_keys(df, key_name, table_name):
    task = f"Primary Key Issues - {table_name}"
    before_nulls = df[key_name].isnull().sum()
    df = df.dropna(subset=[key_name])
    
    before_dupes = df.duplicated(subset=[key_name]).sum()
    df = df.drop_duplicates(subset=[key_name])
    
    log_change(task, f"{key_name} (nulls)", before_nulls, 0, before_nulls)
    log_change(task, f"{key_name} (dupes)", before_dupes, 0, before_dupes)
    return df

def fix_dates(menu_df, dish_df, menuitem_df):
    task = "Date Fixes"
    
    def fix_year(y):
        try:
            y = int(y)
            if y > DATE_RANGE[1]:
                return DATE_RANGE[1]
            if y < DATE_RANGE[0]:
                return None
            return y
        except:
            return None

    # Menu.date
    before_null = menu_df['date'].isnull().sum()
    menu_df['date'] = pd.to_datetime(menu_df['date'], errors='coerce')
    menu_df = menu_df[(menu_df['date'].dt.year >= DATE_RANGE[0]) & (menu_df['date'].dt.year <= DATE_RANGE[1])]
    after_null = menu_df['date'].isnull().sum()
    log_change(task, "Menu.date", before_null, after_null, before_null - after_null)

    # Dish first_appeared and last_appeared
    for col in ['first_appeared', 'last_appeared']:
        before = dish_df[col].apply(lambda x: x > DATE_RANGE[1] if pd.notnull(x) else False).sum()
        dish_df[col] = dish_df[col].apply(lambda x: fix_year(x))
        log_change(task, f"Dish.{col}", before, 0, before)

    # Swap if first > last
    mask = (dish_df['first_appeared'] > dish_df['last_appeared'])
    cells_changed = mask.sum()
    dish_df.loc[mask, 'first_appeared'] = dish_df.loc[mask, 'last_appeared']
    log_change(task, "Dish.first_appeared > last_appeared", cells_changed, 0, cells_changed)

    # MenuItem created_at and updated_at
    menuitem_df['created_at'] = pd.to_datetime(menuitem_df['created_at'], errors='coerce')
    menuitem_df['updated_at'] = pd.to_datetime(menuitem_df['updated_at'], errors='coerce')
    mask = menuitem_df['created_at'] > menuitem_df['updated_at']
    cells_changed = mask.sum()
    menuitem_df.loc[mask, 'created_at'] = menuitem_df.loc[mask, 'updated_at']
    log_change(task, "MenuItem.created_at > updated_at", cells_changed, 0, cells_changed)

    return menu_df, dish_df, menuitem_df

def save_outputs(menu, menupage, menuitem, dish):
    menu.to_csv(os.path.join(CLEANED_FOLDER, 'Menu.csv'), index=False)
    menupage.to_csv(os.path.join(CLEANED_FOLDER, 'MenuPage.csv'), index=False)
    menuitem.to_csv(os.path.join(CLEANED_FOLDER, 'MenuItem.csv'), index=False)
    dish.to_csv(os.path.join(CLEANED_FOLDER, 'Dish.csv'), index=False)
    
    with open(LOG_PATH, 'w') as f:
        f.write("\n".join(log))

# Step-by-step cleaning
menupage, menuitem = fix_foreign_keys()
menupage = drop_duplicates(menupage, "MenuPage")
menuitem = drop_duplicates(menuitem, "MenuItem")
menupage = fix_page_numbers(menupage)
menuitem = deduplicate_menuitems(menuitem)

dataframes = remove_fully_null_columns({
    "Menu": menu,
    "MenuPage": menupage,
    "MenuItem": menuitem,
    "Dish": dish
})

menu = fix_primary_keys(dataframes["Menu"], "id", "Menu")
menupage = fix_primary_keys(dataframes["MenuPage"], "id", "MenuPage")
menuitem = fix_primary_keys(dataframes["MenuItem"], "id", "MenuItem")
dish = fix_primary_keys(dataframes["Dish"], "id", "Dish")

menu, dish, menuitem = fix_dates(menu, dish, menuitem)

# Save cleaned data and log
save_outputs(menu, menupage, menuitem, dish)
