import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. DATA GENERATION (NumPy & Pandas)
# Hum ek dummy dataset bana rahe hain practice ke liye
np.random.seed(42)  # Results same rakhne ke liye

data_size = 100
categories = ['Electronics', 'Clothing', 'Furniture', 'Stationery']
regions = ['North', 'South', 'East', 'West']

data = {
    'Date': pd.date_range(start='2024-01-01', periods=data_size),
    'Category': np.random.choice(categories, data_size),
    'Region': np.random.choice(regions, data_size),
    'Sales': np.random.randint(100, 5000, data_size), # Sales between 100 and 5000
    'Profit': np.random.randint(-500, 2000, data_size) # Profit (loss bhi ho sakta hai)
}

df = pd.DataFrame(data)

# 2. DATA INSPECTION (Pandas)
print("--- Data ki pehli 5 lines ---")
print(df.head())

print("\n--- Data Info ---")
print(df.info())

print("\n--- Summary Statistics ---")
print(df.describe())

# 3. DATA ANALYSIS (Pandas GroupBy)
# Har category ka total sales nikalte hain
category_sales = df.groupby('Category')['Sales'].sum().reset_index()
print("\n--- Category wise Total Sales ---")
print(category_sales)

# 4. VISUALIZATION (Matplotlib & Seaborn)

# Set the style
sns.set_theme(style="whitegrid")
plt.figure(figsize=(15, 10))

# Plot 1: Bar Chart - Category wise Sales
plt.subplot(2, 2, 1)
sns.barplot(x='Category', y='Sales', data=category_sales, palette='viridis')
plt.title('Total Sales by Category')
plt.xlabel('Category')
plt.ylabel('Total Sales')

# Plot 2: Box Plot - Sales Distribution by Region
plt.subplot(2, 2, 2)
sns.boxplot(x='Region', y='Sales', data=df, palette='Set2')
plt.title('Sales Distribution by Region')

# Plot 3: Line Plot - Sales trend over Date (First 20 days)
plt.subplot(2, 2, 3)
sns.lineplot(x='Date', y='Sales', data=df.iloc[:20], marker='o', color='blue')
plt.title('Sales Trend (First 20 Days)')
plt.xticks(rotation=45)

# Plot 4: Heatmap - Correlation Matrix
# (Check karte hain ki Sales aur Profit mein kya relation hai)
plt.subplot(2, 2, 4)
numeric_df = df[['Sales', 'Profit']] # Sirf numbers select karte hain correlation ke liye
correlation = numeric_df.corr()
sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation: Sales vs Profit')

plt.tight_layout()
plt.show()