# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 15:22:51 2021

@author: zuber
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import pickle

np.random.seed(10)
#%%
url=r'C:\Users\zuber\PycharmProjects\Dash,Plotly\08_case_study\datasets\data.csv'

df_raw=pd.read_csv(url,index_col=0)
#%%
cols=['Year','Fuel_Type','Transmission','Engine','Power','Seats','Price']

df=df_raw.copy()
df=df[cols]
#%%
df.Engine=df.Engine.str.split(' ').str[0]
df.Power=df.Power.str.split(' ').str[0].replace('null',np.nan)

df=df.dropna()

df.Engine=df.Engine.astype('float32')
df.Power=df.Power.astype('float32')

#%%
df=pd.get_dummies(df,drop_first=True)
#%%
df.to_csv('data_cleaned.csv')
#%%
X=df.copy()
y=X.pop('Price')
#%%
X_train,X_test,y_train,y_test=train_test_split(X,y)
#%%
reg=RandomForestRegressor()
reg.fit(X_train,y_train)

print(reg.score(X_test,y_test))
#%%

model=RandomForestRegressor()
param_grid=[{'max_depth':[3,4,5,6,7,8,10,20],
             'min_samples_leaf':[3,4,5,10,15]}]
gd=GridSearchCV(model,param_grid=param_grid,scoring='r2')
gd.fit(X_train,y_train)
#%%
print(gd.score(X_test,y_test))
#%%
model=gd.best_estimator_
#%%

with open('model.pickle','wb') as file:
    pickle.dump(model,file)
    
