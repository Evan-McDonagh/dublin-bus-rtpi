#!/usr/bin/env python
# coding: utf-8

# In[229]:


from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.model_selection import cross_validate
from sklearn.model_selection import cross_val_score
from sklearn.tree import export_graphviz

import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[138]:


#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# ## Analysis of Random Sample of 1 million leavetimes merged with trips data

# In[2]:


df1 = pd.read_csv('../../data/leavetimes_trips_1e6.csv',sep=',')


# In[3]:


df1.head()


# In[139]:



# In[4]:


df1.drop('Unnamed: 0',axis=1,inplace=True)


# In[5]:


# dtypes 
df1['DATASOURCE'] = df1['DATASOURCE'].astype('category')
df1['DAYOFSERVICE'] = df1['DAYOFSERVICE'].astype('datetime64')
df1['TRIPID'] = df1['TRIPID'].astype('object')
df1['PROGRNUMBER'] = df1['PROGRNUMBER'].astype('category')
df1['STOPPOINTID'] = df1['STOPPOINTID'].astype('category')
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
df1['LINEID'] = df1['LINEID'].astype('category')


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
    'VEHICLEID',
    'PLANNEDTIME_DEP'
],axis=1)

# df1_simple.drop(['PROGNUMBER','TRIPID'],axis=1,inplace=True)

# In[17]:


df1_simple.head()


# In[18]:


df1_simple.dtypes


# In[24]:


df1_simple['MONTH'] = df1_simple['DAYOFSERVICE'].dt.month.astype('category')
df1_simple['WEEKDAY'] = df1_simple['DAYOFSERVICE'].dt.weekday.astype('category')
# df1_simple.drop('DAYOFSERVICE',axis=1,inplace=True)


# In[25]:


df1_simple.head()


# In[26]:


df1_simple.dtypes


# In[ ]:


# In[140]:


df1_simple.head()


# In[141]:


# df1_simple['ARR_DELTA'] = df1_simple['PLANNEDTIME_ARR'] - df1_simple['ACTUALTIME_ARR']
# df1_simple.drop('ACTUALTIME_ARR',axis=1,inplace=True)


# In[142]:


df1_simple.head()


# In[143]:


categorical_columns = df1_simple.select_dtypes('category').columns
df1_simple[categorical_columns].describe().T


# ### 

# ## 1 bus route

# In[303]:


route = '16'


# In[304]:


df1_simple_1route = df1_simple[df1_simple['LINEID'] == route]


# In[305]:


df1_simple_1route.shape[0]/130


# In[306]:


df1_simple_1route[categorical_columns].describe().T


# In[307]:


df1_simple_1route['lateness'] = df1_simple_1route['ACTUALTIME_ARR'] - df1_simple_1route['PLANNEDTIME_ARR']


# In[308]:


df1_simple_1route.head()


# In[309]:


hour = (df1_simple_1route['PLANNEDTIME_ARR']/(60*60)).astype('int64')
df1_simple_1route['Hour'] = hour
df1_simple_1route.groupby('Hour')['lateness'].mean().plot()
plt.ylabel('Lateness (s)')
plt.title('Average Lateness for 30,000 random %s arrivals'%route)
plt.savefig('%s_lateness.png'%route,dpi=720)


# In[301]:


df1_simple_1route.drop('LINEID',axis=1,inplace=True)
df_rev1 = pd.get_dummies(df1_simple_1route)


# In[302]:


continuous_columns = df_rev1.select_dtypes(include=['int64']).columns.tolist()
# remove the target "binary_outcome"
continuous_columns


# In[109]:


categorical_columns = df_rev1.select_dtypes(include=['uint8']).columns.tolist()
categorical_columns


# ## Train-test Split

# In[92]:


# y is the target
y = df_rev1["ACTUALTIME_ARR"]
# X is everything else
X = df_rev1.drop(["ACTUALTIME_ARR"],1)
# Split the dataset into two datasets: 70% training and 30% test
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1,  test_size=0.3)

