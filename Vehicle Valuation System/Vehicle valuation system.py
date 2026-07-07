#Vehicle Valuation System
#Import Modules
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

from sklearn.decomposition import PCA

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from sklearn.neighbors import KNeighborsRegressor

from sklearn.ensemble import RandomForestRegressor

#Exploratory Data Analysis

#Load Data
#Store data as dataframe from file
car_pricing_data = pd.read_csv("car_pricing_datasets.csv")

#Inspect Data
#Read and check data
print("Dataset Snippet:")
print(car_pricing_data.head())
print("\nMissing Values:")
print(car_pricing_data.isnull().sum())
print("\nDuplicate Records:")
print(car_pricing_data.duplicated().sum())

#Exploratory Data Analysis Visualization
#Graph 1 (Histogram): - Price Distribution
plt.figure(figsize=(10,6))
plt.hist(car_pricing_data["price"],bins=40)
plt.title("Price Distribution")
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.grid(True)
plt.show()

#Summary Statistics
price_median = car_pricing_data["price"].median()
price_mean = car_pricing_data["price"].mean()
price_max = car_pricing_data["price"].max()
price_min = car_pricing_data["price"].min()

print(f"Price Median: R{price_median:,.2f}\nPrice Mean: R{price_mean:,.2f}\nPrice Max: R{price_max:,.2f}\nPrice Min: R{price_min:,.2f}")

#Graph 2 (Scatter plot): - Price vs Horsepower
plt.figure(figsize=(10,6))
plt.scatter(car_pricing_data["price"],car_pricing_data["horsepower"])
plt.title("Price vs Horsepower")
plt.xlabel("Price")
plt.ylabel("Horsepower")
plt.grid(True)
plt.show()

#Graph 3 (Scatter plot): - Price vs Engine Size
plt.figure(figsize=(10,6))
plt.scatter(car_pricing_data["price"],car_pricing_data["enginesize"])
plt.title("Price vs Engine Size")
plt.xlabel("Price")
plt.ylabel("Engine Size")
plt.grid(True)
plt.show()

#Graph 4 (Scatter plot): - Price vs Curb Weight
plt.figure(figsize=(10,6))
plt.scatter(car_pricing_data["price"],car_pricing_data["curbweight"])
plt.title("Price vs Curb Weight")
plt.xlabel("Price")
plt.ylabel("Curb Weight")
plt.grid(True)
plt.show()

#Graph 5 (Bar Graph): - Category Relationship
avg_price_cylindernumber_data = car_pricing_data.groupby("cylindernumber")["price"].mean()#Group and store data in Series

plt.figure(figsize=(10,6))
plt.bar(avg_price_cylindernumber_data.index, avg_price_cylindernumber_data.values)
plt.title("Average Price by Cylinder Number")
plt.xlabel("Cylinder Number")
plt.ylabel("Average Price")
plt.grid(axis="y")
plt.show()

#Data Cleaning for Market Structure
#Lowering all column headings and dropping columns
car_pricing_data.columns = car_pricing_data.columns.str.lower()
car_pricing_data = car_pricing_data.drop("car_id", axis=1)

#Filter Numerical Columns
numerical_cols = ["price", "carlength","carheight", "carwidth",
                  "curbweight", "enginesize", "horsepower", 
                  "citympg", "highwaympg", "wheelbase", "symboling"]

#Filling Numerical Columns with Median
for column in numerical_cols:
    car_pricing_data[column] = car_pricing_data[column].fillna(car_pricing_data[column].median())

#Filter Categorical Columns
categorical_cols = ["carname", "carbody", "drivewheel", 
                    "fueltype", "aspiration", "enginelocation", 
                    "cylindernumber", "enginetype", "doornumber"]

#Filling Categorical Columns with Mode (index at 0)
for column in categorical_cols:
    car_pricing_data[column] = car_pricing_data[column].fillna(car_pricing_data[column].mode()[0])

#Standardisation
for column in categorical_cols:
    car_pricing_data[column] = car_pricing_data[column].astype(str).str.strip().str.lower()

#Check that missing values have been filled and that data types are expected
print(car_pricing_data.isnull().sum())
print(car_pricing_data.dtypes)

#Storing cleaned data as dataframe
selected_cols = numerical_cols + categorical_cols
prepared_analysis_dataset = car_pricing_data[selected_cols]

#Market Structure (Segmentation):

#Engine Performance Features
car_pricing_data["power_to_weight"] = car_pricing_data["horsepower"]/car_pricing_data["curbweight"]
car_pricing_data["fuel_efficiency"] = (car_pricing_data["citympg"] + car_pricing_data["highwaympg"]) / 2

#Vehicle Size Features 
car_pricing_data["vehicle_size"] = car_pricing_data["carlength"] * car_pricing_data["carwidth"] * car_pricing_data["carheight"]

#Market Position Features
car_pricing_data["brand"] = car_pricing_data["carname"].str.split().str[0]
brand_mean_price = car_pricing_data.groupby("brand")["price"].mean()
car_pricing_data["brand_value"] = car_pricing_data["brand"].map(brand_mean_price)

