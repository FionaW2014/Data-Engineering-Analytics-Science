#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
pd.set_option('display.width', 700)
pd.set_option('display.max_columns', 13)


# In[ ]:


# read in csv
df_app = pd.read_csv("googleplaystore.csv")


# In[ ]:


print(list(df_app))   #return a list of all columns


# In[ ]:


print(df_app.head(50))


# In[ ]:


#drop column: Current Ver since it brings no value here
df_app = df_app.drop(['Current Ver'], axis = 1)


# In[ ]:


print(df_app.dtypes)    #display each column types


# In[ ]:


#sort dataframe by column: Category for optimization
df_app = df_app.sort_values(by=['Category','Rating'])


# In[ ]:


#coerce column: Reviews to integer, and exception becomes NaN
df_app['Reviews'] = pd.to_numeric(df_app['Reviews'], errors='coerce').fillna(0).astype(int)

#coerce column: Rating to float, and exception becomes NaN
df_app['Rating'] = pd.to_numeric(df_app['Rating'], errors='coerce').fillna(0).astype(float)


# In[ ]:


#returns range of review counts
print(min(df_app['Reviews']),max(df_app['Reviews']))


# In[ ]:


#filter out any apps (rows) that have fewer than 1,000 reviews
df_app = df_app.drop(df_app[  df_app['Reviews'] < 1000 ].index) 


# In[ ]:


#filter out any apps (rows) that have 0 or > 5 as rating
df_app = df_app.drop(df_app[  df_app['Rating'] == 0 ].index)
df_app = df_app.drop(df_app[  df_app['Rating'] > 5.0 ].index) 


# In[ ]:


print(df_app['Last Updated'][10473])   #regular format

print("Originally there are", len(df_app['Last Updated']),"rows.")  #total row count


# In[ ]:


#let's change column: Last Updated to Date

#try run the conventional way   df_app['Last Updated'] = pd.to_datetime(df_app['Last Updated'], format='%Y%m%d')
#This will return TypeError because here our Last Updated date objects formatted ' month dd, yyyy ' is not recognized 


#You can write your own function to address that:
get_ipython().run_line_magic('run', 'usastring_to_datetime.ipynb')

i = 0
date_updated = [0]*len(df_app['Last Updated'])
for each in df_app['Last Updated']:
    try:
        date_updated[i] = own_str_to_date(each)
        i+=1     
    except: 
        IndexError
        print(i, df_app['Last Updated'][i])
        df_app = df_app.drop(df_app.index[i])  #delete bad data row registered at 1.0.19
        df_app = df_app.reset_index()
        date_updated.pop(i)
        
        continue

print(len(df_app['Last Updated']))
df_app['Date Updated'] = date_updated


# In[ ]:


print(df_app['Date Updated'][5:10], df_app['Last Updated'][5:10])
#check if the new column: Date Updated transcribes correctly against column: Last Updated

print(df_app.dtypes)


# In[ ]:


#we are fine to drop the old column: Last Updated
df_app = df_app.drop(['Last Updated'], axis = 1)


#now let's look at what the first 50 rows of the dataframe is like
print(df_app.tail(15))
#df_app.tail(50) returns bottom 50 rowsdf_app = df_app.reset_index()


# In[ ]:


#we need to delete the $ sign from column: Price,
df_app['Price'] = df_app['Price'].str.replace('$', '')

#convert to numeric, 
df_app['Price'] = pd.to_numeric(df_app['Price'], errors='coerce').fillna(0).astype(float)

#and change column name to Price ($).
df_app.rename(columns = {'Price': 'Price ($)'}, inplace=True)

#returns range of price
print(min(df_app['Price ($)']), max(df_app['Price ($)']))

# In[ ]:


#WOW, APPS UP TO 400 BUCKS?!


# In[ ]:


df_app = df_app.reset_index()
print(df_app.tail(5))


# In[ ]:


'''
Your imaginary stakeholders might be saying to you:
"    Does Price affect consumer expectation, 
        Is expectation significantly different between App categories, 
            If there is, consumers purchasing what categories are less likely to be critical?
                What other correlations between these fields can you find? 
                    Can you create 1-3-5 visualization for management?"


The quantified questions will be:
    is there statistically significant difference on review scores depending whether the App being paid or free?
        is there statistically significant difference on review scores across App categories?
            If yes, present the distribution of review v.s. price, and find if correlation exists.
                Attempt scatter plot, trendline, and variability R^2 for other 
                
'''            


# In[ ]:


df_type_review = df_app[['Rating','Type','App']]
df_type_review['Std'] = df_app['Rating']
df_calc_typept = pd.pivot_table(df_type_review, values=['Rating','Std','App'], index=['Type'], 
                               aggfunc={'Rating':'mean', 'Std':np.std, 'App':'count'})



