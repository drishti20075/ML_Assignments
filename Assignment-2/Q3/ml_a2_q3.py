# -*- coding: utf-8 -*-
"""ML_A2_Q3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ir9I41E6inQ5jmMoWhCxjj2GvdTxpq7d
"""

import pandas as pd
import scipy.io
from random import seed
from random import randrange
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib    #to save and load models
import sys
import os

from google.colab import drive
drive.mount('/content/drive')

data = scipy.io.loadmat('/content/drive/My Drive/ML/Assignment_2_datasets/dataset_2.mat')
print(data)

data1 = data['samples']
df = pd.DataFrame(data1)
labels = data['labels'].reshape(-1)
df['labels'] = labels
df

"""# **Answer to Q3(a)**"""

x=np.array(df[0])
y=np.array(df[1])
z=np.array(df['labels'])

classes=list(df['labels'].unique())
classes.sort()
print(classes)
classes= [str(i) for i in classes]
print(classes)

plt.figure(figsize=(10,8))
sc_plot=plt.scatter(x,y,c=z)
plt.title("Scatter plot on dataset_2.mat")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend(handles=sc_plot.legend_elements()[0],labels=classes)
plt.show()

"""# **Answer to Q3(b)**

Multiclass Logistic Regression using One vs One (OVO) technique
"""

location = "/content/drive/My Drive/Colab Notebooks"
sys.path.append(os.path.abspath(location))
from LogRegression_OVO1 import LogRegression

from sklearn.metrics import accuracy_score

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

LogRegOVO = LogRegression()
joblib_file = "joblib_LogRegOVO_model.pkl"  
joblib.dump(LogRegOVO, joblib_file)

seed(1)
chunks = nfold_split(df, 5)
acc = []
acc_df_test = pd.DataFrame()
sample = []
for a in range(5):
    df_train = pd.DataFrame()
    for b in range(5):
        if (b==a):
          df_test = pd.DataFrame(chunks[b])
        else:
          #train.append(chunks[j])
          data1 = pd.DataFrame()
          data1 = pd.DataFrame(chunks[b])
          df_train = df_train.append(data1, ignore_index=True)
    #LogRegOVO = LogRegression()
    pairs = LogRegOVO.getPairs()
    acc_sk = []
    for [i,j] in pairs:                                                   #for df_train
        newdf = df_train[(df_train[2]==i) | (df_train[2]==j)]
        newdf = pd.DataFrame.reset_index(newdf)
        del newdf['index']
        X = newdf.iloc[:,0:2]
        train = X
        y = np.array(newdf.iloc[:,2:]).reshape(-1)
        for k in range(len(y)):
            if y[k] == i:
                y[k] = 1
            else:
                y[k] = 0
        #X = newdf.iloc[:,:2]
        y = pd.DataFrame(y)
        train[2] = y
        newdf1 = df_test[(df_test[2]==i) | (df_test[2]==j)]
        newdf1 = pd.DataFrame.reset_index(newdf1)
        del newdf1['index']
        X = newdf1.iloc[:,0:2]
        test = X
        y = np.array(newdf1.iloc[:,2:]).reshape(-1)
        for k in range(len(y)):
            if y[k] == i:
                y[k] = 1
            else:
                y[k] = 0
        X = newdf.iloc[:,:2]
        y = pd.DataFrame(y)
        test[2] = y
        X_train = train.iloc[:,0:2]
        y_train = train.iloc[:,2:]                                 #for df_test
        X_test = test.iloc[:,0:2]
        y_test = test.iloc[:,2:]
        LogRegOVO.fit(X_train, y_train)
        y_pred = LogRegOVO.predict(X_test)
        y_test = np.array(y_test).reshape(-1)
        accuracy = accuracy_score(y_test, y_pred) * 100
        acc_sk.append([a,i,j,accuracy])
        temp = pd.DataFrame()
        temp = temp.append(acc_sk) 
    acc_df_test = acc_df_test.append(temp,ignore_index=True)

acc_df_test.rename(columns = {0:'Sample No.',
                         1:'Class i',
                         2:'Class j',
                         3:'Accuracy'}, inplace = True) 
