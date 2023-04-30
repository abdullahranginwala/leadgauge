import pandas as pd
from sklearn.metrics import mean_squared_error
from datetime import datetime

training_data = pd.read_csv('training_data.csv')

drift_threshold = 0.05

incoming_data = pd.read_csv('incoming_data.csv')

mse = mean_squared_error(incoming_data, training_data)

if mse > drift_threshold:
    now = datetime.now()
    print(f"Data drift detected at {now}. Mean squared error: {mse}")
else:
    pass
