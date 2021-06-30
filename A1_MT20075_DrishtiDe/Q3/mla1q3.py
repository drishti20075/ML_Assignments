# -*- coding: utf-8 -*-
"""MLA1Q3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17cdAjGSNIeqzbKR9uKMe20Y9j6ldakNN
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
import scipy.stats
import statistics
from sklearn.tree import DecisionTreeClassifier as dtc

data = drive.CreateFile({'id': '1Wnnp5B62JxZxM6TU5lZeL9LEwP1bpVn7'}) #https://drive.google.com/file/d/1Wnnp5B62JxZxM6TU5lZeL9LEwP1bpVn7/view?usp=sharing
data.GetContentFile('MLA1Q3data.csv')
data3 = pd.read_csv('MLA1Q3data.csv')

data3.fillna(value=data3['pm2.5'].mean(),inplace=True)
del data3['No']  #removing "No" column
del data3['year']
del data3['day']
del data3['hour']
data3['cbwd']=pd.factorize(data3['cbwd'])[0]+1  #converting "cbwd" string values to factors
data3

data3.isnull().sum()

def Train_Test_Split(df):
  train_size = int(0.8 * len(df))

  train_set = df[:train_size]
  test_set = df[train_size:]
  return train_set,test_set

X_train,X_test=Train_Test_Split(data3.iloc[:,1:])

y_train,y_test=Train_Test_Split(data3.iloc[:,:1])

"""# **Answer to Q3(a)**"""

#Using Gini-Index
cls=dtc(criterion='gini')
cls.fit(X_train,y_train)
y_pred=cls.predict(X_test)
y_test1=np.array(y_test)
y_test1 = (y_test1).reshape(-1)
df_confusion = pd.crosstab(y_test1, y_pred)
t_val=0
f_val=0
for i in range(1,13):
  for j in range(1,13):
    if i==j:
      t_val+=df_confusion[i][j]
    else:
      f_val+=df_confusion[i][j]
accuracy=t_val/(f_val+t_val)
accuracy

#Using Entropy
cls=dtc(criterion='entropy')
cls.fit(X_train,y_train)
y_pred=cls.predict(X_test)
y_test1=np.array(y_test)
y_test1 = (y_test1).reshape(-1)
df_confusion = pd.crosstab(y_test1, y_pred)
t_val=0
f_val=0
for i in range(1,13):
  for j in range(1,13):
    if i==j:
      t_val+=df_confusion[i][j]
    else:
      f_val+=df_confusion[i][j]
accuracy=t_val/(f_val+t_val)
accuracy

"""# **Answer to Q3(b)**"""

#testing accuracies
depths = [2,4,8,10,15,30]
accvals = []
for d in depths:
  cls=dtc(criterion='entropy',max_depth=d)
  cls=cls.fit(X_train,y_train)
  y_pred = cls.predict(X_test)
  y_test2 = np.array(y_test)
  y_test2 = (y_test2).reshape(-1)
  accuracy = np.sum(y_pred == y_test2)/len(y_pred)
  accvals.append(accuracy)
accvals

depths = [2,4,8,10,15,30]
table=np.vstack((depths, accvals)).T
table_df=pd.DataFrame(table,columns=["Depths","Testing_Accuracy"])
table_df

#training accuracies
depths = [2,4,8,10,15,30]
accvals2 = []
for d in depths:
  cls=dtc(criterion='entropy',max_depth=d)
  cls=cls.fit(X_train,y_train)
  y_pred2 = cls.predict(X_train)
  y_train2 = np.array(y_train)
  y_train2 = (y_train2).reshape(-1)
  accuracy = np.sum(y_pred2 == y_train2)/len(y_pred2)
  accvals2.append(accuracy)
accvals2

trainacc = pd.DataFrame(accvals2)
table_df['Training_Accuracy'] = trainacc 
table_df

plt.plot(table_df['Depths'],table_df['Testing_Accuracy'], label = 'Testing Accuracy')
plt.plot(table_df['Depths'],table_df['Training_Accuracy'], label = 'Training Accuracy')
plt.xlabel('Depths')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

"""# **Answer to Q3(c)**"""

sampdf = X_train.iloc[:,:8]
sampdf['month'] = y_train
sampdf

