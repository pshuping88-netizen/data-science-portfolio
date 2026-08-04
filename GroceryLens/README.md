# GroceryLens - Grocery Budget & Analytics CLI

## Overview
GroceryLens is a Python command-line application for tracking grocery purchases and monthly budgets. It stores purchase data in JSON files and generates reports that summarize spending patterns, budget usage, category breakdowns, store breakdowns, and month-end projections.

The project demonstrates modular Python design, input validation, data persistence, and practical analytics with Pandas.

### Project Goal
GroceryLens was built to track grocery spending in a structured way and turn raw purchase data into practical reports. The goal was to create a modular Python application that combines data persistence, validation, and analytics to help users monitor budgets, compare spending patterns, and understand how their grocery habits change over time.

### Features
- Add and store grocery purchases
- Persistent JSON-based data storage
- Set and update a monthly budget
- View all recorded purchases
- Weekly, monthly, and lifetime spending metrics
- Category and store spending analysis
- Budget tracking and usage monitoring
- Month-end spending projection
- Spending velocity analysis
- Clean command-line interface
- Modular project structure

___
## Project Structure
```
GroceryLens/
│
├── main.py
├── menu.py
├── operations.py
├── reports.py
├── storage.py
├── validation.py
├── constants.py
│
├── data/
│   ├── grocery_data.json
│   └── grocery_budget.json
│
├── README.md
├── requirements.txt
└── .gitignore
```

### Module Overview

#### `main.py`
Application entry point. Starts the program and launches the main menu.

#### `menu.py`
Handles CLI navigation and user choices.

#### `operations.py`
Contains the main app actions such as adding purchases and setting the monthly budget.

#### `reports.py`
Generates and displays analytics reports and purchase views.

#### `storage.py`
Loads and saves grocery and budget data using JSON files.

#### `validation.py`
Handles input validation for text and numeric values.

#### `constants.py`
Stores reusable values such as grocery categories and stores.

___
## Technologies Used
- Python
- Pandas
- JSON
- Pathlib
- Datetime
- Calendar

___
## Analytics Included
GroceryLens reports include:
- Lifetime spend
- Current month spend
- Last month spend
- Weekly spend comparison
- Monthly budget usage
- Remaining budget
- Budget status
- Month-end spend projection
- Projected remaining budget or overspend
- Category spend breakdown
- Store spend breakdown
- Top spending category
- Top spending store
- Spending velocity trend

___
## Example Output
```
----- GROCERYLENS -----
1. Add Purchase
2. View Purchases
3. Generate Report
4. Set Monthly Budget
5. Exit GroceryLens
Enter Number: 3

========================================
GROCERYLENS REPORT — July 2026
----------------------------------------

SPENDING OVERVIEW
Lifetime Spend:     R3,943.70
This Month:         R891.15
Last Month:         R1,610.24
Trend:              Spending is declining (-44.7%)

BUDGET OVERVIEW
Monthly Budget: R1,700.00
Spent:          R891.15
Remaining:      R808.85
Status:         Moderate Usage
Usage:          52.4%

MONTH END SPEND PROJECTION
Average Daily Spend:     R34.28
Projected Month Spend:   R1,062.53
Projected Remaining:     R637.47
Projected Budget Usage:  62.5%
Status:                  Projected to remain within budget

WEEKLY VIEW
This Week:      R471.55
Last Week:      R0.00

CATEGORY - SPEND BREAKDOWN (This Month)
-> Drinks     R38.99
-> Produce    R200.34
-> Protein    R475.27
-> Snacks     R91.97
-> Staple     R84.58

STORE - SPEND BREAKDOWN (This Month)
-> Checkers   R284.59
-> Other      R20.00
-> PicknPay   R305.03
-> Spar       R281.53

KEY DRIVERS & CONCENTRATION
Top Category:       Protein (53.3%)
Top Store:          PicknPay (34.2%)
```

___
## How to Run 
Clone the repository:

```
git clone <repository-url>
```

Move into the project folder:

```
cd GroceryLens
```

Install dependencies:

```
pip install -r requirements.txt
```

Run the application:

```
python main.py
```

___
## Future Improvements
GroceryLens is actively being developed. 
Planned enhancements include:

### Next Milestones
- Grocery trip tracking to group purchases by shopping session
- Receipt scanning with OCR for faster purchase entry
- Automatic product categorization using text classification
- Price history tracking for recurring grocery items

### Planned Enhancements
- SQL database integration
- Historical report archiving
- Shopping behaviour metrics
- Better visual reporting
- Streamlit dashboard
- More advanced forecasting
