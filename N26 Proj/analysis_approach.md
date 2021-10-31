# CASE STUDY - N26 # 

Agenda:

1. Python code implementation and analysis
2. Tableau Dashboards

## 1. Python Code Implementation and Analysis ## 

These are the points I will answer during the analysis:

1. Give an overview of our channels and how they contribute to user acquisition.
2. Estimate the impact of doubling TV spending
3. Make appropriate assumptions for the channel touchpoint cost. With your assumptions give recommendations how to
   change the budget allocation to maximize user acquisition with a constant budget

The data has been uploaded in Python and analysed for a higher level exploration.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Read Data
path = r'/Users/iuliano/Documents/Proj/N26'
tv_campaign = pd.read_csv(path + '/tv_campaigns.csv')
user_data = pd.read_csv(path + '/user_signup_data.csv')
pd.set_option('display.max_columns', 10)

# Data Understanding
print(tv_campaign.columns)
print(tv_campaign.shape)
print(tv_campaign.info)

print(user_data.columns)
print(user_data.shape)
print(user_data.info)

# Are userid unique?
print(user_data.userid.nunique() == len(user_data))
# Yes

# DO I have rows where none of the channels are 1 ?
user_data['totals'] = user_data.cpc + user_data.affiliate + user_data.social + user_data.organic
user_data[user_data.totals == 0]
# No, so I can assume that a row gets populated as long as a signup occurs


# Time period of sign up dates
print(user_data.signup_date.min())
print(user_data.signup_date.max())
# 4 Months Data
```

**Observations**:

1. Each row uniquely describe a userid conversion on one or multiple channels
2. The tv campaign runs on a single for multiple days in the time range given
3. Joining the two datasets could be a good idea to generate a flag on the rows where a tv campaign was active

```python
df = pd.merge(user_data, tv_campaign, left_on='signup_date', right_on='date', how='left')
df['date'].fillna(False, inplace=True)
df['date'] = df.date.map(lambda x: True if x != False else x)
df.rename(columns={'date': 'is_tv_campaign'}, inplace=True)
df.drop('campaign', axis=1, inplace=True)
df.head()

# Converting date obj into datetime
df['date'] = pd.to_datetime(df['signup_date'])
```

**Observations**:

1. A user can come through different channels but the data doesn't tell me which one is the entry and where the
   conversion occurs
2. I will first look at the percentage of conversions by channel to identify main drivers
3. I will then create a 'total' column that sums up the total amount of touch points by user to identify how many
   touchpoints are needed to maximise conversions

```python
# What is the channel that drove more conversions?
channel_share = round(user_data[['cpc', 'organic', 'affiliate', 'social']].sum() / len(user_data), 2) * 100
channel_share.sort_values(ascending=False).plot.bar(color=['tab:blue', 'tab:orange', 'tab:green', 'tab:purple'])
plt.title("Percentage of Channels Interactions prior Signup")
df['totals'] = df.cpc + df.affiliate + df.social + df.organic
```

Affiliate is the main driver followed by social

![share_of_channels](https://user-images.githubusercontent.com/73912794/139581735-0c06d93b-66ab-4b0b-ad0a-3614cfbeff9e.png)

<img width="500" alt="Screenshot 2021-10-28 at 19 48 27" src="https://user-images.githubusercontent.com/73912794/139581748-7b3b391a-9596-4aed-9cb7-030514bc0ef2.png">

```python
# Count user id grouped by total touchpoints
totals_grouped = df.groupby('totals', as_index=False)['userid'].count()
totals_grouped['percentage_of_totals'] = totals_grouped['userid'] / len(df)
totals_grouped = pd.DataFrame(totals_grouped)
totals_grouped = totals_grouped.rename(columns={'totals': '# Touch Points',
                                                'userid': 'Count Users',
                                                'percentage_of_totals': '% of Totals'})
