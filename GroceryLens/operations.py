#Operations 

#Imports
from storage import load_grocery_data, save_grocery_data, load_budget_data, save_budget_data
from validation import get_valid_num, get_non_empty_str
from constants import categories, stores

from datetime import date

#Functions
def add_purchase():
    grocery_list = load_grocery_data()

    #Item
    item_name = get_non_empty_str("Enter item name: ")
    item_price = get_valid_num("Enter item Price: ",float,1.00,1000.00)
    item_quantity = get_valid_num("Enter item Quantity: ",int,1,100)

    #Item Category
    print("Categories:\n")
    for i in range(len(categories)): 
        print(f"{i+1}.{categories[i]}")
        
    category_input = get_valid_num("Select item Category: ",int,1,len(categories))
    item_category = categories[category_input-1]

    #Item Store
    print("Stores:\n")
    for i in range(len(stores)):
        print(f"{i+1}.{stores[i]}")

    store_input = get_valid_num("Select item Store: ",int,1,len(stores))
    item_store = stores[store_input-1]

            #Append and add item
    grocery_item = {"Item Name":item_name,
                    "Price":item_price,
                    "Quantity":item_quantity,
                    "Date":date.today().isoformat(),
                    "Category":item_category,
                    "Store":item_store}
            
    grocery_list.append(grocery_item)
    #Save item data   
    save_grocery_data(grocery_list)
    print("Purchase saved successfully!")


def set_monthly_budget():
    budget_data = load_budget_data()

    budget = get_valid_num("Enter monthly budget: R", float, 1, 100000)

    budget_data["monthly_budget"] = budget

    save_budget_data(budget_data)

    print(f"Budget set to R{budget:,.2f}")

def get_budget():
    budget_data = load_budget_data()

    if budget_data["monthly_budget"] is None:
        return 0
    return budget_data["monthly_budget"]
