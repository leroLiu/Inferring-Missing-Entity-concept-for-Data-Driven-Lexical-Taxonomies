# lis = []
# with open(r'C:\Users\zhouyuanfu\Desktop\train_data.txt','r',encoding='utf-8')as f,open(r'C:\Users\zhouyuanfu\Desktop\train_data(1).txt','w',encoding='utf-8')as f1:
#     for line in f.readlines():
#         lis.append(line)
#     lis = list(set(lis))
#     for item in lis:
#         f1.write(item)
#
# with open(r'C:\Users\zhouyuanfu\Desktop\complete.txt','r',encoding='utf-8')as f,open(r'C:\Users\zhouyuanfu\Desktop\complete(1).txt','w',encoding='utf-8')as f1:
#     for line in f.readlines():
#         item = line.strip().split('\t')
#         f1.write(item[0] + '\t' + item[5] + '\t' + item[1] + '\t' + item[2] + '\t' + item[3] + '\t' + item[4] + '\n')



import numpy as np
np.random.seed(1337)  # for reproducibility
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Activation, Convolution2D, MaxPooling2D, Flatten
from keras.optimizers import Adam
from sklearn.cross_validation import train_test_split
from keras.layers import BatchNormalization
from sklearn import cross_validation


data = np.loadtxt(r'C:\Users\zhouyuanfu\Desktop\vote_dataset(50).txt')
x, y = np.split(data, (6,), axis=1)
y = y.flatten()
x1, x2, y_train, y_test = cross_validation.train_test_split(x, y, test_size=0.2, random_state=0)
x_train, x_test = x1[:,1:], x2[:,1:]
print(str(x_train[:1,:]))
print(x_train.shape)
print(x_test.shape)

model = Sequential()

model.add(Dense(256, activation='relu',batch_input_shape=(None, 5)))
model.add(BatchNormalization())


model.add(Dense(32, activation='relu'))
model.add(BatchNormalization())

# Fully connected layer 2 to shape (10) for 10 classes
model.add(Dense(1))
model.add(Activation('sigmoid'))

# Another way to define your optimizer
adam = Adam(lr=1e-4)

# We add metrics to get more results you want to see
model.compile(optimizer=adam,
              loss='binary_crossentropy',
              metrics=['accuracy'])

print('Training ------------')
# Another way to train the model
model.fit(x_train, y_train, epochs=10, batch_size=128,)


print('\nTesting ------------')
# Evaluate the model with the metrics we defined earlier

result = model.predict(x_test)

print(len(result))
print(len(y_test))

count = 0
for i in range(len(result)):
    if result[i] >= 0.5:
        result[i] = 1
    else:
        result[i] = 0
for i in range(len(result)):
    if result[i] == y_test[i]:
        count += 1
print(count / len(result))

loss, accuracy = model.evaluate(x_test, y_test)

# print('\ntest loss: ', loss)
# print('\ntest accuracy: ', accuracy)


# data = np.loadtxt(r'C:\Users\zhouyuanfu\Desktop\complete(1).txt')
# x = data[:,1:]
# print(str(x[:1,:]))
# print(x.shape)
# result = model.predict(x)
# print(len(result))
# with open(r'C:\Users\zhouyuanfu\Desktop\com-right.txt','w') as ft,open(r'C:\Users\zhouyuanfu\Desktop\com-false.txt','w') as ff,open(r'C:\Users\zhouyuanfu\Desktop\com-dataset.txt','r') as fin:
#     lines = fin.readlines()
#     for i in range(len(result)):
#         buf = lines[i].strip().split('\t')
#         if result[i] >= 0.5:
#             ft.write(buf[0] + ',\t' + buf[1] + ',\t' + buf[2] + ',\t' + buf[3] + ',\t' + str(result[i]) + '\n')
#         else:
#             ff.write(buf[0] + ',\t' + buf[1] + ',\t' + buf[2] + ',\t' + buf[3] + ',\t' + str(result[i]) + '\n')
