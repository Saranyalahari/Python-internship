import pandas as pd

# 1. Load Dataset

file_path = "laptopData.csv"   # Ensure this file exists in same folder
df = pd.read_csv(file_path)

print("Dataset Loaded Successfully\n")

# 2. Explore Dataset

print("First 5 Rows:")
print(df.head())

print("\nDataset Info:")
df.info()

print("\nStatistical Summary:")
print(df.describe())

# 3. Handle Missing Values Properly

print("\nMissing Values Before Cleaning:")
print(df.isnull().sum())

# Fill numeric missing values safely (Pandas 3.x compatible)
df["Price"] = df["Price"].fillna(df["Price"].median())

# Drop rows where essential columns are missing
df = df.dropna(subset=["Company", "Inches", "Weight"])

print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

df = df.sort_values("serial no")
df["serial no"] = range(1, len(df) + 1)

# 4. Convert Columns to Proper Data Types

# Convert Inches to numeric
df["Inches"] = pd.to_numeric(df["Inches"], errors="coerce")

# Clean Weight column (remove 'kg' and convert)
df["Weight"] = df["Weight"].str.replace("kg", "", regex=False)
df["Weight"] = pd.to_numeric(df["Weight"], errors="coerce")

# Drop rows if conversion created NaN
df = df.dropna(subset=["Inches", "Weight"])

# 5. Filter and Sort Data

high_price = df[df["Price"] > 50000]
sorted_df = df.sort_values(by="Price", ascending=False)

print("\nTop 5 Expensive Laptops:")
print(sorted_df.head())

# 6. Group Data and Calculate Aggregates

company_avg_price = df.groupby("Company")["Price"].mean().sort_values(ascending=False)

print("\nAverage Price by Company:")
print(company_avg_price)

# 7. Add New Calculated Columns

# Price Category
df["Price_Category"] = df["Price"].apply(
    lambda x: "Budget" if x < 40000 else
              "Mid-Range" if x < 80000 else
              "Premium"
)

# Price per Inch
df["Price_per_Inch"] = df["Price"] / df["Inches"]

# Price per Kg
df["Price_per_Kg"] = df["Price"] / df["Weight"]

print("\nNew Columns Preview:")
print(df[["Price", "Inches", "Weight", "Price_per_Inch", "Price_Category"]].head())

# 8. Export Cleaned Dataset

df.to_csv("cleaned_laptops.csv", index=False)

print("\nCleaned dataset saved as cleaned_laptops.csv")

# 9. Insights Section

print("\n Key Insights:")
print("Most Expensive Brand (Average):", company_avg_price.idxmax())
print("Cheapest Brand (Average):", company_avg_price.idxmin())
print("Total Records After Cleaning:", len(df))
print("Premium Laptops Count:", (df["Price_Category"] == "Premium").sum())
print("Budget Laptops Count:", (df["Price_Category"] == "Budget").sum())
