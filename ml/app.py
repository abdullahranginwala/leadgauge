import pickle
from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
import requests
import json
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model
import clean
from sklearn.preprocessing import StandardScaler
from clean import prepare_input, load_dataset
import ast

app=Flask(__name__, template_folder='templates')

model = pickle.load(open('model.pkl', 'rb'))
scaler = StandardScaler()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['post'])
def predict():
    X_test = request.form.get('input')
    X_test = X_test.split(',')
    X_test = [ast.literal_eval(x) for x in X_test]
    
    X_train, _, _, y_test = load_dataset()
    
    X_train[['TotalVisits','Total Time Spent on Website','Page Views Per Visit']] = scaler.fit_transform(X_train[['TotalVisits','Total Time Spent on Website','Page Views Per Visit']])
    X_test[['TotalVisits','Total Time Spent on Website','Page Views Per Visit']] = scaler.transform(X_test[['TotalVisits','Total Time Spent on Website','Page Views Per Visit']])
    
    X_test = pd.DataFrame.to_numpy(X_test)
    
    predict = model.predict(X_test)
    return jsonify(predict)

if __name__ == '__main__':
    app.run()


