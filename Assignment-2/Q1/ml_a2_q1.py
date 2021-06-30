# -*- coding: utf-8 -*-
"""ML_A2_Q1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZuqounxG-HnVz0w2qPBFKUOC_YCv2BGS
"""

!pip install -U -q PyDrive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os
import joblib    #to save and load models
from sklearn.model_selection import train_test_split 
from random import seed
from random import randrange

"""# **Answer to Q1(a)**"""

data = drive.CreateFile({'id': '1xqNQ7sKImZFK2ydwnxYmrzUqGRkqcMy_'}) #https://drive.google.com/file/d/1xqNQ7sKImZFK2ydwnxYmrzUqGRkqcMy_/view?usp=sharing
data.GetContentFile('Dataset.data')
df = pd.read_csv('Dataset.data', skiprows=0, header=None, delimiter=' ', skip_blank_lines=True)

from google.colab import drive
drive.mount('/content/drive')
location = "/content/drive/My Drive/Colab Notebooks"
sys.path.append(os.path.abspath(location))
import Regression      #importing Regression.py as module to use Regression class

df

df[0]=pd.factorize(df[0])[0]+1
df

df.isnull().sum()

def nfold_split(data,num): #Here num is the number of splits to be done for the data
  chunk = list()
  dataset = data.values.tolist()
  fold_size = int(len(data)/num)
  for i in range(num):
    fold = list()
    while len(fold) < fold_size:
      index = randrange(len(dataset))
      fold.append(dataset.pop(index))
    chunk.append(fold)
  return chunk

"""# **Answer to Q1(b)**"""

from sklearn.metrics import mean_squared_error

LinReg = Regression.Regression()

joblib_file = "joblib_LinReg_Model.pkl"  
joblib.dump(LinReg, joblib_file)

seed(1)
chunks = nfold_split(df, 5)
y_pred = 0
MSE1 = []
MSE1sk = []
for i in range(5):
  df_train = pd.DataFrame()
  for j in range(5):
    if (j==i):
      df_test = pd.DataFrame(chunks[j])
    else:
      #train.append(chunks[j])
      data1 = pd.DataFrame()
      data1 = pd.DataFrame(chunks[j])
      df_train = df_train.append(data1, ignore_index=True)
  LinReg.fit(df_train.iloc[:,0:8], df_train.iloc[:,8:])
  y_pred = LinReg.predict(df_test.iloc[:,0:8])
  score = LinReg.calculate_MSE(df_test.iloc[:,8:], y_pred)
  score1 = mean_squared_error(df_test.iloc[:,8:], y_pred)
  MSE1.append(score)
  MSE1sk.append(score1)

MSE1 = np.array(MSE1).reshape(-1)   #MSE scores from regression class of Regression.py
MSE1

MSE_df = pd.DataFrame()
MSE_df['Validation_MSE'] = MSE1
MSE_df['Validation_MSE_sk'] = MSE1sk
MSE_df

seed(1)
chunks = nfold_split(df, 5)
y_pred = 0
MSE2 = []
MSE2sk = []
for i in range(5):
  df_train = pd.DataFrame()
  for j in range(5):
    if (j==i):
      df_test = pd.DataFrame(chunks[j])
    else:
      #train.append(chunks[j])
      data1 = pd.DataFrame()
      data1 = pd.DataFrame(chunks[j])
      df_train = df_train.append(data1, ignore_index=True)
  LinReg.fit(df_train.iloc[:,0:8], df_train.iloc[:,8:])
  y_pred = LinReg.predict(df_train.iloc[:,0:8])
  score = LinReg.calculate_MSE(df_train.iloc[:,8:], y_pred)
  score1 = mean_squared_error(df_train.iloc[:,8:], y_pred)
  MSE2.append(score)
  MSE2sk.append(score1)

MSE2 = np.array(MSE2).reshape(-1)   #MSE scores from regression class of Regression.py
MSE2

MSE_df['Training_MSE'] = MSE2
MSE_df['Training_MSE_sk'] = MSE2sk
MSE_df

#Mean MSE values by using Regression Class
print("Validation MSE: ",np.mean(MSE_df['Validation_MSE']))
print("Validation MSE (sklearn): ",np.mean(MSE_df['Validation_MSE_sk']))
print("Training MSE: ",np.mean(MSE_df['Training_MSE']))
print("Training MSE (sklearn): ",np.mean(MSE_df['Training_MSE_sk']))

"""# **Answer to Q1(c)**"""

#Using Normal Equations
seed(1)
chunks = nfold_split(df, 5)
y_pred = 0
MSE_nm1 = []
MSE1_nm1_sk = []
for i in range(5):
  df_train = pd.DataFrame()
  for j in range(5):
    if (j==i):
      df_test = pd.DataFrame(chunks[j])
    else:
      #train.append(chunks[j])
      data1 = pd.DataFrame()
      data1 = pd.DataFrame(chunks[j])
      df_train = df_train.append(data1, ignore_index=True)
  temp = np.ones((3340,1), dtype=int)
  temp1 = np.ones((835,1), dtype=int)
  X_train = np.array(df_train.iloc[:,0:8])
  X_train = np.concatenate((temp, X_train), axis=1)
  y_train = np.array(df_train.iloc[:,8:])
  X_test = np.array(df_test.iloc[:,0:8])
  X_test = np.concatenate((temp1, X_test), axis=1)
  y_test = np.array(df_test.iloc[:,8:])
  theta = np.linalg.inv(X_train.T.dot(X_train)).dot(X_train.T).dot(y_train)
  y_pred = X_test.dot(theta) 
  score = LinReg.calculate_MSE(y_test, y_pred)
  score1 = mean_squared_error(y_test, y_pred)
  MSE_nm1.append(score)
  MSE1_nm1_sk.append(score1)