output = []
Xtrain_df = sampdf
for i in range(100):
    newdf = Xtrain_df.sample(frac=0.5, replace=True, random_state=1).reset_index(drop=True)
    X_train_new = newdf.drop('month',axis=1)
    y_train_new = newdf['month']
    cls1=dtc(criterion='entropy',max_depth=3)
    cls1=cls1.fit(X_train_new,y_train_new)
    output.append(cls1.predict(X_test))

majorityOutput = []
output = np.array(output)
temp = np.transpose(output)
#len(temp)
for i in range(temp.shape[0]):
    majorityOutput.append(statistics.mode(temp[i]))
    #np.bincount(temp[i]).argmax()

y_test_new = np.array(y_test)
y_test_new = (y_test_new).reshape(-1)
#len(y_test_new)
accuracy=np.sum(majorityOutput == y_test_new)/len(majorityOutput)
accuracy

"""# **Answer to Q3(d)**"""

def EnsembleMethod(tr,dp):   #tr for number of trees and dp for depth
    outputs = []
    for i in range(tr):
        newdf2 = sampdf.sample(frac=1)
        train_size = int(0.5 * len(newdf2))
        XTrain = newdf2.drop('month',axis=1)
        XTrain = X_train_new[:train_size]
        yTrain = newdf2['month']
        yTrain = y_train_new[:train_size]
        cls2 = dtc(criterion='entropy',max_depth=dp)
        cls2 = cls2.fit(XTrain,yTrain)
        outputs.append(cls2.predict(X_test))
    finalOutput = []
    temp2 = np.transpose(outputs)
    for i in range(temp2.shape[0]):
        finalOutput.append(np.bincount(temp2[i]).argmax())
    yTest = np.array(y_test)
    yTest = (yTest).reshape(-1)
    accuracy = np.sum(finalOutput == yTest)/len(finalOutput)
    return accuracy

depths = [4, 8, 10, 15, 20,30]
trees = [75,100,150,300,500,1000]
acc = []; tr = []; dp = []
for dep in depths:
    for t in trees:
        dp.append(dep)
        tr.append(t)
        accuracy = EnsembleMethod(t, dep)
        acc.append(accuracy)

Trees = pd.DataFrame(tr)
Depth = pd.DataFrame(dp)
Accuracy = pd.DataFrame(acc)
ensemble_df = pd.DataFrame(index = range(36))
ensemble_df['Depths'] = Depth
ensemble_df['Trees'] = Trees
ensemble_df['Testing_Accuracy'] = Accuracy
ensemble_df

def EnsembleMethod2(tr,dp):   #tr for number of trees and dp for depth
    outputs = []
    for i in range(tr):
        newdf2 = sampdf.sample(frac=1)
        train_size = int(0.5 * len(newdf2))
        XTrain = newdf2.drop('month',axis=1)
        XTrain = X_train_new[:train_size]
        yTrain = newdf2['month']
        yTrain = y_train_new[:train_size]
        cls2 = dtc(criterion='entropy',max_depth=dp)
        cls2 = cls2.fit(XTrain,yTrain)
        outputs.append(cls2.predict(X_train))
    finalOutput = []
    temp2 = np.transpose(outputs)
    for i in range(temp2.shape[0]):
        finalOutput.append(np.bincount(temp2[i]).argmax())
    yTest = np.array(y_train)
    yTest = (yTest).reshape(-1)
    accuracy = np.sum(finalOutput == yTest)/len(finalOutput)
    return accuracy

depths = [4, 8, 10, 15, 20,30]
trees = [75,100,150,300,500,1000]
acc2 = []; tr2 = []; dp2 = []
for dep in depths:
    for t in trees:
        dp2.append(dep)
        tr2.append(t)
        accuracy2 = EnsembleMethod2(t, dep)
        acc2.append(accuracy2)

ensemble_df['Training_Accuracy'] = pd.DataFrame(acc2)
ensemble_df

plt.plot(ensemble_df['Depths'],ensemble_df['Testing_Accuracy'], label = 'Testing Accuracy')
plt.plot(ensemble_df['Depths'],ensemble_df['Training_Accuracy'], label = 'Training Accuracy')
plt.xlabel('Depths')
plt.ylabel('Accuracy')
plt.legend()
plt.show()