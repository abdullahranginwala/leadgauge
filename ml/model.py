import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score

np.set_printoptions(precision=3)

import clean
from clean import load_dataset, prepare_input, determining_cols # this is a code i will make and create a function in it
import pickle

X_train, X_test, y_train, y_test = load_dataset() # remove 'data' from here after checking

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

X_train[['TotalVisits','Total Time Spent on Website','Page Views Per Visit']] = scaler.fit_transform(X_train[['TotalVisits','Total Time Spent on Website','Page Views Per Visit']])
X_test[['TotalVisits','Total Time Spent on Website','Page Views Per Visit']] = scaler.transform(X_test[['TotalVisits','Total Time Spent on Website','Page Views Per Visit']])

X_train = pd.DataFrame.to_numpy(X_train)
y_train = pd.Series.to_numpy(y_train)
X_test = pd.DataFrame.to_numpy(X_test)
y_test = pd.Series.to_numpy(y_test) 

model = SGDClassifier(loss='log', max_iter=1000, random_state=2)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# using the test examples as test cases
 
pickle.dump(model, open('model.pkl', 'wb'))