# -*- coding: utf-8 -*-
"""MLA1Q1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iq_YyIZ-_ppe1zx7wGCT85UtpgkGBJSl
"""

from google.colab import drive
drive.mount('/content/drive')

from scipy.io import loadmat
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import cv2
from sklearn.manifold import TSNE
import time
from mpl_toolkits import mplot3d 
from google.colab.patches import cv2_imshow

"""# **Answer to Question 1(a)**"""

S =loadmat('/content/drive/My Drive/ML(PG)_assignment_1/dataset_1.mat')
#print(S)

samplearr=S['samples'].reshape(-1,784)
data1=pd.DataFrame(samplearr)
labels=S['labels'].reshape(-1)
data1['labels']=labels
print(data1)

plt.figure(figsize=(10,10))
fig, ax = plt.subplots(10, 10,figsize=(20,20))
fig.subplots_adjust(hspace=0.5)
for j in range(10): 
   newdf = data1[data1['labels']==j]
   newdf = newdf.iloc[:, :784]
   arr = np.array(newdf.sample(n=10))
   arr2 = np.reshape(arr[j], (28, 28))
   for k in range(10):
     arr = np.array(newdf.sample(n=10))
     arr2 = np.reshape(arr[j], (28, 28))
     ax[j,k].imshow(arr2) #row=0, col=0
     ax[j,k].set_xlabel("class {}".format(j))   
plt.show()

"""# **Answer to Question 1(b)**"""

#/content/drive/My Drive/ML(PG)_assignment_1/dataset_2.mat
D = loadmat('/content/drive/My Drive/ML(PG)_assignment_1/dataset_2.mat')
print(D)

# samplearr=S['samples'].reshape(-1,784)
# data1=pd.DataFrame(samplearr)
# labels=S['labels'].reshape(-1)
# data1['labels']=labels
# print(data1)
samplesarr2 = D['samples']
data2 = pd.DataFrame(samplesarr2, columns=['a','b'])
labels2 = D['labels'].reshape(-1)
data2['labels'] = labels2
print(data2)

classes=list(data2['labels'].unique())
classes.sort()
print(classes)
classes= [str(i) for i in classes]
print(classes)

x=np.array(data2['a'])
y=np.array(data2['b'])
z=np.array(data2['labels'])

x,y,z

plt.figure(figsize=(10,8))
sc_plot=plt.scatter(x,y,c=z)
plt.title("Scatter plot on dataset_2.mat")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend(handles=sc_plot.legend_elements()[0],labels=classes)
plt.show()
#handles=sc_plot.legend_elements()[0],labels=classes

"""# **Answer to Question 1(c)**"""

time_start = time.time()
tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=250)
tsne_results = tsne.fit_transform(data1.iloc[:,:-1])
print('t-SNE done! Time elapsed: {} seconds'.format(time.time()-time_start))

tsne_df=pd.DataFrame(tsne_results,columns=['a','b'])
labels=data1['labels']
tsne_df['labels']=labels

#np.array(tsne_df['labels'].unique())
classes2=list(tsne_df['labels'].unique())
classes2.sort()
print(classes2)
classes2= [str(i) for i in classes2]
print(classes2)

#do it the same way as the graph just above tsne
#classes2 = np.array(tsne_df['labels'].unique().sort())
fig=plt.figure(figsize=(10,10))
sc_plt2=plt.scatter(np.array(tsne_df['a']),np.array(tsne_df['b']),marker='o',c=np.array(tsne_df['labels']))
plt.title('Scatter plot of TSNE Data')
plt.legend(handles = sc_plt2.legend_elements()[0],labels = classes2)
plt.xlabel('X')
plt.ylabel('Y')
plt.show()

"""# **Answer to Question 1(d)**"""

#3d plot
time_start = time.time()
tsne = TSNE(n_components=3, verbose=1, perplexity=30, n_iter=250)
tsne_results = tsne.fit_transform(data1.iloc[:,:-1])
print('t-SNE done! Time elapsed: {} seconds'.format(time.time()-time_start))

tsne_df=pd.DataFrame(tsne_results,columns=['a','b','c'])
labels=S['labels'][0].reshape(-1)
tsne_df['labels']=labels

x = np.array(tsne_df['a'])
y = np.array(tsne_df['c'])
z = np.array(tsne_df['c'])
fig=plt.figure(figsize=(15,10))
ax = plt.axes(projection ="3d") 
ax.scatter3D(x, y, z, c = np.array(tsne_df['labels']))
plt.title('3D Scatter plot of TSNE Data')
ax.set_xlabel('X-axis')  
ax.set_ylabel('Y-axis')  
ax.set_zlabel('Z-axis') 
plt.show()