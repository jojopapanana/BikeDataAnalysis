#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 17 11:04:57 2025

@author: jovannamelissa
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_columns', None)
data = pd.read_excel('uncleaned bike sales data.xlsx')
data.info()
data.describe()
data.head(10)

data.columns = data.columns.str.strip()

data.loc[data.isna().any(axis=1)]
data.columns[data.isna().any()].tolist()

data['Day'] = data['Day'].fillna(data['Day'].mean())
data['Day'] = data['Day'].astype('int64')
data['Age_Group'] = data['Age_Group'].fillna(data['Age_Group'].mode().iloc[0])
data['Product_Description'] = data['Product_Description'].fillna(data['Product_Description'].mode().iloc[0])
data['Order_Quantity'] = data['Order_Quantity'].fillna(data['Order_Quantity'].mean())

data.loc[data.duplicated()]

data['Month'].value_counts()
data['Month'] = data['Month'].str.replace('Decmber', 'December')

data.plot(kind='box', subplots = True, layout=(9, 2), figsize=(20,20), showmeans=True)
plt.show()

number_data = data.select_dtypes(include='number')
q1 = number_data.quantile(0.25)
q3 = number_data.quantile(0.75)
iqr = q3 - q1

outlier_data = data[((data['Profit'] < q1['Profit'] - 1.5 * iqr['Profit']) | (data['Profit'] > q3['Profit'] + 1.5 * iqr['Profit']))
                    | ((data['Cost'] < q1['Cost'] - 1.5 * iqr['Cost']) | (data['Cost'] > q3['Cost'] + 1.5 * iqr['Cost']))
                    | ((data['Revenue'] < q1['Revenue'] - 1.5 * iqr['Revenue']) | (data['Revenue'] > q3['Revenue'] + 1.5 * iqr['Revenue']))
                    ]

#data correlation
sns.pairplot(data)
plt.show()

data['Year'] = data['Year'].astype(str)
corr_matrix = data.select_dtypes(include='number').corr()
sns.heatmap(corr_matrix, annot=True, cmap='YlGnBu')
plt.legend().set_visible(False)
plt.show()

#what is the correlation between cost and profit?
x = data['Cost']
y = data['Profit']
plt.scatter(x, y, color='orange', marker='*')
plt.title('Scatter Plot Cost and Profit')
plt.xlabel('Cost')
plt.ylabel('Profit')
plt.show()

# what is the age distribution of the customers?
age_plot = data['Age_Group'].value_counts()
plt.pie(age_plot.values, labels = age_plot.index, autopct='%1.1f%%')
plt.title('Age Group Distribution')
plt.show()

# which Gender has the most orders?
gender_plot = data['Customer_Gender'].value_counts()
x_gender = gender_plot.index
y_gender = gender_plot.values

plt.bar(x_gender, y_gender)
plt.title('Highest gender order')
for i in range(2):
    plt.text(x_gender[i], y_gender[i], f'{y_gender[i]}')
plt.show()

# which country/state generates the highest revenue?
country_plot = data.groupby('Country')['Revenue'].sum().sort_values(ascending = False).head(5)
x_country = country_plot.index
y_country = country_plot.values

plt.pie(y_country, labels=x_country, autopct='%1.1f%%')
plt.title('Highest revenue by countries')
plt.show()

state_plot = data.groupby('State')['Revenue'].sum().sort_values(ascending = False).head(5)
x_state = state_plot.index
y_state = state_plot.values

plt.pie(y_state, labels=x_state, autopct='%1.1f%%')
plt.title('Highest revenue by states')
plt.show()

# is there any correlation between the customer’s age and revenue?
plt.scatter(data['Customer_Age'], data['Revenue'], marker='o', color='blue')
plt.title('Correlation between customer\'s age and revenue')
plt.show()

data.to_csv('bike_data_cleaned.csv', index = False)
