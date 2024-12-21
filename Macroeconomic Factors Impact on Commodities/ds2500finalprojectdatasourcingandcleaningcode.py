#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: anoopdindigal
DS 2500 Final Project Data Sourcing
NUID: 002973221
3 December 2024
"""

import yfinance as yf
import pandas as pd
from pandas_datareader import data as pdr
from datetime import datetime

# Defines daily tickers for commodities and factors (from Yahoo Finance)
# Commodities include gold, silver, platinum, and copper, and factors include
# S&P 500, VIX Index, Brent Crude Oil, and USD/JPY Exchange
daily_tickers = {
    "gold": "GC=F",               
    "silver": "SI=F",             
    "platinum": "PL=F",           
    "copper": "HG=F",             
    "sp500": "^GSPC",            
    "vix": "^VIX",                
    "brent_crude": "BZ=F",        
    "usd_jpy": "JPY=X",           
}

# Defines monthly data tickers for factors (from FRED), including US 
# Unemployment Rate, US Industrial Production, Federal Funds Rate, and CPI
monthly_tickers = {
    "unemployment_rate": "UNRATE",       
    "industrial_production": "INDPRO",   
    "fed_funds_rate": "FEDFUNDS",         
    "cpi": "CPIAUCSL",                   
}

# Defines the date range for data download
start_date = "2010-11-23"   
end_date = "2024-11-23"   

def download_daily_data(tickers, start_date, end_date):
    """Downloads daily data from Yahoo Finance and saves it to CSV."""
    for asset, ticker in tickers.items():
        # Downloads the asset's daily price data for the defined date range
        data = yf.download(
            ticker, start=start_date, end=end_date, interval="1d"
        )
        # Prints the first few rows of the data for a quick preview
        print(
            f"First few rows of {asset.replace('_', ' ').capitalize()} "
            f"(daily) data:"
        )
        print(data.head())
        # Defines the CSV filename for the asset's daily data
        csv_filename = f"{asset}_daily_prices_2010_to_2024.csv"
        # Saves the data to a CSV file
        data.to_csv(csv_filename)
        # Prints confirmation that the data was saved
        print(
            f"{asset.replace('_', ' ').capitalize()} (daily) data saved to "
            f"{csv_filename}"
        )

def download_monthly_data(tickers, start_date, end_date):
    """Downloads monthly data from FRED, processes CPI growth rate, 
    and saves it to CSV."""
    for factor, ticker in tickers.items():
        # Retrieves monthly data from FRED using pandas_datareader
        data = pdr.get_data_fred(
            ticker,
            start=datetime.strptime(start_date, "%Y-%m-%d"),
            end=datetime.strptime(end_date, "%Y-%m-%d"),
        )
        if factor == "cpi":
            # If the factor is CPI, calculate the monthly CPI growth rate
            data["CPI Growth Rate (%)"] = data[ticker].pct_change() * 100
            # Prints the first few rows of the CPI data with the growth rate
            print(
                f"First few rows of {factor.replace('_', ' ').capitalize()} "
                f"(monthly) data with growth rate:"
            )
        else:
            # For other factors, print first few rows without the growth rate
            print(
                f"First few rows of {factor.replace('_', ' ').capitalize()} "
                f"(monthly) data:"
            )
        print(data.head())
        # Defines the CSV filename for the factor's monthly data
        csv_filename = f"{factor}_monthly_data_2010_to_2024.csv"
        # Saves the data to a CSV file
        data.to_csv(csv_filename)
        # Prints confirmation that the data was saved
        print(
            f"{factor.replace('_', ' ').capitalize()} (monthly) data saved to "
            f"{csv_filename}"
        )

def main():
    """Main function to execute all downloads of daily and monthly data."""
    download_daily_data(daily_tickers, start_date, end_date)
    download_monthly_data(monthly_tickers, start_date, end_date)

if __name__ == "__main__":
    main()



    










