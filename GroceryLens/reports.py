#Reports

#Imports
import pandas as pd
import calendar

#Functions
def view_items(data_list):
    if len(data_list) == 0:
         print("There is no data to display (data is empty)")
         return
    grocery_dataframe = pd.DataFrame(data_list)
    print(grocery_dataframe.to_string(index=False))

def generate_report(df, budget):
    if df.empty:
        print("No purchases available.")
        return None

    df = df.copy()
    #Convert Dates
    df["Date"] = pd.to_datetime(df["Date"])

    #Calculate Each record's spend (Total amount)
    df["Spend"] = df["Price"] * df["Quantity"]

    #Date Filters
    today = pd.Timestamp.today()
    month_name = calendar.month_name[today.month]
    year = today.year

    #Current Month
    current_month_df = df[(
    df["Date"].dt.year == today.year) & 
    (df["Date"].dt.month == today.month)]

    #Last Month
    if today.month == 1:
        last_month = 12
        last_year = today.year - 1
    else:
        last_month = today.month - 1
        last_year = today.year

    last_month_df = df[(
    df["Date"].dt.year == last_year) &
    (df["Date"].dt.month == last_month)]

    #Current Week
    current_week = today.isocalendar().week
    current_year = today.isocalendar().year

    current_week_df = df[(
    df["Date"].dt.isocalendar().week == current_week)&
    (df["Date"].dt.isocalendar().year == current_year)]
            
    #Last Week 
    last_week_date = today - pd.Timedelta(days=7)

    last_week = last_week_date.isocalendar().week
    last_week_year = last_week_date.isocalendar().year

    last_week_df = df[(
    df["Date"].dt.isocalendar().week == last_week)&
    (df["Date"].dt.isocalendar().year == last_week_year)]

    #CORE METRICS
    total_spend = df["Spend"].sum()

    current_month_spend = current_month_df["Spend"].sum()
    last_month_spend = last_month_df["Spend"].sum()
    current_week_spend = current_week_df["Spend"].sum()
    last_week_spend = last_week_df["Spend"].sum()

    #Budget
    if budget > 0:
        budget_remaining = budget - current_month_spend
        budget_used_pcnt = (current_month_spend / budget) * 100
    else:
        budget_remaining = None
        budget_used_pcnt = None

    if budget > 0:
        if budget_used_pcnt >= 100:
            budget_status = "Over Budget"
        elif budget_used_pcnt >= 80:
            budget_status = "High Usage"
        elif budget_used_pcnt >= 50:
            budget_status = "Moderate Usage"
        else:
            budget_status = "Low Usage"
    else:
        budget_status = "No Budget Set"

    #Monthly % Change
    if last_month_spend > 0:
        month_change_pcnt = ((current_month_spend - last_month_spend) / last_month_spend) * 100
    else:
        month_change_pcnt = 0
    
    #Spend Projection
    days_passed = today.day
    days_in_month = calendar.monthrange(today.year, today.month)[1]

    #Calculate avg daily spend and projected month spend
    if days_passed > 0:
        average_daily_spend = current_month_spend / days_passed
        projected_month_spend = average_daily_spend * days_in_month
    else:
        average_daily_spend = 0
        projected_month_spend = 0

    #Compare to budget
    if budget > 0:
        projected_budget_difference = budget - projected_month_spend
    else:
        projected_budget_difference = None

    #Spend Projection Status
    if budget > 0:
        projected_budget_usage = (projected_month_spend / budget) * 100

        if projected_month_spend > budget:
            spend_projection_status = "Projected to exceed budget"
        else:
            spend_projection_status = "Projected to remain within budget"
    else:
        projected_budget_usage = None
        spend_projection_status = "No budget set"

    #Context is Current Month / Monthly
    #Top Category / Store & Spend
    category_spend = current_month_df.groupby("Category")["Spend"].sum()
    store_spend = current_month_df.groupby("Store")["Spend"].sum()

    top_category = category_spend.idxmax() if not category_spend.empty else None
    top_store = store_spend.idxmax() if not store_spend.empty else None
    
    #Spend Concentration 
    top_category_share = 0
    top_store_share = 0

    if current_month_spend > 0 and not category_spend.empty:
        top_category_share = (category_spend.max() / current_month_spend) * 100

    if current_month_spend > 0 and not store_spend.empty:
        top_store_share = (store_spend.max() / current_month_spend) * 100

    #Month Velocity (For Spend)
    month_spend_difference = current_month_spend - last_month_spend

    if last_month_spend > 0:
        month_velocity_pcnt = (month_spend_difference / last_month_spend) * 100
    else:
        month_velocity_pcnt = 0

    #Text Insight (simple rules)
    if month_velocity_pcnt > 15:
        month_velocity_insight = "Spending is accelerating strongly"
    elif month_velocity_pcnt > 5:
        month_velocity_insight = "Spending is increasing moderately"
    elif month_velocity_pcnt < -10:
        month_velocity_insight = "Spending is declining"
    else:
        month_velocity_insight = "Spending is stable"

    #Final Report
    return {
        #Core Month Report
        "current_month_spend": current_month_spend,
        "last_month_spend": last_month_spend,
        "month_change_pcnt": month_change_pcnt,
        "month_velocity_pcnt": month_velocity_pcnt,
        "month_velocity_insight": month_velocity_insight,

        #Week Context
        "current_week_spend": current_week_spend,
        "last_week_spend": last_week_spend,

        #Current Month Category / Store breakdown
        "category_spend": category_spend.to_dict(),
        "store_spend": store_spend.to_dict(),

        #Month & Year
        "month_name": month_name,
        "year": year,

        #Budget
        "budget": budget,
        "budget_remaining": budget_remaining,
        "budget_used_pcnt": budget_used_pcnt,
        "budget_status": budget_status,

        #Spend Projection
        "average_daily_spend": average_daily_spend,
        "projected_month_spend": projected_month_spend,
        "projected_budget_difference": projected_budget_difference,
        "projected_budget_usage": projected_budget_usage,
        "projection_status": spend_projection_status,

        #Lifetime Context
        "total_spend": total_spend,

        #Highlights
        "top_category": top_category,
        "top_store": top_store,
        "top_category_share": top_category_share,
        "top_store_share": top_store_share
 }

