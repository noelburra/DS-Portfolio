#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

# Noel Burra
# DS 2001 - Economics
# Final Project
# 11 March, 2024

# Reference link on how to merge csv using panda:
https://www.geeksforgeeks.org/how-to-merge-two-csv-files-by-specific-column-using-pandas-in-python/

"""

import pandas as pd
import matplotlib.pyplot as plt


def main():
    
    def merge_files(file1, file2, column):
        """
        merge two csv files and categorize plants into east and west
        Parameters:
        file1
        file2
        column
        Returns:
        output file, east_plants, west_plants
        """
        data1 = pd.read_csv(file1)
        data2 = pd.read_csv(file2)

        output_file = pd.merge(data1, data2, on=column, how='outer')

        east_plants = output_file[output_file['X'] > -119.5]
        west_plants = output_file[output_file['X'] <= -119.5]

        return output_file, east_plants, west_plants
        
    def plot_plants(merged_data):
        """
        make a plot of plants in east or west California
        Parameters:
        merged_data
        Returns:
        scatter plot
        """
        plt.figure(figsize=(15, 10))
        plt.scatter(east_plants['X'], east_plants['Y'], color='red', label='East')
        plt.scatter(west_plants['X'], west_plants['Y'], color='blue', label='West')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Power Plants in California')
        plt.legend()
        plt.grid(True)
        
        plt.show()

    def categorize_plants(list1, list2, merged_data):
        """
        categorize plants in east and west tuples based on renewable status: Y or N
        Parameters:
        east_plants
        west_plants
        merged_data
        Returns:
        tuple containing counts of renewable and nonrenewable plants for east and west
        """
        east_renewable = east_plants[east_plants['Renewable Flag'] == 'Y']
        east_nonrenewable = east_plants[east_plants['Renewable Flag'] == 'N']

        west_renewable = west_plants[west_plants['Renewable Flag'] == 'Y']
        west_nonrenewable = west_plants[west_plants['Renewable Flag'] == 'N']

        return (len(east_renewable), len(east_nonrenewable), len(west_renewable), len(west_nonrenewable))

    def plot_counts(tuple):
        """
        plot a bar graph of counts of renewable and nonrenewable plants for east and west
        Parameters:
        tuple containing counts of renewable and nonrenewable plants for east and west
        Returns:
        bar graph
        """
        renew_or_nonrenew_lists = ['East Renewable', 'East Nonrenewable', 'West Renewable', 'West Nonrenewable']
        counts_list = list(counts)

        plt.figure(figsize=(10, 7))
        plt.bar(renew_or_nonrenew_lists, counts_list, color=['orange', 'purple', 'orange', 'purple'])
        plt.xlabel('Region and Energy Status')
        plt.xticks(rotation=30)
        plt.ylabel('Counts')
        plt.title('Counts of Renewable and Nonrenewable Plants in the East and West')
        
        plt.show()
        
# main code

    merged_data, east_plants, west_plants = merge_files('California_Power_Plants.csv', 'Renewable_Energy_Flag.csv', 'PriEnergySource')
   
    plot_plants(merged_data)

    counts = categorize_plants(east_plants, west_plants, merged_data)
    
    plot_counts(counts)

main()
