#Storage

#Imports
from pathlib import Path
import json

#Load/Create Grocery & Budget Data
base_directory = Path(__file__).resolve().parent
grocery_path = base_directory / "data" / "grocery_data.json"
budget_path = base_directory / "data" / "grocery_budget.json"

#Functions
def load_grocery_data():
    try:
        with open(grocery_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    
def save_grocery_data(grocery_list):
    with open(grocery_path, "w") as file:
        json.dump(grocery_list, file, indent=4)

def load_budget_data():
    try:
        with open(budget_path,"r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"monthly_budget": None}

def save_budget_data(budget_data):
    with open(budget_path, "w") as file:
        json.dump(budget_data, file, indent=4)
