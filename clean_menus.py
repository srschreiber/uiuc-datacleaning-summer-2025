import csv
from collections import defaultdict
import numpy as np
from sklearn.cluster import DBSCAN
from src.lib.openai_client import LLMCleaner

from sklearn.metrics.pairwise import cosine_distances
from collections import defaultdict
from sklearn.cluster import DBSCAN
from src.lib.openai_client import LLMCleaner # or your actual path
from tqdm import tqdm
import os
from typing import List
import pickle
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors

import numpy as np
import faiss
from collections import defaultdict
from tqdm import tqdm
import os
import pickle
from typing import List
from src.lib.openai_client import LLMCleaner
import re

def embed_dishes_in_batches(cleaner: LLMCleaner, dishes: List[str], batch_size=1000) -> List[List[float]]:
    all_embeddings = []

    def normalize_dish_name(name: str) -> str:
        if not name:
            return ""
        name = name.lower().strip()
        name = re.sub(r'[^a-z0-9\s]', '', name)
        name = re.sub(r'\s+', ' ', name)
        return name

    dishes = list(map(normalize_dish_name, dishes))
    for i in tqdm(range(0, len(dishes), batch_size), desc="Embedding batches"):
        batch = dishes[i:i + batch_size]
        response = cleaner.embed_dishes(batch)
        all_embeddings.extend(item.embedding for item in response.entities)

    return all_embeddings

