import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read data
company = pd.read_csv("/Users/marioiuliano/Playground/pricing/CaseStudy_Data/Company.csv", delimiter = ';')
contracts = pd.read_csv("/Users/marioiuliano/Playground/pricing/CaseStudy_Data/Contracts.csv", delimiter = ';')
user_postings = pd.read_csv("/Users/marioiuliano/Playground/pricing/CaseStudy_Data/User_Postings.csv", delimiter = ';')


# How many distinct companies?
# Total purchases by company? 
# Churned customers ? Total companies who did not renew after n date. Because min start date is dec 2021 and min end data is in 2022, we can't answer this question.  
# Which industry overall is the one that has the highest amount of employees? Potential market size
# Product distribution per industry ? 
# Distribution of product per region/city /industry .. sell to those with higher products distribution

data = [company,contracts, user_postings ]
for d in data: 
    _ = sns.displot(data = d.isna().melt(value_name = 'missing'), y = 'variable', hue = 'missing', multiple = 'fill', height= 5)
    plt.show()
    
# Check for data shape # 

print("Data shape for Company Data " , company.shape) 
print("Data shape for Contracts Data " , contracts.shape) 
print("Data shape for user_postings Data " , user_postings.shape) 


# User postins has 99% of null values for posting_id and created_at, meaning that we don't know when a posting has been published. 
# The min date for this data is 2023 meaning that these ads are planned to be run in the future.
# Although we don't know when most of the ads will run we can still know how many ads have been purchased by company and how many are already scheduled.
# How many user id a company contain


### Findings ### 

#There are 600 companies and 633 contracts. On average a company holds 1.5 contracts.

#User postings data contains created at in 2024, why?



# Inspect data types and null for Company Data
company.info()

# Convert date object into date

user_postings["CREATED_AT"] = pd.to_datetime(user_postings.CREATED_AT)
print("Min Date ", user_postings["CREATED_AT"].min())
print("Max Date ", user_postings["CREATED_AT"].max())

# Inspect data types and null for contracts Data
contracts.info()

# Is it possible that in this case we are only looking at fictious data with dates based in the future? 

# Convert date obj into dates
dates = ["START_DATE", "END_DATE"]
contracts[dates] = contracts[dates].apply(pd.to_datetime)


# Return max and min dates 

print("Min start date ", contracts.START_DATE.min())
print("Max start date ", contracts.START_DATE.max())
print("Min end date ", contracts.END_DATE.min())
print("Max end date ", contracts.END_DATE.max())


# For those with multiple contracts, which products do they have ? 
contracts_product = contracts.pivot_table(index = "COMPANY_ID", columns="PRODUCT", values= "CONTRACT_ID", aggfunc = 'count').reset_index()
contracts_product 


contracts_product.fillna(0, inplace=True)

contracts_product["total_prod"] = contracts_product.ABC + contracts_product.EBP + contracts_product.XTM 

contracts_product["ABC_text"] = contracts_product.ABC.apply(lambda x: 'ABC' if x == 1 else 0)
contracts_product["EBP_text"] = contracts_product.EBP.apply(lambda x: 'EBP' if x == 1 else 0)
contracts_product["XTM_text"] = contracts_product.XTM.apply(lambda x: 'XTM' if x == 1 else 0)


merge_test = contracts_product.merge(company, how ='left', left_on='COMPANY_ID', right_on="ID")


