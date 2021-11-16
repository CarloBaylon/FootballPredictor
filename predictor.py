from numpy import loadtxt
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from keras.utils.vis_utils import plot_model

dataset = loadtxt('pastnflseasonschedules.csv', delimiter=',')
# split data
X = dataset[:,0:7]
y = dataset[:,7]


# define the keras model
model = Sequential()
model.add(Dense(12, input_dim=7, activation='relu'))
model.add(Dense(7, activation='relu'))
model.add(Dense(1, activation='sigmoid'))


# compile the Keras model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])


# fit the keras model on the dataset
model.fit(X, y, epochs=40, batch_size=10)

# evaluate the keras model
_, accuracy = model.evaluate(X, y)
print('Accuracy: %.2f' % (accuracy*100))

# make class predictions with the model
predictions = (model.predict(X) > 0.5).astype(int)
# summarize first 20 cases
for i in range(20):
	print('%s => %d (expected %d)' % (X[i].tolist(), predictions[i], y[i]))
    

