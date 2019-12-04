import numpy as np
from random import randint
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import keras
from keras import backend as K
from keras.models import Sequential
from keras.layers import Activation
from keras.layers.core import Dense
from keras.optimizers import Adam
from keras.metrics import categorical_crossentropy
from keras.utils import to_categorical
import matplotlib.pyplot as plt
from keras.optimizers import SGD
set = pd.read_csv('NHL_DATA_FULL.csv')
set.head()
set = set.drop(['h_goals', 'a_goals'], axis=1)

y_binary = to_categorical(set['h_Won/Lost'], num_classes=2, dtype='int64')
train_labels = set.iloc[:,:1]
train_samples = set.iloc[:,1:]

scaler = MinMaxScaler()
train_samples = scaler.fit_transform(train_samples)
y = np.array(y_binary)
x = np.array(train_samples)
x = x[:, np.random.permutation(x.shape[1])]

model = Sequential()

model.add(Dense(16, input_shape=(82,), activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(2, activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)

model.compile( loss = "categorical_crossentropy", 
               optimizer = sgd, 
               metrics=['accuracy']
             )

model.fit(x, y, validation_split=0.2, batch_size=1, epochs=20)

data = pd.read_csv('NHL_DATA_TEST_PRED.csv')
test_binary = to_categorical(data['h_Won/Lost'], num_classes=2, dtype='int64')
data = data.drop(['h_goals', 'a_goals'], axis=1)
test_labels = data.iloc[:,:1]
test_samples = data.iloc[:,1:]
test_samples = scaler.fit_transform(test_samples)
test_label = np.array(test_binary)
test_sample = np.array(test_samples)
predicton = model.predict(test_sample, batch_size=1)
for i in predicton:
    print(i)
