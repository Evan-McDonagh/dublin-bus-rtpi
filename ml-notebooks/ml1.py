#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import mysql.connector


# In[2]:


os.environ


# In[3]:


conda list


# In[4]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sqlalchemy as sa
from sqlalchemy import create_engine
from sshtunnel import SSHTunnelForwarder
import pymysql


# In[2]:


filename = "../../data/rt_leavetimes_DB_2018.txt"
n = sum(1 for line in open(filename)) - 1 #number of records in file (excludes header)
s = 10000 #desired sample size
skip = sorted(random.sample(range(1,n+1),n-s)) #the 0-indexed header will not be included in the skip list
df = pandas.read_csv(filename, skiprows=skip)


# In[19]:


filename = "../../data/rt_leavetimes_DB_2018.txt"
df = pd.read_csv(filename,sep=";", nrows=10000000)


# In[23]:


df.head()


# In[14]:


i = 0
with open(filename) as file:  # the a opens it in append mode
    for line in file:
        i += 1


# In[15]:


print(i)


# In[18]:


engine = sa.create_engine('mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(USER,PASSWORD,URI,PORT,DB),echo=True)


# In[19]:


for res in engine.execute("SHOW VARIABLES;"):
    print(res)


# In[25]:


def connect_to_db():
    mydb = mysql.connector.connect(
        host = URI,
        user = USER + ":" + PORT,
        passwd=  PASSWORD,
        database = DB,
    )
    return mydb


# In[26]:


mydb = connect_to_db()


# In[4]:


pip install sshtunnel


# In[5]:


from config import *

def query_database(sql_statement):
    try:
        with SSHTunnelForwarder(
                (ssh_config['host'], ssh_config['port']),
                ssh_password=ssh_config['password'],
                ssh_username=ssh_config['user'],
                remote_bind_address=ssh_config['remote_bind_address']
        )as tunnel:
            try:
                connection = pymysql.connect(
                    host=database_config['host'],
                    user=database_config['user'],
                    passwd=database_config['password'],
                    db=database_config['database'],
                    port=tunnel.local_bind_port,
                    charset='utf8',
                    cursorclass=pymysql.cursors.DictCursor
                )
                cursor = connection.cursor()
                cursor.execute(sql_statement)
                connection.close()
                return cursor.fetchall()
            except Exception as e:
                print("pymysql failed!")
                print(e)
                print()
    # server.start()
    except Exception as e:
        print("ssh connection failed!")
        print(e)
        print()


# In[7]:


GET_STOPS = "SELECT * FROM dublinbus.stops limit 5;"
five_stops = query_database(GET_STOPS)
print(five_stops)


# In[ ]:


import time

time1 = time.time()
GET_JAN01 = "SELECT * FROM dublinbus.RT_LeaveTimes WHERE DAYOFSERVICE='01-JAN-18 00:00:00';"
JAN01 = query_database(GET_JAN01)

print(time.time() - time1)


# In[13]:





# In[ ]:




