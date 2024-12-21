import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

copper_prices = pd.read_csv('/mnt/data/copper_prices_2010_to_2024 2.xlsx')
gold_prices = pd.read_csv('/mnt/data/gold_prices_2010_to_2024 2.xlsx')
platinum_prices = pd.read_csv('/mnt/data/platinum_prices_2010_to_2024 2.xlsx')
silver_prices = pd.read_csv('/mnt/data/silver_prices_2010_to_2024 2.xlsx')
sp500_prices = pd.read_csv('/mnt/data/sp500_prices_2010_to_2024 2.xlsx')
industrial_production = pd.read_csv('/mnt/data/industrial_production_monthly_data_2010_to_2024 2.xlsx')


def clean_data(df, name):
    df = df.iloc[2:] 
    df.columns = ['Date', f'{name}_Adj_Close', f'{name}_Close', f'{name}_High', f'{name}_Low', f'{name}_Open', f'{name}_Volume']
    df['Date'] = pd.to_datetime(df['Date'])  
    df = df[['Date', f'{name}_Adj_Close']].dropna()  
    df[f'{name}_Adj_Close'] = pd.to_numeric(df[f'{name}_Adj_Close'], errors='coerce')  # Convert prices to numeric
    return df

copper_prices = clean_data(copper_prices, 'Copper')
gold_prices = clean_data(gold_prices, 'Gold')
platinum_prices = clean_data(platinum_prices, 'Platinum')
silver_prices = clean_data(silver_prices, 'Silver')
sp500_prices = clean_data(sp500_prices, 'SP500')

industrial_production.columns = ['Date', 'Industrial_Production']
industrial_production['Date'] = pd.to_datetime(industrial_production['Date'])
industrial_production['Industrial_Production'] = pd.to_numeric(industrial_production['Industrial_Production'], errors='coerce')

def merge_with_industrial(df, industrial_df, name):
    merged = pd.merge(df, industrial_df, on='Date', how='inner')
    merged.rename(columns={f'{name}_Adj_Close': 'Price', 'Industrial_Production': 'Industrial Production'}, inplace=True)
    return merged

gold_data = merge_with_industrial(gold_prices, industrial_production, 'Gold')
silver_data = merge_with_industrial(silver_prices, industrial_production, 'Silver')
platinum_data = merge_with_industrial(platinum_prices, industrial_production, 'Platinum')
copper_data = merge_with_industrial(copper_prices, industrial_production, 'Copper')

merged_data = copper_prices.merge(gold_prices, on='Date', how='inner') \
                           .merge(platinum_prices, on='Date', how='inner') \
                           .merge(silver_prices, on='Date', how='inner') \
                           .merge(sp500_prices, on='Date', how='inner')

for col in merged_data.columns[1:]:
    merged_data[f'{col}_Return'] = merged_data[col].pct_change()

merged_data = merged_data.dropna()

# Rolling Correlation Plot
plt.figure(figsize=(12, 8))
rolling_window = 60  # 3-month rolling window (assuming ~20 trading days/month)
for col in ['Copper_Adj_Close', 'Gold_Adj_Close', 'Platinum_Adj_Close', 'Silver_Adj_Close']:
    merged_data[f'Rolling_Corr_{col}'] = merged_data['SP500_Adj_Close_Return'].rolling(rolling_window).corr(merged_data[f'{col}_Return'])
    plt.plot(merged_data['Date'], merged_data[f'Rolling_Corr_{col}'], label=col.split('_')[0])

plt.title('Rolling Correlation: S&P 500 vs. Commodities', fontsize=16)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Correlation', fontsize=14)
plt.axhline(0, color='black', linestyle='--', linewidth=0.7)
plt.legend(fontsize=12)
plt.grid(True)
plt.show()

# Heatmap of Correlation Coefficients
corr_matrix = merged_data[[
    'SP500_Adj_Close_Return',
    'Copper_Adj_Close_Return',
    'Gold_Adj_Close_Return',
    'Platinum_Adj_Close_Return',
    'Silver_Adj_Close_Return'
]].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Correlation Matrix: S&P 500 vs. Commodities', fontsize=16)
plt.show()

# Plotting Industrial Production and Commodity Prices
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
commodities = {
    "Gold": gold_data,
    "Silver": silver_data,
    "Platinum": platinum_data,
    "Copper": copper_data
}

for ax, (name, data) in zip(axes.flatten(), commodities.items()):
    ax.plot(data['Date'], data['Industrial Production'], label='Industrial Production', color='orange')
    ax.plot(data['Date'], data['Price'], label=f'{name} Price', color='coral')
    ax.set_title(f'{name} Price and Industrial Production Over Time', fontsize=14)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Value', fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(True)

plt.tight_layout()
plt.show()
