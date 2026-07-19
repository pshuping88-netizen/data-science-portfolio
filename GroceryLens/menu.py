#Menu

#Imports
from storage import load_grocery_data
from operations import add_purchase, set_monthly_budget, get_budget
from reports import view_items, generate_report, display_report
from validation import get_valid_num

import pandas as pd

#Functions
def main_menu():
    while True:
    #Display CLI menu
        print(f"----- GROCERYLENS -----\n1. Add Purchase\n2. View Purchases\n3. Generate Report\n4. Set Monthly Budget\n5. Exit GroceryLens")

    #User Choice
        user_choice = get_valid_num("Enter Number: ",int,1,5)

    #Match Case
        match user_choice:
            case 1: #Add Purchase
                add_purchase()
            case 2: #View items
                grocery_list = load_grocery_data()
                view_items(grocery_list)

            case 3: #Current State Report
                grocery_list = load_grocery_data()
                budget = get_budget()

                df = pd.DataFrame(grocery_list)

                report = generate_report(df, budget)
                if report is not None:
                    display_report(report)

            case 4: #Set Budget
                set_monthly_budget()

            case 5: #Exit Tracker
                print("Exiting GroceryLens!")
                break
            case _:
                print("Wrong Value entered")
                