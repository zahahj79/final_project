import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping


def max_pred(data):
    # Function to preprocess the data
    def preprocess_data(data, time_steps):
        df = pd.DataFrame(data, columns=['Temperature'])
        temperature_data = df['Temperature'].values.reshape(-1, 1)

        scaler = MinMaxScaler()
        temperature_data_scaled = scaler.fit_transform(temperature_data)

        X, Y_max = [], []

        for i in range(len(temperature_data_scaled) - time_steps):
            X.append(temperature_data_scaled[i:(i + time_steps), 0])
            Y_max.append(np.max(temperature_data_scaled[i + 1:i + time_steps + 1, 0]))

        X, Y_max = np.array(X), np.array(Y_max)

        return X, Y_max, scaler

    # Preprocess the data for the LSTM algorithm
    real_temperature_data = data

    time_steps = 10
    epochs = 100

    # Preprocess data for the LSTM algorithm
    X, Y_max, scaler = preprocess_data(real_temperature_data, time_steps)

    # LSTM model structure
    model = Sequential()
    model.add(LSTM(256, input_shape=(time_steps, 1), return_sequences=True, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.4))
    model.add(LSTM(128, return_sequences=True, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.4))
    model.add(LSTM(64, return_sequences=True, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.4))
    model.add(LSTM(32, return_sequences=True, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.4))
    model.add(LSTM(16, activation='relu'))
    model.add(Dense(1, activation='linear'))
    model.add(BatchNormalization())
    model.compile(optimizer=Adam(learning_rate=0.01), loss=MeanSquaredError())

    # Callbacks for saving the best model and early stopping
    callbacks = [
        ModelCheckpoint(filepath='best_model.h5', monitor='val_loss', save_best_only=True),
        EarlyStopping(monitor='val_loss', patience=30, restore_best_weights=True)
    ]

    # Train the model
    model.fit(X, Y_max, epochs=epochs, batch_size=32, validation_split=0.1, callbacks=callbacks)

    # Make predictions
    X_test = X[-1:]
    X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))
    future_max_temperature = model.predict(X_test)
    future_max_temperature = scaler.inverse_transform(future_max_temperature)

    # Calculate accuracy
    actual_max_temperature = np.max(real_temperature_data[-time_steps:])
    accuracy = 100 * (1 - abs(future_max_temperature - actual_max_temperature) / actual_max_temperature)
    print(str(float(f'{float(accuracy):.2f}')) + '%')

    return float(f'{float(future_max_temperature):.2f}')
