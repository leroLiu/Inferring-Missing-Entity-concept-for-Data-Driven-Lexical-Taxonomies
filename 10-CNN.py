# please note, all tutorial code are running under python3.5.
# If you use the version like python2.7, please modify the code accordingly

#  CNN

# to try tensorflow, un-comment following two lines
# import os
# os.environ['KERAS_BACKEND']='tensorflow'

import numpy as np
np.random.seed(1337)  # for reproducibility
from keras.models import Sequential
from keras.layers import Dense, Activation, Convolution2D, MaxPooling2D, Flatten
from keras.optimizers import Adam
from sklearn.cross_validation import train_test_split
from keras.layers import BatchNormalization
import tensorflow as tf


gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.333)
sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))

dis = {}
with open(r'C:\Users\zhouyuanfu\Desktop\CNN_dataset(10).txt', 'r', encoding='utf-8')as f: #k
    row = 0
    for line in f.readlines():
        x = line.strip().split('\t')
        if x[0] in dis:
            dis[x[0]].append((x[1],x[2], x[3], x[4], x[5])) # x[4] & x[6]
        else:
            row += 1
            dis[x[0]] = [(x[1],x[2], x[3], x[4], x[5])] # x[4] & x[6]

lis1 = []
for i in range(row):
    lis2 = []
    for value in dis[str(i+1)]:
        lis3 = []
        for item in value:
            lis3.append(item)
        lis2.append(lis3)
    lis1.append(lis2)
x = np.array(lis1)
y1 = [0.0 for i in range(13827)]
y2 = [1.0 for i in range(14259)]
y = np.array(y2 + y1).flatten()
x1, x2, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
X_train = x1.reshape(-1, 1 , 10 , 5)   #7 -> 5 #k
X_test = x2.reshape(-1, 1 , 10 , 5)    #7 -> 5 #k
print(X_train.shape)
print(X_test.shape)

# Another way to build your CNN
model = Sequential()

# Conv layer 1 output shape (None, 10, 5)
model.add(Convolution2D(
    batch_input_shape=(None, 1, 10, 5), #7 -> 5 #k
    filters=4,
    kernel_size= 3,
    strides=2,
    padding='valid',                     # Padding method
    data_format='channels_first',
))
model.add(Activation('relu'))
# kernel_size = 3 -> 92.54%
# kernel_size = 5 -> 96.90%
model.add(MaxPooling2D(
    pool_size=1,
    strides=1,
    padding='valid',    # Padding method
    data_format='channels_first',
))
# model.add(BatchNormalization())


model.add(Convolution2D(2, (2,1), strides=2, padding='valid', data_format='channels_first'))
model.add(Activation('relu'))
model.add(MaxPooling2D(1,1, 'valid', data_format='channels_first'))
# model.add(BatchNormalization())

# Fully connected layer 1
model.add(Flatten())
model.add(Dense(8))
model.add(Activation('relu'))
# model.add(BatchNormalization())

model.add(Dense(4, activation='relu'))
# model.add(BatchNormalization())

# Fully connected layer 2
model.add(Dense(1))
model.add(Activation('sigmoid'))

# Another way to define your optimizer
adam = Adam(lr=1e-4)
# We add metrics to get more results you want to see
model.compile(optimizer=adam,
              loss='binary_crossentropy',
              metrics=['accuracy'])

model.summary()
print('Training ------------')
# Another way to train the model
model.fit(X_train, y_train, epochs=15, batch_size=64,)

print('\nTesting ------------')

result = model.predict(X_test)

print(len(result))
print(len(y_test))

count = 0                                       #手动测量
for i in range(len(result)):
    if result[i] >= 0.5:
        result[i] = 1
    else:
        result[i] = 0

TP = 0
FP = 0
TN = 0
FN = 0
for i in range(len(result)):
    if result[i] == y_test[i]:
        count += 1
        if result[i] == 1:
            TP += 1
        else:
            TN += 1
    else:
        if result[i] == 1:
            FP += 1
        else:
            FN += 1
print(count / len(result))
print('TP:' + str(TP))
print('TN:' + str(TN))
print('FP:' + str(FP))
print('FN:' + str(FN))

# Evaluate the model with the metrics we defined earlier
loss, accuracy = model.evaluate(X_test, y_test)

print('\ntest loss: ', loss)
print('\ntest accuracy: ', accuracy)
acc = (TP + TN)/(TP + TN + FP + FN)
pre = TP/(TP +FP)
recall = TP /(TP + FN)
F1 = (2 * pre * recall) / (pre + recall)
print('acc:' + str(acc))
print('pre:' + str(pre))
print('recall:' + str(recall))
print('F1:' + str(F1))