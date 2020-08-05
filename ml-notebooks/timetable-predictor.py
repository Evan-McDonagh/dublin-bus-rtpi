#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np 
import pandas as pd


# In[7]:


trips = pd.read_csv('google_transit_dublinbus/trips.txt',sep=',')
stop_times = pd.read_csv('google_transit_dublinbus/stop_times.txt',sep=',')
routes = pd.read_csv('google_transit_dublinbus/routes.txt',sep=',')


# In[3]:


trips.head()


# In[4]:


stop_times.head()


# In[8]:


routes.head()


# In[9]:


df = stop_times.merge(trips,on='trip_id')


# In[10]:


df.head()


# In[11]:


df = df.merge(routes,on='route_id')


# In[12]:


df.head()


# In[13]:


df.shape


# In[23]:


df[df['trip_id'] == '10964.y1001.60-155-d12-1.94.I'][df['stop_sequence']==df['stop_sequence'].min()]


# In[29]:


df[df['trip_id'] == '10964.y1001.60-155-d12-1.94.I'][df['stop_sequence']==df['stop_sequence'].m()]


# In[27]:


df[df['trip_id'] == '10964.y1001.60-155-d12-1.94.I']['stop_sequence'].min()


# In[33]:


df_trip = df[df['trip_id'] == '10964.y1001.60-155-d12-1.94.I']
df_trip_max = df_trip[df_trip['stop_sequence'] == df_trip['stop_sequence'].max()]['arrival_time'].iloc[0]
df_trip_min = df_trip[df_trip['stop_sequence'] == df_trip['stop_sequence'].min()]['arrival_time'].iloc[0]
df_trip_min


# In[ ]:




