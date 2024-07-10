from __future__ import print_function
import numpy as np
from keras.datasets import reuters
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.text import Tokenizer

max_words = 1000  # vocab 大小
batch_size = 32  # mini_batch_size
nb_epoch = 5  # 大循环次数

print('Loading data...')
(X_train, y_train), (X_test, y_test) = reuters.load_data(num_words=max_words, test_split=0.2)  # 载入路透社语料 # 打印
print(len(X_train), 'train sequences')
print(len(X_test), 'test sequences')

# 分类数目--原版路透社我记着是 10 来着，应该是语料用的是大的那个
nb_classes = np.max(y_train) + 1
print(nb_classes, 'classes')

print('Vectorizing sequence data...')  # tokenize
tokenizer = Tokenizer(num_words=max_words)  # 序列化，取 df 前 1000 大 # 这里有个非常好玩的事， X_train 里面初始存的是 wordindex，wordindex 是按照词大小来的（应该是，因为直接就给撇了） # 所以这个效率上还是很高的 # 转化的还是 binary，默认不是用 tfidf
X_train = tokenizer.sequences_to_matrix(X_train, mode='binary')
X_test = tokenizer.sequences_to_matrix(X_test, mode='binary')
print('X_train shape:', X_train.shape)
print('X_test shape:', X_test.shape)

print('Convert class vector to binary class matrix (for use with categorical_crossentropy)')
Y_train = to_categorical(y_train, nb_classes)
Y_test = to_categorical(y_test, nb_classes)
print('Y_train shape:', Y_train.shape)
print('Y_test shape:', Y_test.shape)

print('Building model...')
model = Sequential()  # 第一层 # Dense 就是全连接层
model.add(Dense(512, input_shape=(max_words,)))  # 输入维度, 512 == 输出维度
model.add(Activation('relu'))  # 激活函数
model.add(Dropout(0.5))  # dropout  # 第二层
model.add(Dense(nb_classes))
model.add(Activation('softmax'))

# 损失函数设置、优化函数，衡量标准
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

# 训练，交叉验证
history = model.fit(X_train, Y_train,
                    epochs=nb_epoch, batch_size=batch_size,
                    verbose=1, validation_split=0.1)
score = model.evaluate(X_test, Y_test,
                       batch_size=batch_size, verbose=1)
print('\nTest score:', score[0])
print('Test accuracy:', score[1])
