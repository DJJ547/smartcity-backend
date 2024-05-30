from django.conf import settings
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from keras.models import load_model
import keras
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error

model = load_model('static/iot_model.h5')

def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        seq = data[i:(i + seq_length)]
        X.append(seq[:-1])
        y.append(seq[-1])

    return np.array(X), np.array(y)

#data has to be a 2d array, first column is the speed, second column is the flow
def predict(data):
    seq_length = 10
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)
    X, y = create_sequences(scaled_data, seq_length)
    X = np.reshape(X, (X.shape[0], X.shape[1], 2))
    y_pred = model.predict(X)
    y_pred_actual = scaler.inverse_transform(y_pred)
    return y_pred_actual

def predict_average(data):
    y_pred_actual = predict(data)
    return np.mean(y_pred_actual[:, 0]), np.mean(y_pred_actual[:, 1])

if __name__ == "__main__":
    data = pd.read_csv('./static/data/iots.txt', delimiter = "\t")
    data = data[['308511_speed', '308511_flow']].values
    y_pred_actual = predict(data)
    average = predict_average(data)
    print(average)