def cluster(dishes: List[str], eps: float = 0.1) -> List[str]:
    embedding_cache_path = "cleaned_data/cleaned_dish_embeddings.pkl"
    name_cache_path = "cleaned_data/cleaned_dish_names.pkl"

    if os.path.exists(name_cache_path):
        with open(name_cache_path, "rb") as f:
            return pickle.load(f)

    if os.path.exists(embedding_cache_path):
        with open(embedding_cache_path, "rb") as f:
            embeddings_list = pickle.load(f)
    else:
        print("Precomputed embeddings not found, computing embeddings...")
        cleaner = LLMCleaner()
        embedded = embed_dishes_in_batches(cleaner, dishes)
        embeddings_list = [embedding for embedding in embedded]
        os.makedirs("cleaned_data", exist_ok=True)
        pickle.dump(embeddings_list, open(embedding_cache_path, "wb"))

    print("Normalizing embeddings for cosine similarity...")
    X = np.array(embeddings_list).astype(np.float32)
    faiss.normalize_L2(X)

    print("Building FAISS index...")
    index = faiss.IndexFlatIP(X.shape[1])
    index.add(X)

    k = 128  # Number of neighbors to search
    print("Searching for neighbors...")
    D, I = index.search(X, k)

    threshold = 1.0 - eps
    parent = list(range(len(X)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        root_x = find(x)
        root_y = find(y)
        if root_x != root_y:
            parent[root_y] = root_x

    for i in range(len(X)):
        for j_idx, sim in zip(I[i], D[i]):
            if i != j_idx and sim >= threshold:
                union(i, j_idx)

    root_to_label = {}
    labels = []
    label_count = 0
    for i in range(len(X)):
        root = find(i)
        if root not in root_to_label:
            root_to_label[root] = label_count
            label_count += 1
        labels.append(root_to_label[root])

    cluster_to_names = defaultdict(list)
    for dish, label in zip(dishes, labels):
        cluster_to_names[label].append(dish)

    cluster_to_canonical = {
        label: min(group, key=len) for label, group in cluster_to_names.items()
    }

    out = [cluster_to_canonical[label] for label in labels]

    pickle.dump(out, open(name_cache_path, "wb"))
    return out


def run():
    """
    This function will read the dish csv, clean the dish names, group by dish name, and
    merge the records (keeping one of the ids) and summing menu appeared times, maxing highest price,
    minning lowest price, and keeping the first and last appeared dates.
    """

    # id,name,menus_appeared,times_appeared,first_appeared,last_appeared,lowest_price,highest_price
    fpath_dish = "/Users/samschreiber/Downloads/cleaned_data/Dish.csv"

    # id,menu_page_id,price,high_price,dish_id,created_at,updated_at,xpos,ypos
    fpath_menu_item = "/Users/samschreiber/Downloads/cleaned_data/MenuItem.csv"
    
    all_dishes = []
    all_menu_items = []

    with open(fpath_dish, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            all_dishes.append(row)
    
    with open(fpath_menu_item, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            all_menu_items.append(row)
    
    dish_names = [dish["name"] for dish in all_dishes]
    cleaned_dish_names = cluster(dish_names, eps=0.10)

    grouped_by_name = defaultdict(list)
    for dish, cleaned_name in zip(all_dishes, cleaned_dish_names):
        grouped_by_name[cleaned_name].append(dish)
    
    # Now we will merge the records
    merged_dishes = []
    dish_id_mappings = {}
    for cleaned_name, dishes in grouped_by_name.items():
        first_dish = dishes[0]

        # Make sure we can resolve old dish ids to new dish ids
        for dish in dishes:
            dish_id_mappings[dish["id"]] = first_dish["id"]
            try:
                dish["menus_appeared"] = float(dish["menus_appeared"])
            except:
                dish["menus_appeared"] = None
            try:
                dish["times_appeared"] = float(dish["times_appeared"])
            except:
                dish["times_appeared"] = None
            try:
                dish["lowest_price"] = float(dish["lowest_price"]) if dish["lowest_price"] else None
            except:
                dish["lowest_price"] = None
            try:
                dish["highest_price"] = float(dish["highest_price"]) if dish["highest_price"] else None
            except:
                dish["highest_price"] = None
            try:
                dish["first_appeared"] = float(dish["first_appeared"]) if dish["first_appeared"] else None
            except:
                dish["first_appeared"] = None
            try:
                dish["last_appeared"] = float(dish["last_appeared"]) if dish["last_appeared"] else None
            except:
                dish["last_appeared"] = None


        if len(dishes) == 1:
            merged_dishes.append(first_dish)
            continue

        merged_dish = {
            "id": first_dish["id"],
            "name": cleaned_name,
            "menus_appeared": sum(int(float(dish["menus_appeared"] or 0)) for dish in dishes),
            "times_appeared": sum(int(float(dish["times_appeared"] or 0)) for dish in dishes),
            "first_appeared": min(int(float(dish["first_appeared"] or 9999)) for dish in dishes),
            "last_appeared": max(int(float(dish["last_appeared"] or 0)) for dish in dishes),
            "lowest_price": min(float(dish["lowest_price"] or 9999) for dish in dishes),
            "highest_price": max(float(dish["highest_price"] or 0) for dish in dishes)
        }
        merged_dishes.append(merged_dish)
    
    cleaned_menu_items = []
    # Now read in the menu items and overwrite the dish ids to match the new merged dishes
    for menu_item in all_menu_items:
        old_dish_id = str(int(float(menu_item["dish_id"])))
        if old_dish_id in dish_id_mappings:
            menu_item["dish_id"] = dish_id_mappings[old_dish_id]
        cleaned_menu_items.append(menu_item)
    
    # Write the cleaned dishes to a new file
    with open("cleaned_data/cleaned_dish.csv", "w", newline='') as f:
        fieldnames = merged_dishes[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for dish in merged_dishes:
            writer.writerow(dish)

    # Write the cleaned menu items to a new file
    with open("cleaned_data/cleaned_menu_item.csv", "w", newline='') as f:
        fieldnames = cleaned_menu_items[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for menu_item in cleaned_menu_items:
            writer.writerow(menu_item)

def compare_old_and_new_dishes():
    """
    This function will randomly select 10 menu item ids. It will then join the new menu items with new dishes,
    and the old menu items with old dishes. It will then compare the dish names and prices and display the differences.
    """
    new_fpath_dish = "cleaned_data/Dish.csv"
    new_fpath_menu_item = "cleaned_data/MenuItem.csv"
    old_fpath_dish = "/Users/samschreiber/Downloads/cleaned_data/Dish.csv"
    old_fpath_menu_item = "/Users/samschreiber/Downloads/cleaned_data/MenuItem.csv"

    # select 10 rows between 1 and # rows(old_fpath_menu_item)
    with open(old_fpath_menu_item, "r") as f:
        reader = csv.DictReader(f)
        old_menu_items = list(reader)

    with open(new_fpath_menu_item, "r") as f:
        reader = csv.DictReader(f)
        new_menu_items = list(reader)
    
    sampled = np.random.choice(len(old_menu_items), size=10, replace=False)

    new_sampled = [new_menu_items[i] for i in sampled]
    old_sampled = [old_menu_items[i] for i in sampled]

    # index the new and old dishes by dish id
    new_dishes = {}
    with open(new_fpath_dish, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            new_dishes[int(float(row["id"]))] = row

    old_dishes = {}
    with open(old_fpath_dish, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            old_dishes[int(float(row["id"]))] = row

    for new_item, old_item in zip(new_sampled, old_sampled):
        new_dish = new_dishes[int(float(new_item["dish_id"]))] if int(float(new_item["dish_id"])) in new_dishes else None
        old_dish = old_dishes[int(float(old_item["dish_id"]))] if int(float(old_item["dish_id"])) in old_dishes else None
        print(f"New Item: {new_item['id']}, Dish: {new_dish['name'] if new_dish else 'N/A'}")
        print(f"Old Item: {old_item['id']}, Dish: {old_dish['name'] if old_dish else 'N/A'}")
        print("-" * 40)

if __name__ == "__main__":
    # Example usage of LLMCleaner
    # cleaner = LLMCleaner()
    # orig = ["Baked Mac n Cheese", "eggs", "soup", "egg soup", "bagels with cream cheese", "toast with cream cheese", "Macaroni and Cheese"]
    # cleaned: list[str] = cleaner.run(
    #     orig
    # )

    # dish_index = {dish: i for i, dish in enumerate(cleaned)}



    # print(dish_index)
    # run()
    compare_old_and_new_dishes()