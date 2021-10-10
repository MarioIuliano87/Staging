# Muenchen Price Analysis 

## Scope ##

This project goal is to outline exploration data analysis (EDA) steps to generate insights 
on a dataset. 

In this specific case, I'm imaging to be someone interested in having an air bnb in Muenchen and 
I want to explore the overall price distribution based on: 

- Listing locations 
- Listing characteristics 

At the end of this analysis I'm expecting to draw an insightful picture on the AirBnB scenario in Muenche. 

# Analysis # 

## Dataset understanding ##

I will first load the data to check its quality: 

- Data types
- Missing values

```python

import pandas as pd
path = r'D:\Documents\dataSets\listings.csv'
df = pd.read_csv(path)

# DF Head
df.info()
```