car_pricing_data["log_price"] = np.log(car_pricing_data["price"]) #Log to compress large price values

car_pricing_data["symboling"] = (car_pricing_data["symboling"] - car_pricing_data["symboling"].mean()) / car_pricing_data["symboling"].std() #Scaling

#Vehicle Design Features
car_pricing_data["doornumber"] = car_pricing_data["doornumber"].map({
    "one": 1, "two": 2,
    "three": 3, "four": 4,
    "five": 5, "six": 6,
    "seven": 7, "eight": 8,
    "nine": 9, "ten": 10 })

#Dummy Encoding (Catergorical Values)
car_pricing_data = pd.get_dummies(car_pricing_data, columns=["fueltype", "aspiration", "carbody", "drivewheel", "enginelocation"], drop_first=True)

#Dropping Variables For Cleaner Clustering 
clustering_data = car_pricing_data.drop(columns=["carname", "price","curbweight", "enginetype",
                                                    "cylindernumber", "fuelsystem", "brand", "horsepower",
                                                    "citympg", "highwaympg", "doornumber", "wheelbase",
                                                    "carwidth", "carlength", "carheight", "boreratio",
                                                    "stroke", "compressionratio", "peakrpm", "brand_value"]) #Removed brand_value after careful consideration

#Controlled Scaling so that variable dimensions are equal
scaler = StandardScaler()
scaled_clustering_data = pd.DataFrame(scaler.fit_transform(clustering_data), columns=clustering_data.columns)

#Use K Means to Cluster Data (Unsupervised Model)
kmeans = KMeans(n_clusters = 3, random_state = 42, n_init = 10)
car_pricing_data["cluster"] = kmeans.fit_predict(scaled_clustering_data)

#Checking Model Output
print(car_pricing_data["cluster"].value_counts())

#Cluster Profiling
print("Cluster 0")
print(car_pricing_data[car_pricing_data["cluster"] == 0].head(10))
print("Cluster 1")
print(car_pricing_data[car_pricing_data["cluster"] == 1].head(10))
print("Cluster2")
print(car_pricing_data[car_pricing_data["cluster"] == 2].head(10))

#Cluster Summaries
cluster_summaries = car_pricing_data.groupby("cluster").mean(numeric_only=True)
print("Cluster Summaries")
print(cluster_summaries)

#Visualizing the clusters (Not accurate)
plt.figure(figsize=(10,6))
scatter = plt.scatter(car_pricing_data["power_to_weight"], car_pricing_data["vehicle_size"], c=car_pricing_data["cluster"], cmap="tab10", alpha=0.9)
plt.title("Cluster Segments")
plt.xlabel("Power to Weight")
plt.ylabel("Vehicle Size")

handles, labels = scatter.legend_elements()
plt.legend(handles, labels, title="Cluster")

plt.grid(True)
plt.show()

#Visualizing the clusters using PCA
pca  = PCA(n_components = 2, random_state=42)
X_pca = pca.fit_transform(scaled_clustering_data)

pca_df = pd.DataFrame(X_pca, columns=["PC1", "PC2"])
pca_df["cluster"] = car_pricing_data["cluster"]

plt.figure(figsize=(10,6))
scatter = plt.scatter(pca_df["PC1"], pca_df["PC2"], c=pca_df["cluster"], cmap="tab10", alpha=0.9)
plt.title("Vehicle Clusters in PCA space")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.grid(True)
handles, labels = scatter.legend_elements()
plt.legend(handles, labels, title="Cluster")
plt.show()

#Get Price Quantiles
log_price_q1= car_pricing_data["log_price"].quantile(0.25)
log_price_q2= car_pricing_data["log_price"].quantile(0.50)
log_price_q3= car_pricing_data["log_price"].quantile(0.75)

#Functions
def price_band(x):
    if x <= log_price_q1:
        return "automatic valuation"
    elif x <= log_price_q2:
        return "manual review"
    elif x <= log_price_q3:
        return "high value review"
    else:
        return "premium valuation"
    
def risk_band(x):
    if x > 1:
        return "high risk review"
    elif x < -1:
        return "low risk"
    else:
        return "standard risk"
    
def performance_band(x):
    if x > car_pricing_data["power_to_weight"].quantile(0.75):
        return "performance vehicle"
    else:
        return "standard vehicle"

#Apply Business Rules
def business_category(row):
    if row["price_band"] == "automatic valuation" and row["risk_band"] != "high risk review" and row["performance_band"] == "standard vehicle":
        return "auto approve"

    elif row["risk_band"] == "high risk review":
        return "manual - high risk review"

    elif row["price_band"] == "premium valuation" or row["performance_band"] == "performance vehicle":
        return "manual - high value review"

    else:
        return "standard manual review"

