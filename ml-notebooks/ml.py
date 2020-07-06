#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# ## Analysis of Random Sample of 1 million leavetimes merged with trips data

# In[2]:


df1 = pd.read_csv('../../data/leavetimes_trips_1e6.csv',sep=',')


# In[3]:


df1.head()


# In[4]:


df1.drop('Unnamed: 0',axis=1,inplace=True)


# In[5]:


# dtypes 
df1['DATASOURCE'] = df1['DATASOURCE'].astype('category')
df1['DAYOFSERVICE'] = df1['DAYOFSERVICE'].astype('datetime64')
df1['TRIPID'] = df1['TRIPID'].astype('object')
df1['PROGRNUMBER'] = df1['PROGRNUMBER'].astype('object')
df1['STOPPOINTID'] = df1['STOPPOINTID'].astype('object')
df1['VEHICLEID'] = df1['VEHICLEID'].astype('object')
df1['SUPPRESSED_x'] = df1['SUPPRESSED_x'].astype('category')
df1['JUSTIFICATIONID_x'] = df1['JUSTIFICATIONID_x'].astype('category')
df1['DIRECTION'] = df1['DIRECTION'].astype('category')
df1['SUPPRESSED_y'] = df1['SUPPRESSED_y'].astype('category')
df1['JUSTIFICATIONID_y'] = df1['JUSTIFICATIONID_y'].astype('category')
df1['TENDERLOT'] = df1['TENDERLOT'].astype('category')
df1['NOTE_x'] = df1['NOTE_x'].astype('category')
df1['PASSENGERS'] = df1['PASSENGERS'].astype('category')
df1['PASSENGERSIN'] = df1['PASSENGERSIN'].astype('category')
df1['PASSENGERSOUT'] = df1['PASSENGERSOUT'].astype('category')
df1['DISTANCE'] = df1['DISTANCE'].astype('category')
df1['NOTE_y'] = df1['DISTANCE'].astype('category')
df1['LASTUPDATE_x'] = df1['LASTUPDATE_x'].astype('datetime64')
df1['LASTUPDATE_y'] = df1['LASTUPDATE_y'].astype('datetime64')
df1['BASIN'] = df1['BASIN'].astype('category')


# In[6]:


df1.dtypes


# In[7]:


categorical_columns = df1.select_dtypes('category').columns
numerical_columns = df1.select_dtypes('int64','float64').columns
object_columns = df1.select_dtypes('object').columns


# In[8]:


df1[categorical_columns].describe().T


# In[9]:


df1.drop(['PASSENGERS','PASSENGERSIN','PASSENGERSOUT','DISTANCE','NOTE_x'],axis=1,inplace=True)


# In[10]:


categorical_columns = df1.select_dtypes('category').columns


# In[11]:


df1[categorical_columns].describe().T


# In[12]:


df1.drop(['DATASOURCE','TENDERLOT','NOTE_y','BASIN','SUPPRESSED_y','JUSTIFICATIONID_y'],axis=1,inplace=True)


# In[13]:


categorical_columns = df1.select_dtypes('category').columns


# In[14]:


df1[categorical_columns].describe().T


# In[15]:


df1.head()


# In[16]:


df1_simple = df1.drop([
    'LASTUPDATE_y',
    'ROUTEID',
    'LASTUPDATE_x',
    'JUSTIFICATIONID_x',
    'SUPPRESSED_x',
    'ACTUALTIME_DEP',
    'TRIPID',
    'VEHICLEID',
    'PLANNEDTIME_DEP'
],axis=1)


# In[17]:


df1_simple.head()


# In[18]:


df1_simple.dtypes


# In[24]:


df1_simple['MONTH'] = df1_simple['DAYOFSERVICE'].dt.month.astype('category')
df1_simple['WEEKDAY'] = df1_simple['DAYOFSERVICE'].dt.weekday.astype('category')
df1_simple.drop('DAYOFSERVICE',axis=1,inplace=True)


# In[25]:


df1_simple.head()


# In[26]:


df1_simple.dtypes


# In[ ]:




