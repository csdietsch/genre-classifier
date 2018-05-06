# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 19:56:50 2018

@author: csdietsch and matt stone
"""


import numpy as np
import codecs
import tensorflow as tf
import keras
import pandas as pd
import matplotlib.pyplot as plt
hello = tf.constant('Hello, TensorFlow!') #test tensorflow
sess = tf.Session()
print(sess.run(hello))

#get dataset from the csv file
dataset = pd.read_csv('audio_features_no_alt_no_names.csv', sep=',', header=0, encoding='utf-8').as_matrix()
data = dataset[:,0:12]
target = dataset[:,13]

#one hot encode target
target = keras.utils.to_categorical(target, num_classes=4)

#separate training and validation data
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(data, target, test_size = 0.2)

#implementation of MLPClassifier
from sklearn.neural_network import MLPClassifier
classifier = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)

classifier.fit(X_train, y_train)
predictions = classifier.predict(X_test)
#for p in predictions:
	#print(p)

from sklearn.metrics import classification_report
print(classification_report(y_test,predictions))	

#implementation of our model
from keras.models import Sequential
from keras.layers import Dense, Dropout, MaxPooling1D

model = Sequential()
model.add(Dense(output_dim = 36, init = 'uniform', activation = 'sigmoid', input_dim = (12)))
model.add(Dense(output_dim = 36, init = 'uniform', activation = 'sigmoid'))
model.add(Dense(output_dim = 36, init = 'uniform', activation = 'sigmoid'))

model.add(Dense(output_dim = 4, init = 'uniform', activation = 'softmax'))

from keras import optimizers
#training model
adam = keras.optimizers.Adam(lr=0.0000001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
sgd = optimizers.SGD(lr=0.0000001, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(optimizer = 'sgd', loss = 'categorical_crossentropy', metrics = ['accuracy'])
history = model.fit(X_train, y_train, batch_size = 25, validation_data=(X_test, y_test), nb_epoch = 100)
print(history.history)
fig = plt.figure()
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')

plt.show()
fig.savefig('train.png');

fig2 = plt.figure()
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
fig2.savefig('train_loss.png');

#checking validation data
prediction = model.predict_classes(X_test)
#for p in prediction:
  # print(p)