print("original range is: ",df_rev1.shape[0])
print("training range (70%):\t rows 0 to", round(X_train.shape[0]))
print("test range (30%): \t rows", round(X_train.shape[0]), "to", round(X_train.shape[0]) + X_test.shape[0])


# In[69]:


# need to reset the index to allow contatenation with predicted values otherwise not joining on same index...
X_train.reset_index(drop=True, inplace=True)
y_train.reset_index(drop=True, inplace=True)
X_test.reset_index(drop=True, inplace=True)
y_test.reset_index(drop=True, inplace=True)
X_train.head(5)


# ## Linear Regression with 1 bus route

# In[70]:


# Train aka fit, a model using all continuous and categorical features.
multiple_linreg = LinearRegression().fit(X_train, y_train)


# In[71]:


# Print the weights learned for each feature.
print("\nFeatures are: \n", X_train.columns)
print("\nCoeficients are: \n", multiple_linreg.coef_)
print("\nIntercept is: \n", multiple_linreg.intercept_)
print("\nFeatures and coeficients: \n")#, list(zip(X_train.columns, multiple_linreg.coef_)))
for i in list(zip(X_train.columns,multiple_linreg.coef_)):
    print("{:e}".format(i[1]), i[0])


# In[72]:


# calculate the prediction and threshold the value. If >= 0.5 its true
multiple_linreg_predictions_train = multiple_linreg.predict(X_train)
actual_vs_predicted_multiplelinreg = pd.concat([y_train, pd.DataFrame(multiple_linreg_predictions_train, columns=['Predicted'])], axis=1)

print("\nUnthresholded predictions with multiple linear regression: \n")
print(actual_vs_predicted_multiplelinreg.head(10))
print()


# In[73]:


#This function is used repeatedly to compute all metrics
def printMetrics(testActualVal, predictions):
    #classification evaluation measures
    print('\n==============================================================================')
    print("MAE: ", metrics.mean_absolute_error(testActualVal, predictions))
    #print("MSE: ", metrics.mean_squared_error(testActualVal, predictions))
    print("RMSE: ", metrics.mean_squared_error(testActualVal, predictions)**0.5)
    print("R2: ", metrics.r2_score(testActualVal, predictions))


# In[74]:


printMetrics(y_train, multiple_linreg_predictions_train)


# In[75]:


# Predicted price on test set
test_predictions = multiple_linreg.predict(X_test)
print("Actual values of test:\n", y_test)
print("Predictions on test:", test_predictions)
printMetrics(y_test, test_predictions)


# In[76]:


#Timetabled Arrival Time
printMetrics(y_test, X_test['PLANNEDTIME_ARR'])


# In[ ]:





# ## SVM with one route

# from sklearn import svm
# 
# svr = svm.LinearSVR().fit(X_train,y_train)

# # calculate the prediction and threshold the value. If >= 0.5 its true
# svr_predictions_train = svr.predict(X_train)
# actual_vs_predicted_svr = pd.concat([y_train, pd.DataFrame(svr_predictions_train, columns=['Predicted'])], axis=1)
# 
# print("\nUnthresholded predictions with svr: \n")
# print(actual_vs_predicted_svr.head(10))
# print()

# printMetrics(y_train, svr_predictions_train)

# ## All Trips on 46A

# In[171]:


df1_simple_1route.head()


# In[170]:


TRIPIDs = df1_simple_1route['TRIPID'].unique()
# DAYS = df1_simple_1route['DAYOFSERVICE'].unique()
count = 0
for ID in TRIPIDs:
    DAYS = df1_simple_1route[df1_simple_1route['TRIPID'] == ID]['DAYOFSERVICE']
    for day in DAYS:
        print(day)
#         print(df1_simple[df1_simple['TRIPID'] == ID and df1_simple['DAYOFSERVICE'] == day].shape)


# In[ ]:




