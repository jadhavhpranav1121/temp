#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# In[2]:


data = pd.read_csv('data.csv')
data


# In[3]:


likelihood = data['Likelihood']
likelihood.drop([0], axis = 0, inplace=True)
likelihood


# In[4]:


data = pd.read_csv('data.csv',usecols=[0,1,2,3,4,5,6,8,9])


# In[5]:


df = pd.DataFrame(data)
df


# In[6]:


df.rename(columns = {'crime':'crime_Violent','Unnamed: 9':'crime_NonViolent'},inplace=True)
df.drop([0], axis = 0, inplace=True)
df


# In[7]:


label_encoder = preprocessing.LabelEncoder()
df['Gender'] = label_encoder.fit_transform(df['Gender'])
df['Education'] = label_encoder.fit_transform(df['Education'])
df['Population'] = label_encoder.fit_transform(df['Population'])
df['Family_record'] = label_encoder.fit_transform(df['Family_record'])
df['Fin_status'] = label_encoder.fit_transform(df['Fin_status'])
df


# In[8]:


#train_test data split
x_train,x_test,y_train,y_test=train_test_split(df, likelihood, test_size=0.2, random_state=42)
y_train


# In[9]:


from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)


# In[10]:


y_test.shape


# # Passive Aggressive Classifier

# In[11]:


pac = PassiveAggressiveClassifier()
pac.fit(x_train,y_train)


# In[12]:


y_pred = pac.predict(x_test)
score = accuracy_score(y_test,y_pred)
print(f'Accuracy: {round(score*100,2)}%')


# # Random Forest

# In[13]:


classifier2 = RandomForestClassifier(n_estimators=3)
classifier2.fit(x_train,y_train)


# In[15]:


pred2 = classifier2.predict(x_test)
score = accuracy_score(y_test,pred2)
print(f'Accuracy: {round(score*100,2)}%')


# In[ ]:




