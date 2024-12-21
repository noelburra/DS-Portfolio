
# import libraries
import pandas as pd
import seaborn as sns
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# File 
COPPER = "copper_prices_2010_to_2024 2(in).csv"
GOLD = "gold_prices_2010_to_2024 2(in).csv"
PLATINUM = "platinum_prices_2010_to_2024 2(in).csv"
SILVER = "silver_prices_2010_to_2024 2(in).csv"
UNRATE = "unemployment_rate_monthly_data_2010_to_2024 2(in).csv"
CRUDE = "brent_crude_prices_2010_to_2024 2(in).csv"
CURRENCY = "usd_jpy_prices_2010_to_2024 2(in).csv"

# Process monthly returns
def process_monthly_returns_data(file_name):
    '''reads the data based on the date monthly
    '''
    df = pd.read_csv(file_name, skiprows=2)
    df.columns = ["Date", "Adj Close", "Close", "High", "Low", "Open", "Volume"]
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")[["Date", "Adj Close"]]
    df.set_index("Date", inplace=True)
    
    monthly_prices = df.resample("MS").first()
    monthly_returns = monthly_prices.pct_change().dropna()
    monthly_returns.rename(columns={"Adj Close": "Monthly Return"}, inplace=True)
    monthly_returns.reset_index(inplace=True)
    
    return monthly_returns

# Process daily returns
def process_daily_returns_data(file_name):
    '''reads the data based on the date daily
    '''
    df = pd.read_csv(file_name, skiprows=2)
    df.columns = ["Date", "Adj Close", "Close", "High", "Low", "Open", "Volume"]
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")[["Date", "Adj Close"]]
    df = df.iloc[1:]
    df["Daily Return"] = df["Adj Close"].pct_change().dropna()
    
    return df.dropna()[["Date", "Daily Return"]]

# Merge datasets
def merge_datasets(main_data, other_data, on="Date", suffixes=("", ""), how="inner"):
    '''merges the datasets for ease of use
    '''

    return pd.merge(main_data, other_data, on=on, how=how, suffixes=suffixes)

# Monte Carlo simulation
def monte_carlo_simulation(data_x, data_y, num_simulations=10000):
    '''performs monte carlo simulation
    '''
    mean_x, std_x = stats.norm.fit(data_x)
    mean_y, std_y = stats.norm.fit(data_y)
    simulated_x = np.random.normal(mean_x, std_x, num_simulations)
    simulated_y = np.random.normal(mean_y, std_y, num_simulations)
    simulated_correlations = np.corrcoef(simulated_x, simulated_y)[0, 1]

    return simulated_x, simulated_y, simulated_correlations

# Visualizations 
def plot_scatter_with_trend(ax, x, y, title, x_label, y_label, color):
    '''plots scatterplot with regression trendline
    '''
    ax.scatter(x, y, color=color, alpha=0.7, label="Data Points")
    sns.regplot(x=x, y=y, ax=ax, scatter=False, color=color, label="Trend Line", line_kws={"linestyle": "--"})
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.legend()

def plot_line_graph(ax, data, commodity_name):
    '''plots line graph 
    '''
    ax.plot(data["Date"], data["Daily Return_Crude"], label="Crude Oil", color="blue", linestyle="-")
    ax.plot(data["Date"], data[f"Daily Return_{commodity_name}"], label=commodity_name, color="orange", linestyle="-")
    ax.set_title(f"Crude Oil vs {commodity_name} Daily Returns", fontsize=14)
    ax.set_ylabel("Daily Returns")
    ax.legend(loc="upper right")
    ax.grid(alpha=0.4)

def plot_density(data_dict, title):
    '''plots density graph
    '''
    plt.figure(figsize=(12, 8))
    for asset, df in data_dict.items():
        sns.kdeplot(data=df, x="Daily Return", label=asset, linewidth=2)
    plt.title(title, fontsize=16)
    plt.xlabel("Daily Return", fontsize=12)
    plt.ylabel("Density", fontsize=12)
    plt.legend(loc="upper left", fontsize=10)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_monte_carlo(simulated_x, simulated_y, simulated_correlations, title):
    '''plots scatterplot from monte carlo simulations
    '''
    plt.figure(figsize=(10, 6))
    plt.scatter(simulated_x, simulated_y, alpha=0.5, label=f"Simulated Correlation: {simulated_correlations:.2f}")
    plt.title(title, fontsize=16)
    plt.xlabel("Simulated Unemployment Rate")
    plt.ylabel("Simulated Commodity Monthly Return")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.show()

def main():
    
