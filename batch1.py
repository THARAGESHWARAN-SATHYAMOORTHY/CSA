# -*- coding: utf-8 -*-
"""Batch1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-iPWJ_9v2mrk3nUzYWfp4U5Zpdqj4O7F
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import random
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

df =pd.read_csv("cyber crime(2017-2020).csv")

df

df.describe()

num_rows, num_columns = df.shape

print("Number of rows:", num_rows)
print("Number of columns:", num_columns)

print("\nS.No      ColumnName                                        Datatype")
for k,(i,j) in enumerate(df.dtypes.items(),start=1):
  print(f'{k:<10}{i:<50}{j}')

df.drop([29,37,38,68,76,77,78,108,116,117,146,155,156],axis=0,inplace=True)

a=[i for i in range(144)]
df['Index']=a
df.set_index('Index',inplace=True)

num_rows, num_columns = df.shape

print("Number of rows:", num_rows)
print("Number of columns:", num_columns)

plt.figure(figsize=(50,25))
sns.heatmap(df.corr(), annot=True)
plt.show()

num = df.select_dtypes(include=[np.number]).columns
plt.figure(figsize=(100,100))
sns.boxplot(df[num])

plt.figure(figsize=(20,8))
sns.scatterplot(df[num])

num = df.select_dtypes(include=[np.number])
mean = num.mean()
median = num.median()

quartiles = num.quantile([0.25, 0.5, 0.75])

min_val = num.min()
max_val = num.max()

mode = df.mode()

print("\nMean:\n\n", mean)
print("\nMedian:\n\n", median)
print("\nQuartiles:\n\n", quartiles)
print("\nMin:\n\n", min_val)
print("\nMax:\n\n", max_val)
print("\nMode:\n\n", mode)

numeric = df.select_dtypes(include=np.number)

for i in numeric.columns:
  column = numeric[i]

  Q1 = column.quantile(0.25)
  Q3 = column.quantile(0.75)

  IQR = Q3 - Q1

  lower_threshold = Q1 - 1.5 * IQR
  upper_threshold = Q3 + 1.5 * IQR

  outliers = column[(column < lower_threshold) | (column > upper_threshold)]

  print("\n\nOutliers of",i,":\n")
  print(outliers)

print(df.isna().sum())

numeric_columns = df.select_dtypes(include=np.number).columns
for i in numeric_columns:
    df[i] = df[i].fillna(df[i].mean())
categorical_columns = df.select_dtypes(include='object').columns
for i in categorical_columns:
    df[i] = df[i].fillna(df[i].mode()[0])

print(df.isna().sum())

# m=MinMaxScaler()
# df[numeric_columns]=m.fit_transform(df[numeric_columns])
# print(df)

dictionary={}
for i in range(len(df)):
  if df.iloc[i,25]==2020:
    if df.iloc[i,1]=='State':
      dictionary[df.iloc[i,2]]=df.iloc[i,24]
print(dictionary)

m = -1
s = ''
# for i,j in dictionary.items():
#   if j>m:
#     m = j
#     s = i
print('State that has the highest cases in the year 2020 :',s)

d = sorted(dictionary.values(), reverse=True)
for i, j in dictionary.items():
  if j == d[0]:
    s = i

print('State that has the highest cases in the year 2020 :',s)

mdc={2019:0,2020:0}

for i in range(len(df)):
  if df.iloc[i,1]!='State':
    if df.iloc[i,25]==2019:
      mdc[2019]+=df.iloc[i,24]
    elif df.iloc[i,25]==2020:
      mdc[2020]+=df.iloc[i,24]

k=[mdc[2019],mdc[2020]]
plt.pie(k,labels=[f'2019 cases : {k[0]}',f'2020 cases : {k[1]}'])

encoded = pd.get_dummies(df, columns=['Category','State/UT'])

l = LabelEncoder()
X = encoded.drop(columns=['Year'], axis=1)
y = encoded['Year']

L = l.fit_transform(y)
s = SelectKBest(score_func=chi2, k=3)
s.fit_transform(X, L)
score = pd.Series(s.scores_, index=X.columns)
print(score)

top3_features = score.nlargest(3)
print("Top 3 features:")
print(top3_features)

df['bins']=pd.qcut(df['Year'], 20 , duplicates='drop')
print('\nBining\n',df['Year'])
bin_means=df.groupby('bins')['Year'].mean()
df['Year']=df['bins'].map(bin_means)
df.drop('bins',axis=1,inplace=True)
print('\n\nAfter Binning\n',df['Year'])

X1,X2,y1,y2 = train_test_split(X,y,train_size=0.4,random_state=42)

d=DecisionTreeClassifier(max_depth=10000)
d.fit(X1,y1)
ypre=d.predict(X2)
print(accuracy_score(ypre,y2))