MSE_nm1 = np.array(MSE_nm1).reshape(-1)   #MSE scores from normal equation
MSE_nm1

MSE_df_nm = pd.DataFrame()
MSE_df_nm['Validation_MSE'] = MSE_nm1
MSE_df_nm['Validation_MSE_sk'] = MSE1_nm1_sk
MSE_df_nm

#Using Normal Equations
seed(1)
chunks = nfold_split(df, 5)
y_pred = 0
MSE_nm2 = []
MSE_nm2_sk = []
for i in range(5):
  df_train = pd.DataFrame()
  for j in range(5):
    if (j==i):
      df_test = pd.DataFrame(chunks[j])
    else:
      #train.append(chunks[j])
      data1 = pd.DataFrame()
      data1 = pd.DataFrame(chunks[j])
      df_train = df_train.append(data1, ignore_index=True)
  temp = np.ones((3340,1), dtype=int)
  X_train = np.array(df_train.iloc[:,0:8])
  X_train = np.concatenate((temp, X_train), axis=1)
  y_train = np.array(df_train.iloc[:,8:])
  theta = np.linalg.inv(X_train.T.dot(X_train)).dot(X_train.T).dot(y_train)
  y_pred = X_train.dot(theta) 
  score = LinReg.calculate_MSE(y_train, y_pred)
  score1 = mean_squared_error(y_train, y_pred)
  MSE_nm2.append(score)
  MSE_nm2_sk.append(score1)

MSE_nm2 = np.array(MSE_nm2).reshape(-1)   #MSE scores from normal equation
MSE_nm2

MSE_df_nm['Training_MSE'] = MSE_nm2
MSE_df_nm['Training_MSE_sk'] = MSE_nm2_sk
MSE_df_nm

#Mean MSE values by using Normal Equation
print("Validation MSE: ",np.mean(MSE_df_nm['Validation_MSE']))
print("Validation MSE (sklearn): ",np.mean(MSE_df_nm['Validation_MSE_sk']))
print("Training MSE: ",np.mean(MSE_df_nm['Training_MSE']))
print("Training MSE (sklearn): ",np.mean(MSE_df_nm['Training_MSE_sk']))

"""# **Answer to Q1(d)**"""

from sklearn.linear_model import LinearRegression as lr

lr_model = lr()
seed(1)
chunks = nfold_split(df, 5)
y_pred = 0
MSE_sklearn1 = []
MSE_sklearn1_sk = []
for i in range(5):
  df_train = pd.DataFrame()
  for j in range(5):
    if (j==i):
      df_test = pd.DataFrame(chunks[j])
    else:
      #train.append(chunks[j])
      data1 = pd.DataFrame()
      data1 = pd.DataFrame(chunks[j])
      df_train = df_train.append(data1, ignore_index=True)
  X_train = np.array(df_train.iloc[:,0:8])
  y_train = np.array(df_train.iloc[:,8:])
  X_test = np.array(df_test.iloc[:,0:8])
  y_test = np.array(df_test.iloc[:,8:])
  lr_model.fit(X_train, y_train)
  y_pred = lr_model.predict(X_test)
  score = LinReg.calculate_MSE(y_test, y_pred)
  score1 = mean_squared_error(y_test, y_pred)
  MSE_sklearn1.append(score)
  MSE_sklearn1_sk.append(score1)

#MSE_sklearn1
MSE_sklearn1 = np.array(MSE_sklearn1).reshape(-1)   #MSE scores from regression using sklearn
MSE_sklearn1_sk

MSE_df_sk = pd.DataFrame()
MSE_df_sk['Validation_MSE'] = MSE_sklearn1
MSE_df_sk['Validation_MSE_sk'] = MSE_sklearn1_sk
MSE_df_sk

seed(1)
chunks = nfold_split(df, 5)
y_pred = 0
MSE_sklearn2 = []
MSE_sklearn2_sk = []
for i in range(5):
  df_train = pd.DataFrame()
  for j in range(5):
    if (j==i):
      df_test = pd.DataFrame(chunks[j])
    else:
      #train.append(chunks[j])
      data1 = pd.DataFrame()
      data1 = pd.DataFrame(chunks[j])
      df_train = df_train.append(data1, ignore_index=True)
  X_train = np.array(df_train.iloc[:,0:8])
  y_train = np.array(df_train.iloc[:,8:])
  lr_model.fit(X_train, y_train)
  y_pred = lr_model.predict(X_train)
  score = LinReg.calculate_MSE(y_train, y_pred)
  score1 = mean_squared_error(y_train, y_pred)
  MSE_sklearn2.append(score)
  MSE_sklearn2_sk.append(score1)

MSE_sklearn2 = np.array(MSE_sklearn2).reshape(-1)   #MSE scores from regression using sklearn
MSE_sklearn2

MSE_df_sk['Training_MSE'] = MSE_sklearn2
MSE_df_sk['Training_MSE_sk'] = MSE_sklearn2_sk
MSE_df_sk

#Mean MSE values by using sklearn Regression
print("Validation MSE: ",np.mean(MSE_df_sk['Validation_MSE']))
print("Validation MSE (sklearn): ",np.mean(MSE_df_sk['Validation_MSE_sk']))
print("Training MSE: ",np.mean(MSE_df_sk['Training_MSE']))
print("Training MSE (sklearn): ",np.mean(MSE_df_sk['Training_MSE_sk']))