#Apply Functions
car_pricing_data["price_band"] = car_pricing_data["log_price"].apply(price_band)
car_pricing_data["risk_band"] = car_pricing_data["symboling"].apply(risk_band)
car_pricing_data["performance_band"] = car_pricing_data["power_to_weight"].apply(performance_band)

#Applying Business Rule Function
car_pricing_data["business_category"] = car_pricing_data.apply(business_category, axis=1)

#Baseline Model (Linear Regression)
X = scaled_clustering_data.drop(columns=["log_price"]) #Data
y = car_pricing_data["log_price"] #Target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size= 0.20, random_state= 42 )

linear_model = LinearRegression()
linear_model.fit(X_train, y_train)

linear_y_pred = linear_model.predict(X_test)

#Evaluate Model Performance

#Convert log price back to price
linear_price_pred = np.exp(linear_y_pred)
actual_price = np.exp(y_test)

rmse_linear = np.sqrt(mean_squared_error(actual_price, linear_price_pred))
mae_linear = mean_absolute_error(actual_price, linear_price_pred)
r2_linear = r2_score(actual_price, linear_price_pred)

print(f"Linear Regression RMSE: R{rmse_linear:,.2f}")
print(f"Linear Regression MAE: R{mae_linear:,.2f}")
print(f"Linear Regression R2: {r2_linear:,.2f}")

#Modelling Approach 2 (K Nearest Neighbour)
#(Model uses same data as Linear)
knn_model = KNeighborsRegressor(n_neighbors=5)
knn_model.fit(X_train, y_train)

knn_y_pred = knn_model.predict(X_test)

#Evaluate Model Performance

#Convert log price back to price
knn_price_pred = np.exp(knn_y_pred)

rmse_knn = np.sqrt(mean_squared_error(actual_price, knn_price_pred))
mae_knn = mean_absolute_error(actual_price, knn_price_pred)
r2_knn = r2_score(actual_price, knn_price_pred)

print(f"K-Nearest Neighbour RMSE: R{rmse_knn:,.2f}")
print(f"K-Nearest Neighbour MAE: R{mae_knn:,.2f}")
print(f"K-Nearest Neighbour R2: {r2_knn:,.2f}")

#Modelling Approach 3 (Random Forest) - Final Model
random_forest_model = RandomForestRegressor(n_estimators= 100, random_state= 42)
random_forest_model.fit(X_train, y_train)

rf_y_pred = random_forest_model.predict(X_test)

#Evaluate Model Performance

#Convert log price back to price
rf_price_pred = np.exp(rf_y_pred)

rmse_rf = np.sqrt(mean_squared_error(actual_price, rf_price_pred))
mae_rf = mean_absolute_error(actual_price, rf_price_pred)
r2_rf = r2_score(actual_price, rf_price_pred)

print(f"Random Forest RMSE: R{rmse_rf:,.2f}")
print(f"Random Forest MAE: R{mae_rf:,.2f}")
print(f"Random Forest R2: {r2_rf:,.2f}")

#Check Feature Importance
importance_df = pd.DataFrame({
    "feature": X.columns,
    "importance": random_forest_model.feature_importances_
}).sort_values("importance", ascending=False)

print(importance_df.head(10))

#Error Analysis
rf_results = pd.DataFrame({
    "actual_price": actual_price,
    "predicted_price": rf_price_pred})

rf_results["error"] = rf_results["actual_price"] - rf_results["predicted_price"]
rf_results["abs_error"] = abs(rf_results["error"])

#Actual vs Predicted Scatter
plt.figure(figsize=(10,6))
plt.scatter(rf_results["actual_price"],
            rf_results["predicted_price"])

plt.plot(
    [rf_results["actual_price"].min(), rf_results["actual_price"].max()],
    [rf_results["actual_price"].min(), rf_results["actual_price"].max()],
    "r--")

plt.title("Actual vs Predicted Prices")
plt.xlabel("Actual Price")
plt.ylabel("Predicted Price")
plt.grid(True)
plt.show()

#Error vs Price Scatter
plt.figure(figsize=(10,6))
plt.scatter(rf_results["actual_price"],
            rf_results["abs_error"])

plt.title("Absolute Error vs Actual Price")
plt.xlabel("Actual Price")
plt.ylabel("Absolute Error")
plt.grid(True)
plt.show()

#Quartile MAE analysis
rf_results["price_group"] = pd.qcut(
    rf_results["actual_price"],
    q=4,
    labels=["Q1 Cheapest","Q2","Q3","Q4 Most Expensive"])

quartile_mae = rf_results.groupby("price_group")["abs_error"].mean()
print(quartile_mae)

print(rf_results.sort_values("abs_error",ascending=False).head(10))

#Valuation Function (Random Forest)
def vehicle_valuation(vehicle_features):
    predicted_log_price = random_forest_model.predict(vehicle_features)
    predicted_price = np.exp(predicted_log_price)[0]

    return predicted_price

vehicle_price = vehicle_valuation(X_test.iloc[[3]])

print(f"Estimated Market Value: R{vehicle_price:,.2f}")