totals_grouped
```

![Screenshot 2021-10-29 at 14 37 12](https://user-images.githubusercontent.com/73912794/139581780-32113ae2-c5cd-46a4-915c-64eb42e1f830.png)


**Findings**

1. 67% of users signed up through two touch points
2. 25% came through only one
3. Only 7% of them signed up when coming through three channels

I want to plot the conversions by channel for each touch point group to observe the different behaviours. 

```python
# Social Channel by Touch Points
fig, ax = plt.subplots()
ax.plot(one_ch.groupby('signup_date', as_index=False)['social'].sum()['signup_date'],
        one_ch.groupby('signup_date', as_index=False)['social'].sum()['social'], label='social: 1 Touch Point')
ax.legend()

ax.plot(two_ch.groupby('signup_date', as_index=False)['social'].sum()['signup_date'],
        two_ch.groupby('signup_date', as_index=False)['social'].sum()['social'], label='social: 2 Touch Points')
ax.legend()

ax.plot(three_ch.groupby('signup_date', as_index=False)['social'].sum()['signup_date'],
        three_ch.groupby('signup_date', as_index=False)['social'].sum()['social'], label='social: 3 Touch Points')
plt.xticks(rotation=90)
ax.legend()
ax.set_title('Social Conversions by Touch Point Groups')

# Affiliate Channel by Touch Points
fig, ax = plt.subplots()
ax.plot(one_ch.groupby('signup_date', as_index=False)['affiliate'].sum()['signup_date'],
        one_ch.groupby('signup_date', as_index=False)['affiliate'].sum()['affiliate'], label='Affiliate: 1 Touch Point')
ax.legend()

ax.plot(two_ch.groupby('signup_date', as_index=False)['affiliate'].sum()['signup_date'],
        two_ch.groupby('signup_date', as_index=False)['affiliate'].sum()['affiliate'],
        label='Affiliate: 2 Touch Points')
ax.legend()

ax.plot(three_ch.groupby('signup_date', as_index=False)['affiliate'].sum()['signup_date'],
        three_ch.groupby('signup_date', as_index=False)['affiliate'].sum()['affiliate'],
        label='Affiliate: 3 Touch Points')
plt.xticks(rotation=90)
ax.legend()
ax.set_title('Affiliate Conversions by Touch Point Groups')

# CPC Channel by Touch Points
fig, ax = plt.subplots()
ax.plot(one_ch.groupby('signup_date', as_index=False)['cpc'].sum()['signup_date'],
        one_ch.groupby('signup_date', as_index=False)['cpc'].sum()['cpc'], label='CPC: 1 Touch Point')
ax.legend()

ax.plot(two_ch.groupby('signup_date', as_index=False)['cpc'].sum()['signup_date'],
        two_ch.groupby('signup_date', as_index=False)['cpc'].sum()['cpc'],
        label='CPC: 2 Touch Points')
ax.legend()

ax.plot(three_ch.groupby('signup_date', as_index=False)['cpc'].sum()['signup_date'],
        three_ch.groupby('signup_date', as_index=False)['cpc'].sum()['cpc'],
        label='CPC: 3 Touch Points')
plt.xticks(rotation=90)
ax.legend()
ax.set_title('CPC Conversions by Touch Point Groups')

# Organic Channel by Touch Points
fig, ax = plt.subplots()
ax.plot(one_ch.groupby('signup_date', as_index=False)['organic'].sum()['signup_date'],
        one_ch.groupby('signup_date', as_index=False)['organic'].sum()['organic'], label='Organic: 1 Touch Point')
ax.legend()

ax.plot(two_ch.groupby('signup_date', as_index=False)['organic'].sum()['signup_date'],
        two_ch.groupby('signup_date', as_index=False)['organic'].sum()['organic'],
        label='Organic: 2 Touch Points')
ax.legend()

ax.plot(three_ch.groupby('signup_date', as_index=False)['organic'].sum()['signup_date'],
        three_ch.groupby('signup_date', as_index=False)['organic'].sum()['organic'],
        label='Organic: 3 Touch Points')