acc_df_test

final_accuracy = np.array(acc_df_test['Accuracy'])
final_accuracy = np.mean(final_accuracy)
final_accuracy

seed(1)
chunks = nfold_split(df, 5)
acc = []
acc_df_train = pd.DataFrame()
sample = []
for a in range(5):
    df_train = pd.DataFrame()
    for b in range(5):
        if (b==a):
          df_test = pd.DataFrame(chunks[b])
        else:
          #train.append(chunks[j])
          data1 = pd.DataFrame()
          data1 = pd.DataFrame(chunks[b])
          df_train = df_train.append(data1, ignore_index=True)
    LogRegOVO = LogRegression()
    pairs = LogRegOVO.getPairs()
    acc_sk = []
    for [i,j] in pairs:                                                   #for df_train
        newdf = df_train[(df_train[2]==i) | (df_train[2]==j)]
        newdf = pd.DataFrame.reset_index(newdf)
        del newdf['index']
        X = newdf.iloc[:,0:2]
        train = X
        y = np.array(newdf.iloc[:,2:]).reshape(-1)
        for k in range(len(y)):
            if y[k] == i:
                y[k] = 1
            else:
                y[k] = 0
        #X = newdf.iloc[:,:2]
        y = pd.DataFrame(y)
        train[2] = y
        X_train = train.iloc[:,0:2]
        y_train = train.iloc[:,2:]                                 #for df_test
        LogRegOVO.fit(X_train, y_train)
        y_pred = LogRegOVO.predict(X_train)
        y_train = np.array(y_train).reshape(-1)
        accuracy = accuracy_score(y_train, y_pred) * 100
        acc_sk.append([a,i,j,accuracy])
        temp = pd.DataFrame()
        temp = temp.append(acc_sk) 
    acc_df_train = acc_df_train.append(temp,ignore_index=True)

acc_df_train.rename(columns = {0:'Sample No.',
                         1:'Class i',
                         2:'Class j',
                         3:'Accuracy'}, inplace = True) 
acc_df_train

final_accuracy1 = np.array(acc_df_train['Accuracy'])
final_accuracy1 = np.mean(final_accuracy1)
final_accuracy1

"""# **Answer to Q3(c)**

Multiclass Logistic Regression using One vs Rest (OVR) technique
"""

location1 = "/content/drive/My Drive/ML/ML Code Classes"
sys.path.append(os.path.abspath(location1))
from LogRegression_OVR1 import LogRegression

LogRegOVR = LogRegression()
joblib_file = "joblib_LogRegOVR_Model.pkl"  
joblib.dump(LogRegOVR, joblib_file)

seed(1)
chunks = nfold_split(df, 5)
acc = []
acc_df1_test = pd.DataFrame()
sample = []
for a in range(5):
    df_train = pd.DataFrame()
    for b in range(5):
        if (b==a):
          df_test = pd.DataFrame(chunks[b])
        else:
          #train.append(chunks[j])
          data1 = pd.DataFrame()
          data1 = pd.DataFrame(chunks[b])
          df_train = df_train.append(data1, ignore_index=True)
    #LogRegOVR = LogRegression()
    acc_sk = []
    for i in np.sort(df_train[2].unique()):  
        j = int(i)                                                #for df_train
        newdf = pd.DataFrame.reset_index(df_train)
        del newdf['index']
        X = newdf.iloc[:,0:2]
        train = X
        y = np.array(newdf.iloc[:,2:]).reshape(-1)
        for k in range(len(y)):
            if y[k] == j:
                y[k] = 1
            else:
                y[k] = 0
        #X = newdf.iloc[:,:2]
        y = pd.DataFrame(y)
        train[2] = y
        newdf1 = pd.DataFrame.reset_index(df_test)
        del newdf1['index']
        X = newdf1.iloc[:,0:2]
        test = X
        y = np.array(newdf1.iloc[:,2:]).reshape(-1)
        for k in range(len(y)):
            if y[k] == j:
                y[k] = 1
            else:
                y[k] = 0
        X = newdf.iloc[:,:2]
        y = pd.DataFrame(y)
        test[2] = y
        X_train = train.iloc[:,0:2]
        y_train = train.iloc[:,2:]                                 #for df_test
        X_test = test.iloc[:,0:2]
        y_test = test.iloc[:,2:]
        LogRegOVR.fit(X_train, y_train)
        y_pred = LogRegOVR.predict(X_test)
        y_test = np.array(y_test).reshape(-1)
        accuracy = accuracy_score(y_test, y_pred) * 100
        acc_sk.append([a,j,accuracy])
        temp = pd.DataFrame()
        temp = temp.append(acc_sk) 
    acc_df1_test = acc_df1_test.append(temp,ignore_index=True)

