#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from statsmodels.tools.eval_measures import rmse
from sklearn.preprocessing import MinMaxScaler
from keras.preprocessing.sequence import TimeseriesGenerator
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
import warnings

warnings.filterwarnings("ignore")
#path to the dataset
df = pd.read_csv("D://AI_Datasets//second.csv")


# In[3]:


df.head()


# In[4]:


df.Date = pd.to_datetime(df.Date)
df = df.set_index("Date")


# In[5]:


df.head()


# In[12]:



train, test = df[500:], df[:500]


# In[13]:


#defining the model
scaler = MinMaxScaler()
scaler.fit(train)
train = scaler.transform(train)
test = scaler.transform(test)


# In[14]:


n_input = 144
n_features = 1

generator = TimeseriesGenerator(train, train, length= n_input, batch_size = 20)

model = Sequential()
model.add(LSTM(200, activation = "relu", input_shape = (n_input, n_features)))
model.add(Dropout(0.15))
model.add(Dense(1))
model.compile(optimizer = "adam", loss = "mse", metrics=['accuracy'])

model.fit_generator(generator, epochs = 50)


# In[15]:


#making space for predictions
pred_list = []

batch = train[-n_input:].reshape((1,n_input, n_features))

for i in range(n_input):
    pred_list.append(model.predict(batch)[0])
    batch = np.append(batch[:, 1:,:],[[pred_list[i]]], axis=1)


# In[16]:


df_predict = pd.DataFrame(scaler.inverse_transform(pred_list), index = df[-n_input:].index, columns = ["Predictions"])
df_test = pd.concat([df, df_predict], axis =1)


# In[17]:


df_test.tail(145)
#df_test.to_csv("SoilHum1.csv")
df_test.tail()


# In[18]:


plt.figure(figsize =(20,5))
plt.plot(df_test.index, df_test[' Environment Humidity'])
plt.plot(df_test.index, df_test['Predictions'], color = "r")
#plt.savefig("EnvHum1.png")
plt.show()


# In[ ]:


train = df
scaler.fit(train)
train = scaler.transform(train)
n_input = 144
n_features = 1

generator = TimeseriesGenerator(train, train, length= n_input, batch_size = 20)

model.fit_generator(generator, epochs = 25)
pred_list = []

batch = train[-n_input:].reshape((1,n_input, n_features))

for i in range(n_input):
    pred_list.append(model.predict(batch)[0])
    batch = np.append(batch[:, 1:,:],[[pred_list[i]]], axis=1)


# In[6]:


from pandas.tseries.offsets import DateOffset
add_dates = [df.index[-2] + DateOffset(minutes = x) for x in range(0,1460,10)]
future_dates = pd.DataFrame(index = add_dates[2:], columns = df.columns)


# In[7]:


future_dates.tail()


# In[ ]:


df_predict = pd.DataFrame(scaler.inverse_transform(pred_list),index = future_dates[-n_input:].index, columns = ['Prediction'])
df_proj = pd.concat([df,df_predict], axis = 1)


# In[ ]:


df_proj.tail()
df_proj.to_csv("SoilHum2.csv")


# In[ ]:


plt.figure(figsize = (15,5))
plt.plot(df_proj.index, df_proj[' Soil Humidity'])
plt.plot(df_proj.index, df_proj['Prediction'],color="r")
#plt.legend(loc = "best", fontsize= "large")
plt.legend([df_proj[' Soil Humidity'],df_proj['Prediction']],["Environment Humidity","Prediction"])
plt.xticks(fontsize = 12)
plt.yticks(fontsize = 12)
#plt.savefig("EnvHum2.png")
plt.show()


# In[ ]:




