import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.losses import Huber
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split


def min_pred(data, time_steps=10, epochs=400, batch_size=32):
    # تقسیم داده به دو بخش آموزش و تست
    train_data, test_data = train_test_split(data, test_size=0.2, shuffle=False)

    df_train = pd.DataFrame(train_data, columns=['Temperature'])
    df_test = pd.DataFrame(test_data, columns=['Temperature'])

    temperature_train = df_train['Temperature'].values.reshape(-1, 1)
    temperature_test = df_test['Temperature'].values.reshape(-1, 1)

    # استانداردسازی داده
    scaler = MinMaxScaler()
    temperature_train_scaled = scaler.fit_transform(temperature_train)
    temperature_test_scaled = scaler.transform(temperature_test)

    # ساخت داده‌های ورودی و خروجی برای مدل
    X_train, Y_min_train = [], []
    for i in range(len(temperature_train_scaled) - time_steps):
        X_train.append(temperature_train_scaled[i:(i + time_steps), 0])
        Y_min_train.append(np.min(temperature_train_scaled[i + 1:i + time_steps + 1, 0]))

    X_train, Y_min_train = np.array(X_train), np.array(Y_min_train)
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))

    X_test, Y_min_test = [], []
    for i in range(len(temperature_test_scaled) - time_steps):
        X_test.append(temperature_test_scaled[i:(i + time_steps), 0])
        Y_min_test.append(np.min(temperature_test_scaled[i + 1:i + time_steps + 1, 0]))

    X_test, Y_min_test = np.array(X_test), np.array(Y_min_test)
    X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

    # ساخت مدل
    min_model = Sequential()
    min_model.add(LSTM(150, input_shape=(time_steps, 1), return_sequences=True))
    min_model.add(Dropout(0.2))
    min_model.add(LSTM(75, return_sequences=True))
    min_model.add(Dropout(0.2))
    min_model.add(LSTM(50))
    min_model.add(Dense(1, activation='linear'))
    min_model.compile(optimizer=Adam(), loss=Huber())
    min_model.fit(X_train, Y_min_train, epochs=epochs, batch_size=batch_size, verbose=2)

    # پیش‌بینی مینیمم دما بر روی داده‌های تست
    future_min_temperature = min_model.predict(X_test)
    future_min_temperature = scaler.inverse_transform(future_min_temperature)

    # محاسبه درصد درستی پیش‌بینی
    actual_min_temperature = np.min(temperature_test[-time_steps:])
    accuracy = 100 * (1 - np.abs(future_min_temperature - actual_min_temperature) / actual_min_temperature)
    print("Accuracy min: {:.2f}%".format(np.mean(accuracy)))

    return float(f'{float(future_min_temperature[0]):.2f}')
