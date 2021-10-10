#!/usr/bin/env python
# coding: utf-8

# # Telco Customer Churn EDA
#
# ** Task Description **
#
# In this analysis I will focus on exploring the telco customer churn dataset.
# The target variable is 'churn' which indicates if a customer has cancelled their contract.
#
# The goal of this analysis is to identify patterns and correlations with the target variable and finally list some potential action items for a potential management audience.
#
# ** Documentation **
#
# This dataset was downloaded from [Kaggle](https://www.kaggle.com/blastchar/telco-customer-churn/version/1?select=WA_Fn-UseC_-Telco-Customer-Churn.csv)
#
# The data dictionary can be found the [IBM Communit URL](https://community.ibm.com/community/user/businessanalytics/blogs/steven-macko/2019/07/11/telco-customer-churn-1113)
#

# In[110]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# In[87]:


df = pd.read_csv(r'D:\Documents\dataSets\telco_customer_churn.csv')


# # Data Understanding
#
# In this section, we will focus on inspecting the data surface properties:
#
# - data format
# - number of records and features
# - missing values

# In[88]:


df.shape


# In[89]:


df.head()


# In[90]:


df.isna().sum()


# No Missing Values

# In[91]:


df.info()


# In[92]:


for c in df.columns:
    print(f"Column:{c}",df[c].unique() )


# - Boolean values are mainly stored in Yes/No Format.
# - No cleansing needed within columns.
# - Total Charges is Obj Type. Why?
#

# In[93]:


df['TotalCharges'].sample(10)


# There are no characters attached to the total charges column. I will try to convert the column into float.

# In[94]:


pd.to_numeric(df['TotalCharges'])


# In[95]:


# We discover that white spaces are stored within the column. I will strip them out.


# In[96]:


df['TotalCharges'] =df.TotalCharges.str.strip()


# In[97]:


df['TotalCharges']=pd.to_numeric(df['TotalCharges'])
df['TotalCharges'] = df['TotalCharges'].fillna(0)
df['TotalCharges'].dtype


# In[98]:


df.TotalCharges.isnull().sum()


# I want to store all Obj Data in lower cases and finally convert Y/N columns into 1/0.

# In[99]:


for c in df.columns:
    if df[c].dtype == 'O':
        df[c] = df[c].str.lower()


# In[101]:


def converter(col):
    if col == 'yes':
        return 1
    else:
        return 0


# In[105]:


to_convert = ['Partner','Dependents','PhoneService','PaperlessBilling','Churn']

for c in to_convert:
    if c in df.columns:
        df[c] = df[c].apply(converter)


# Verify applied steps

# In[106]:


for c in df.columns:
    print(f"Column:{c}",df[c].unique() )

