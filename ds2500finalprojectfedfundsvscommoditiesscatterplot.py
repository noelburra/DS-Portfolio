#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: anoopdindigal
DS2500 Final Project Code
NUID: 002973221
3 December 2024
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Inputs CSV file names for the commodity data
commodity_files = {
    "Gold": "gold_prices_2010_to_2024.csv",       
    "Silver": "silver_prices_2010_to_2024.csv",     
    "Platinum": "platinum_prices_2010_to_2024.csv",   
    "Copper": "copper_prices_2010_to_2024.csv"
}
# Inputs CSV file for the Fed Funds Rate data
fed_funds_file = "fed_funds_rate_monthly_data_2010_to_2024.csv"

# Defines a color map for the commodities to assign distinct colors to each
commodity_colors = {
    "Gold": "gold", 
    "Silver": "silver", 
    "Platinum": "purple", 
    "Copper": "brown"
}

def load_fed_funds_data(file):
    """Loads and preprocesses Fed Funds Rate data."""
    data = pd.read_csv(file)
    data = data.rename(
        columns={'DATE': 'Date', 'FEDFUNDS': 'Value'}
    )
    # Converts 'Date' column to datetime for better processing
    data['Date'] = pd.to_datetime(data['Date'])
    return data

def load_commodity_data(file):
    """Loads and preprocesses commodity data starting from row 4."""
    data = pd.read_csv(
        file, skiprows=3  
    )
    # Renames columns for easy understanding of the data
    data = data.rename(
        columns={data.columns[0]: 'Date', data.columns[1]: 'Adj Close'}
    )
    # Converts 'Date' column to datetime for proper time series processing
    data['Date'] = pd.to_datetime(
        data['Date'] 
    )
    return data

def calculate_correlation(data, x_col, y_col, commodity_name):
    """Calculates and prints correlation coefficient between two columns."""
    correlation = data[x_col].corr(data[y_col])
    
    # Determines the correlation type based on the coefficient value
    correlation_type = (
        "positive" if correlation > 0 
        else "negative" if correlation < 0 
        else "no linear relationship"
    )
    # Prints the correlation result for analysis
    print(
        f"Correlation between Fed Funds Rate and {commodity_name} Returns: "
        f"{correlation:.4f} ({correlation_type})"
    )
    return correlation

def plot_scatter(data, x_col, y_col, title, x_label, y_label, color):
    """Generates scatter plots with a dashed regression line for 
    visual analysis."""
    plt.figure(figsize=(10, 6))
    sns.regplot(
        data=data, x=x_col, y=y_col,
        scatter_kws={'color': color},  
        line_kws={'color': color, 'linestyle': '--'} 
    )
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()

def main():
    """Main function to load data, process it, and visualize correlations."""
    fed_funds_data = load_fed_funds_data(fed_funds_file)

    # Dictionary to hold merged data for each commodity
    merged_data = {}

    # Loads and processes each commodity data
    for commodity_name, commodity_file in commodity_files.items():
        # Loads commodity data for each commodity
        commodity_data = load_commodity_data(commodity_file)

        # Merges commodity data with Fed Funds data on 'Date' for 
        # joint analysis
        merged = pd.merge(
            fed_funds_data, commodity_data, 
            on='Date', how='inner'
        )
        # Stores the merged data for later use
        merged_data[commodity_name] = merged

        # Calculates percentage returns for the commodity based on adjusted 
        # close prices
        merged[f'{commodity_name} Returns'] = (
            merged['Adj Close'].pct_change() * 100
        )

        # Calculates and prints the correlation coefficient between Fed Funds 
        # Rate and commodity returns
        calculate_correlation(
            merged, 'Value', f'{commodity_name} Returns', 
            commodity_name
        )

        # Generates scatter plots with regression lines to visualize 
        # relationships, with each commodity getting a unique color from the 
        # defined map
        plot_scatter(
            merged, 'Value', f'{commodity_name} Returns',
            f"Fed Funds Rate vs {commodity_name} Monthly Returns 2010-2024",
            "Fed Funds Rate (%)", 
            f"{commodity_name} Monthly Returns (%)", 
            commodity_colors[commodity_name]
        )

if __name__ == "__main__":
    main()
    
    

    
    
    
    