def display_report(report):
    print("\n" + "="*40)
    print(f"GROCERYLENS REPORT — {report['month_name']} {report['year']}")
    print("-"*40)

    print("\nSPENDING OVERVIEW")
    print(f"Lifetime Spend:     R{report['total_spend']:,.2f}")
    print(f"This Month:         R{report['current_month_spend']:,.2f}")
    print(f"Last Month:         R{report['last_month_spend']:,.2f}")
    print(f"Trend:              {report['month_velocity_insight']} ({report['month_velocity_pcnt']:.1f}%)")

    print("\nBUDGET OVERVIEW")
    if report["budget"] > 0:
        print(f"Monthly Budget: R{report['budget']:,.2f}")
        print(f"Spent:          R{report['current_month_spend']:,.2f}")
        print(f"Remaining:      R{report['budget_remaining']:,.2f}")
        print(f"Status:         {report['budget_status']}")

        #Usage % clamping
        usage = min(max(report["budget_used_pcnt"], 0), 100)
        print(f"Usage:          {usage:.1f}%")

    else:
        print("Monthly Budget:      Not set")

    print("\nMONTH END SPEND PROJECTION")
    print(f"Average Daily Spend:     R{report['average_daily_spend']:,.2f}")
    print(f"Projected Month Spend:   R{report['projected_month_spend']:,.2f}")

    if report["projected_budget_difference"] is not None:
        difference = report["projected_budget_difference"]

        if difference >= 0:
            print(f"Projected Remaining:     R{difference:,.2f}")
        else:
            print(f"Projected Overspend:    R{abs(difference):,.2f}")

    if report["projected_budget_usage"] is not None:
        print(f"Projected Budget Usage:  {report['projected_budget_usage']:.1f}%")

    print(f"Status:                  {report['projection_status']}")

    print("\nWEEKLY VIEW")
    print(f"This Week:      R{report['current_week_spend']:,.2f}")
    print(f"Last Week:      R{report['last_week_spend']:,.2f}")

    print("\nCATEGORY - SPEND BREAKDOWN (This Month)")
    for category, spend in report["category_spend"].items():
        print(f"-> {category:<10} R{spend:,.2f}")

    print("\nSTORE - SPEND BREAKDOWN (This Month)")
    for store, spend in report["store_spend"].items():
        print(f"-> {store:<10} R{spend:,.2f}")

    print("\nKEY DRIVERS & CONCENTRATION")
    print(f"Top Category:       {report['top_category']} ({report['top_category_share']:.1f}%)")
    print(f"Top Store:          {report['top_store']} ({report['top_store_share']:.1f}%)")

    print("="*40 + "\n")