plt.xticks(rotation=90)
ax.legend()
ax.set_title('Organic Conversions by Touch Point Groups')
```
![social_conv_by_groups](https://user-images.githubusercontent.com/73912794/139581806-6b752881-6455-461f-b86a-2546067daa62.png)

![affiliate_conv_by_groups](https://user-images.githubusercontent.com/73912794/139581810-1414e125-8ec1-4835-a8d4-e85d14405c71.png)

![cpc_conv_by_group](https://user-images.githubusercontent.com/73912794/139581814-d1cb3feb-71d3-469b-a241-983dc26eeaae.png)

![organic_conv_by_group](https://user-images.githubusercontent.com/73912794/139581815-edc0aa31-e719-46ce-9dd5-a3247b41596b.png)


**Findings** 

1.All channels receive a significant increase when in pairs

2.Social channel has no conversions by itself but when paired with affiliate shows a significant increase

3.Organic show much fluctuation 

What are the most successful pairs?

```python
# Count userid by Concatenation of pairs
concat_grouped = df.groupby('concat', as_index=False)['userid'].count()
concat_grouped['percentage_of_total'] = round(concat_grouped['userid'] / len(df), 2)
concat_grouped.rename(columns={'concat': 'Pairs', 'userid': '# Users', 'percentage_of_total': '% of Total'}, inplace = True)
concat_grouped.sort_values(by = '# Users', ascending = False).plot.bar(x='Pairs', y='% of Total')
plt.title('Percentage of Conversions by Touch Point Pairs')
# Table
fig, ax = plt.subplots()
fig.patch.set_visible(False)
ax.axis('off')
ax.axis('tight')
plt.table(cellText = concat_grouped.sort_values(by = '# Users', ascending= False).values, colLabels = concat_grouped.columns,loc='center')
fig.tight_layout()
```

![pairs_bars](https://user-images.githubusercontent.com/73912794/139581825-ae290246-4ffd-4c33-8e55-25d779588899.png)

<img width="617" alt="pairs_t" src="https://user-images.githubusercontent.com/73912794/139581837-ca3f6680-211e-4540-a68d-b6bc48186e7d.png">


**Answer to Q1**
 
1. Conversions occur through cross-channel and can be clustered in 3 groups: 
   a. 1 Touch Point
   b. 2 Touch Points 
   c. 3 Touch Points
   
2. The 66% of all conversions occurred through 2 Touch points. In these cases, 40% of all conversions are attributable to Affiliate and Social channels. 
3. The second most successful pair was Affiliate and CPC with 10% conversions. 
4. Affiliate alone owns the 20% of all conversions

**Answer to Q3** 

1. Considering that the 67% of all conversions in the time period between Jan and Apr 2017 occurred through 2 Touch Points and only 7% through 3 Touch Points, 
**I'd suggest investing budget on a two-cross-channel strategy** to maximise conversions and minimise costs. 
2. The budget should be invested on Social and CPC which are the main channels increasing their conversions when working in pairs with Affiliate.


I will now measure the impact of TV Campaign on Conversions. 
I will calculate the average number of users per day and observe difference between days when tv campaign is on. 

```python
# What is the impact of tv spending on the conversions?
tv_campaign_yes = df[df.is_tv_campaign == True]
tv_campaign_no = df[df.is_tv_campaign == False]

avg_conv_tvc = round(tv_campaign_yes.userid.count() / tv_campaign_yes.signup_date.nunique(), 2)
avg_conv_tvc_no = round(tv_campaign_no.userid.count() / tv_campaign_no.signup_date.nunique(), 2)

avg_conv = pd.DataFrame({'TV Campaign T/F': [True, False],
                         'AVG Conversions Per Day': [avg_conv_tvc, avg_conv_tvc_no]})
fig, ax = plt.subplots()
fig.patch.set_visible(False)
ax.axis('off')
ax.axis('tight')
plt.table(cellText=avg_conv.values, colLabels=avg_conv.columns, loc='center')
fig.tight_layout()
```
![tv_campaign_impact](https://user-images.githubusercontent.com/73912794/139581851-df48cb33-60a5-4d84-b9b2-a30382a2b8fd.png)

**Answer to Q2** 

1. TV campaigns generates a +28% uplift on the average conversions per day. 
2. Assuming that these observations are not coming from the same distribution and that the difference is not given by chance, 
**we should expect ~ 550 * 2 conversions when doubling TV Costs**.