# UNEMPLOYMENT VS COMMODITIES

    # Monthly returns for commodities
    copper_returns = process_monthly_returns_data(COPPER)
    gold_returns = process_monthly_returns_data(GOLD)
    platinum_returns = process_monthly_returns_data(PLATINUM)
    silver_returns = process_monthly_returns_data(SILVER)
    
    # Unemployment data
    unemployment_df = pd.read_csv(UNRATE)
    unemployment_df["DATE"] = pd.to_datetime(unemployment_df["DATE"])
    unemployment_df.rename(columns={"DATE": "Date", "UNRATE": "Unemployment Rate"}, inplace=True)
    
    # Merge unemployment and commodities
    merged_copper = merge_datasets(copper_returns, unemployment_df)
    merged_gold = merge_datasets(gold_returns, unemployment_df)
    merged_platinum = merge_datasets(platinum_returns, unemployment_df)
    merged_silver = merge_datasets(silver_returns, unemployment_df)
    
    # Unemployment and commodities correlation
    correlation_copper = merged_copper["Monthly Return"].corr(merged_copper["Unemployment Rate"])
    correlation_gold = merged_gold["Monthly Return"].corr(merged_gold["Unemployment Rate"])
    correlation_platinum = merged_platinum["Monthly Return"].corr(merged_platinum["Unemployment Rate"])
    correlation_silver = merged_silver["Monthly Return"].corr(merged_silver["Unemployment Rate"])
    print(f"Correlation between Unemployment Rate and Copper Monthly Returns: {correlation_copper:.4f}")
    print(f"Correlation between Unemployment Rate amnd Gold Monthly Returns: {correlation_gold:.4f}")
    print(f"Correlation between Unemployment Rate and Platinum Monthly Returns: {correlation_platinum:.4f}")
    print(f"Correlation between Unemployment Rate and Silver Monthly Returns: {correlation_silver:.4f}")
    
    # Unemployment scatter plots
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    plot_scatter_with_trend(axes[0, 0], merged_copper["Unemployment Rate"], merged_copper["Monthly Return"],
                            "Copper Monthly Returns vs. Unemployment Rate", "Unemployment Rate", "Copper Monthly Return", color="red")
    plot_scatter_with_trend(axes[0, 1], merged_gold["Unemployment Rate"], merged_gold["Monthly Return"],
                            "Gold Monthly Returns vs. Unemployment Rate", "Unemployment Rate", "Gold Monthly Return", color="gold")
    plot_scatter_with_trend(axes[1, 0], merged_platinum["Unemployment Rate"], merged_platinum["Monthly Return"],
                            "Platinum Monthly Returns vs. Unemployment Rate", "Unemployment Rate", "Platinum Monthly Return", color="purple")
    plot_scatter_with_trend(axes[1, 1], merged_silver["Unemployment Rate"], merged_silver["Monthly Return"],
                            "Silver Monthly Returns vs. Unemployment Rate", "Unemployment Rate", "Silver Monthly Return", color="silver")
    plt.tight_layout()
    plt.show()
    
    # Monte Carlo simulation based on unemployment rates
    simulated_x_copper, simulated_y_copper, simulated_corr_copper = monte_carlo_simulation(
        merged_copper["Unemployment Rate"], merged_copper["Monthly Return"]
    )
    plot_monte_carlo(simulated_x_copper, simulated_y_copper, simulated_corr_copper,
                     "Monte Carlo Simulation: Copper vs Unemployment Rate")
    
    simulated_x_gold, simulated_y_gold, simulated_corr_gold = monte_carlo_simulation(
        merged_gold["Unemployment Rate"], merged_gold["Monthly Return"]
    )
    plot_monte_carlo(simulated_x_gold, simulated_y_gold, simulated_corr_gold,
                     "Monte Carlo Simulation: Gold vs Unemployment Rate")

    simulated_x_platinum, simulated_y_platinum, simulated_corr_platinum = monte_carlo_simulation(
        merged_platinum["Unemployment Rate"], merged_platinum["Monthly Return"]
    )
    plot_monte_carlo(simulated_x_platinum, simulated_y_platinum, simulated_corr_platinum,
                     "Monte Carlo Simulation: Platinum vs Unemployment Rate")

    simulated_x_silver, simulated_y_silver, simulated_corr_silver = monte_carlo_simulation(
        merged_silver["Unemployment Rate"], merged_silver["Monthly Return"]
    )
    plot_monte_carlo(simulated_x_silver, simulated_y_silver, simulated_corr_silver,
                     "Monte Carlo Simulation: Silver vs Unemployment Rate")