acc_df1_test.rename(columns = {0:'Sample No.',
                         1:'Class Number',
                         2:'Accuracy'}, inplace = True) 
acc_df1_test.iloc[0:20]

final_accuracy2 = np.array(acc_df1_test['Accuracy'])
final_accuracy2 = np.mean(final_accuracy2)
final_accuracy2

seed(1)
chunks = nfold_split(df, 5)
acc = []
acc_df1_train = pd.DataFrame()
sample = []
for a in range(5):
    df_train = pd.DataFrame()
    for b in range(5):
        if (b==a):
          df_test = pd.DataFrame(chunks[b])
        else:
          #train.append(chunks[j])
          data1 = pd.DataFrame()
          data1 = pd.DataFrame(chunks[b])
          df_train = df_train.append(data1, ignore_index=True)
    LogRegOVR = LogRegression()
    acc_sk = []
    for i in np.sort(df_train[2].unique()):  
        j = int(i)                                                 #for df_train
        newdf = pd.DataFrame.reset_index(df_train)
        del newdf['index']
        X = newdf.iloc[:,0:2]
        train = X
        y = np.array(newdf.iloc[:,2:]).reshape(-1)
        for k in range(len(y)):
            if y[k] == j:
                y[k] = 1
            else:
                y[k] = 0
        #X = newdf.iloc[:,:2]
        y = pd.DataFrame(y)
        train[2] = y
        X_train = train.iloc[:,0:2]
        y_train = train.iloc[:,2:]                                 #for df_test
        LogRegOVR.fit(X_train, y_train)
        y_pred = LogRegOVR.predict(X_train)
        y_train = np.array(y_train).reshape(-1)
        accuracy = accuracy_score(y_train, y_pred) * 100
        acc_sk.append([a,j,accuracy])
        temp = pd.DataFrame()
        temp = temp.append(acc_sk) 
    acc_df1_train = acc_df1_train.append(temp,ignore_index=True)

acc_df1_train.rename(columns = {0:'Sample No.',
                         1:'Class Number',
                         2:'Accuracy'}, inplace = True) 
acc_df1_train

final_accuracy3 = np.array(acc_df1_train['Accuracy'])
final_accuracy3 = np.mean(final_accuracy3)
final_accuracy3

"""# **Answer to Q3(d)**

For OVO using sklearn
"""

from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsOneClassifier

seed(1)
chunks = nfold_split(df, 5)
#acc_dfsk_test = pd.DataFrame()
acc = []
sample = []
for a in range(5):
    df_train = pd.DataFrame()
    for b in range(5):
        if (b==a):
          df_test = pd.DataFrame(chunks[b])
        else:
          #train.append(chunks[j])
          data1 = pd.DataFrame()
          data1 = pd.DataFrame(chunks[b])
          df_train = df_train.append(data1, ignore_index=True)
    X_train = df_train.iloc[:,0:2]
    y_train = np.array(df_train.iloc[:,2:]).reshape(-1)
    X_test = df_test.iloc[:,0:2]
    y_test = df_test.iloc[:,2:]
    clf = OneVsOneClassifier(LogisticRegression(tol=0.0001, max_iter=1000)).fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    y_test = np.array(y_test).reshape(-1)
    accuracy = accuracy_score(y_test,y_pred)*100 
    acc.append([a,accuracy])

acc

acc_dfsk = pd.DataFrame(acc)
acc_dfsk.rename(columns = {0:'Fold Number',
                           1:'SkLearn_OVO_Test_Accuracy'}, inplace = True) 
acc_dfsk

