#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Noel Burra 
08/28/2024
Database: Open Database, Contents: Database Contents
"""

# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
import seaborn as sns

# Read the datafile 
file = "stroke_data.txt"
data = pd.read_csv(file, delimiter=",")  

# Create a column list 
columns_data = [
    'gender', 'hypertension', 'heart_disease', 
    'ever_married', 'work_type', 'Residence_type', 
    'smoking_status'
]

# Visualize the counts for each factor 
for column in columns_data:
    counts = data[column].value_counts()
    plt.figure(figsize=(15, 10))
    plt.bar(counts.index, counts.values, color='lightcoral')
    plt.title('Count of ' + column.capitalize())
    plt.xlabel('Count')
    plt.ylabel(column.capitalize())
    plt.show()

# Visualize stroke incidence by work type
work_type_incidence = data.groupby('work_type')['stroke'].mean()
plt.figure(figsize=(15, 10))
work_type_incidence.plot(kind='bar', color='teal')
plt.title('Average Stroke Risk by Work Type')
plt.xlabel('Work Type')
plt.ylabel('Average Incidence')
plt.xticks(rotation=45)
plt.show()

# Visualize stroke incidence by residence type
residence_incidence = data.groupby('Residence_type')['stroke'].mean()
plt.figure(figsize=(6, 4))
residence_incidence.plot(kind='bar', color='plum')
plt.title('Average Stroke Risk by Residence Type')
plt.xlabel('Residence Type')
plt.ylabel('Average Incidence')
plt.xticks([0, 1], ['Rural', 'Urban'], rotation=0)
plt.show()

# Visualize stroke incidence by smoking status
smoking_incidence = data.groupby('smoking_status')['stroke'].mean()
plt.figure(figsize=(8, 4))
smoking_incidence.plot(kind='bar', color='darkgoldenrod')
plt.title('Average Stroke Risk by Smoking Status')
plt.xlabel('Smoking Status')
plt.ylabel('Average Incidence')
plt.xticks(rotation=45)
plt.show()

# Encode factors using .replace()
data_encode = data.copy()
data_encode['gender'] = data_encode['gender'].replace({'Male': 1, 'Female': 0})
data_encode['ever_married'] = data_encode['ever_married'].replace({'Yes': 1, 'No': 0})
data_encode['Residence_type'] = data_encode['Residence_type'].replace({'Urban': 1, 'Rural': 0})
work_type_mapping = {'Private': 0, 'Self-employed': 1, 'Govt_job': 2, 'children': 3, 'Never_worked': 4}
data_encode['work_type'] = data_encode['work_type'].replace(work_type_mapping)
smoking_status_mapping = {'never smoked': 0, 'formerly smoked': 1, 'smokes': 2, 'Unknown': 3}
data_encode['smoking_status'] = data_encode['smoking_status'].replace(smoking_status_mapping)

# Calculate the correlation of each factor to resulting in a stroke
correlation_matrix = data_encode.corr()
correlation_with_stroke = correlation_matrix['stroke'].drop('stroke')

# Sort the factors 
sort_factors = correlation_with_stroke.abs().sort_values(ascending=False)

# Visualize the correlations 
plt.figure(figsize=(12, 8))
sns.stripplot(x=sort_factors.values, y=sort_factors.index, color='red', size=10)
plt.title("Stroke Factor Correlation")
plt.xlabel("Correlation Value")
plt.ylabel("Factors")
plt.show()

# Create bins to categorize the age column into increasing ranges 
bins = [0, 30, 40, 50, 60, 70, 80, 90, 100]
labels = ['0-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91-100']
data['age_group'] = pd.cut(data['age'], bins=bins, labels=labels, right=False)

# Calculate the stroke incidence for each age group
age_group_stroke = data.groupby('age_group')['stroke'].mean()

# Visualize the stroke risk by age group
plt.figure(figsize=(10, 6))
plt.fill_between(age_group_stroke.index, age_group_stroke.values, color='pink', alpha=0.5)
plt.plot(age_group_stroke.index, age_group_stroke.values, marker='o', color='deeppink')
plt.title('Average Stroke Risk by Age Group')
plt.xlabel('Age Group')
plt.ylabel('Average Incidence')
plt.xticks(rotation=45)
plt.show()

# T-test to compare age between patients
age_group_yes_stroke = data[data['stroke'] == 1]['age']
age_group_no_stroke = data[data['stroke'] == 0]['age']
t_stat, p_value = ttest_ind(age_group_yes_stroke, age_group_no_stroke)
print('T-test: t-statistic = ' + str(round(t_stat, 2)) + ', p-value = ' + str(round(p_value, 2)))