# CRUDE OIL VS COMMODITIES 

    # Crude oil and commodities daily returns
    crude_daily_returns = process_daily_returns_data(CRUDE)
    copper_daily_returns = process_daily_returns_data(COPPER)
    gold_daily_returns = process_daily_returns_data(GOLD)
    platinum_daily_returns = process_daily_returns_data(PLATINUM)
    silver_daily_returns = process_daily_returns_data(SILVER)
    
    # Merge crude oil and commodities
    merged_crude_copper = merge_datasets(crude_daily_returns, copper_daily_returns, suffixes=("_Crude", "_Copper"))
    merged_crude_gold = merge_datasets(crude_daily_returns, gold_daily_returns, suffixes=("_Crude", "_Gold"))
    merged_crude_platinum = merge_datasets(crude_daily_returns, platinum_daily_returns, suffixes=("_Crude", "_Platinum"))
    merged_crude_silver = merge_datasets(crude_daily_returns, silver_daily_returns, suffixes=("_Crude", "_Silver"))
    
    # Crude oil and commodities correlation
    correlation_crude_copper = merged_crude_copper["Daily Return_Crude"].corr(merged_crude_copper["Daily Return_Copper"])
    correlation_crude_gold = merged_crude_gold["Daily Return_Crude"].corr(merged_crude_gold["Daily Return_Gold"])
    correlation_crude_platinum = merged_crude_platinum["Daily Return_Crude"].corr(merged_crude_platinum["Daily Return_Platinum"])
    correlation_crude_silver = merged_crude_silver["Daily Return_Crude"].corr(merged_crude_silver["Daily Return_Silver"])
    print(f"Correlation between Crude Oil and Copper Daily Returns: {correlation_crude_copper:.4f}")
    print(f"Correlation between Crude Oil and Gold Daily Returns: {correlation_crude_gold:.4f}")
    print(f"Correlation between Crude Oil and Platinum Daily Returns: {correlation_crude_platinum:.4f}")
    print(f"Correlation between Crude Oil and Silver Daily Returns: {correlation_crude_silver:.4f}")
    
    # Crude oil line graph
    fig, axes = plt.subplots(4, 1, figsize=(14, 20), sharex=True)
    plot_line_graph(axes[0], merged_crude_copper, "Copper")
    plot_line_graph(axes[1], merged_crude_gold, "Gold")
    plot_line_graph(axes[2], merged_crude_platinum, "Platinum")
    plot_line_graph(axes[3], merged_crude_silver, "Silver")
    plt.xlabel("Date", fontsize=12)
    plt.tight_layout()
    plt.suptitle("Daily Returns: Crude Oil vs Other Commodities (Line Graphs)", fontsize=16, y=1.02)
    plt.show()

# CURRENCY VS COMMODITIES

    # USD/JPY daily returns
    currency_daily_returns = process_daily_returns_data(CURRENCY)
    
    # Merge currency and commodities
    merged_currency_copper = merge_datasets(currency_daily_returns, copper_daily_returns, suffixes=("_Currency", "_Copper"))
    merged_currency_gold = merge_datasets(currency_daily_returns, gold_daily_returns, suffixes=("_Currency", "_Gold"))
    merged_currency_platinum = merge_datasets(currency_daily_returns, platinum_daily_returns, suffixes=("_Currency", "_Platinum"))
    merged_currency_silver = merge_datasets(currency_daily_returns, silver_daily_returns, suffixes=("_Currency", "_Silver"))

    # Currency and commodities correlation
    correlation_currency_copper = merged_currency_copper["Daily Return_Currency"].corr(merged_currency_copper["Daily Return_Copper"])
    correlation_currency_gold = merged_currency_gold["Daily Return_Currency"].corr(merged_currency_gold["Daily Return_Gold"])
    correlation_currency_platinum = merged_currency_platinum["Daily Return_Currency"].corr(merged_currency_platinum["Daily Return_Platinum"])
    correlation_currency_silver = merged_currency_silver["Daily Return_Currency"].corr(merged_currency_silver["Daily Return_Silver"])
    print(f"Correlation between USD/JPY and Copper Daily Returns: {correlation_currency_copper:.4f}")
    print(f"Correlation between USD/JPY and Gold Daily Returns: {correlation_currency_gold:.4f}")
    print(f"Correlation between USD/JPY and Platinum Daily Returns: {correlation_currency_platinum:.4f}")
    print(f"Correlation between USD/JPY and Silver Daily Returns: {correlation_currency_silver:.4f}")

    # Currency density plot
    data_dict = {
        "USD/JPY": currency_daily_returns,
        "Copper": copper_daily_returns,
        "Gold": gold_daily_returns,
        "Platinum": platinum_daily_returns,
        "Silver": silver_daily_returns
    }
    plot_density(data_dict, "Density Plot: USD/JPY vs Commodities Daily Returns")

if __name__ == "__main__":
    main()