np.mean(np.array(acc_dfsk['SkLearn_OVO_Test_Accuracy']))

seed(1)
chunks = nfold_split(df, 5)
#acc_dfsk_test = pd.DataFrame()
acc1 = []
sample = []
for a in range(5):
    df_train = pd.DataFrame()
    for b in range(5):
        if (b==a):
          df_test = pd.DataFrame(chunks[b])
        else:
          #train.append(chunks[j])
          data1 = pd.DataFrame()
          data1 = pd.DataFrame(chunks[b])
          df_train = df_train.append(data1, ignore_index=True)
    X_train = df_train.iloc[:,0:2]
    y_train = np.array(df_train.iloc[:,2:]).reshape(-1)
    clf = OneVsOneClassifier(LogisticRegression(tol=0.0001, max_iter=1000)).fit(X_train, y_train)
    y_pred = clf.predict(X_train)
    accuracy = accuracy_score(y_train,y_pred)*100 
    acc1.append([a,accuracy])

acc1

acc_dfsk_train = pd.DataFrame(acc1)
acc_dfsk_train.rename(columns = {0:'Fold Number',
                           1:'SkLearn_OVO_Train_Accuracy'}, inplace = True) 
acc_dfsk_train

np.mean(np.array(acc_dfsk_train['SkLearn_OVO_Train_Accuracy']))

"""For OVR using sklearn"""

from sklearn.multiclass import OneVsRestClassifier

seed(1)
chunks = nfold_split(df, 5)
#acc_dfsk_test = pd.DataFrame()
acc2 = []
sample = []
for a in range(5):
    df_train = pd.DataFrame()
    for b in range(5):
        if (b==a):
          df_test = pd.DataFrame(chunks[b])
        else:
          #train.append(chunks[j])
          data1 = pd.DataFrame()
          data1 = pd.DataFrame(chunks[b])
          df_train = df_train.append(data1, ignore_index=True)
    X_train = df_train.iloc[:,0:2]
    y_train = np.array(df_train.iloc[:,2:]).reshape(-1)
    X_test = df_test.iloc[:,0:2]
    y_test = df_test.iloc[:,2:]
    clf1 = OneVsRestClassifier(LogisticRegression(tol=0.0001, max_iter=1000)).fit(X_train, y_train)
    y_pred = clf1.predict(X_test)
    y_test = np.array(y_test).reshape(-1)
    accuracy = accuracy_score(y_test,y_pred)*100 
    acc2.append([a,accuracy])

acc2

acc_dfsk_OVR = pd.DataFrame(acc2)
acc_dfsk_OVR.rename(columns = {0:'Fold Number',
                           1:'SkLearn_OVR_Test_Accuracy'}, inplace = True) 
acc_dfsk_OVR

np.mean(np.array(acc_dfsk_OVR['SkLearn_OVR_Test_Accuracy']))

seed(1)
chunks = nfold_split(df, 5)
#acc_dfsk_test = pd.DataFrame()
acc3 = []
sample = []
for a in range(5):
    df_train = pd.DataFrame()
    for b in range(5):
        if (b==a):
          df_test = pd.DataFrame(chunks[b])
        else:
          #train.append(chunks[j])
          data1 = pd.DataFrame()
          data1 = pd.DataFrame(chunks[b])
          df_train = df_train.append(data1, ignore_index=True)
    X_train = df_train.iloc[:,0:2]
    y_train = np.array(df_train.iloc[:,2:]).reshape(-1)
    clf2 = OneVsRestClassifier(LogisticRegression(tol=0.0001, max_iter=1000)).fit(X_train, y_train)
    y_pred = clf2.predict(X_train)
    accuracy = accuracy_score(y_train,y_pred)*100 
    acc3.append([a,accuracy])

acc3

acc_dfsk_OVR_train = pd.DataFrame(acc3)
acc_dfsk_OVR_train.rename(columns = {0:'Fold Number',
                           1:'SkLearn_OVR_Train_Accuracy'}, inplace = True) 
acc_dfsk_OVR_train

np.mean(np.array(acc_dfsk_OVR_train['SkLearn_OVR_Train_Accuracy']))