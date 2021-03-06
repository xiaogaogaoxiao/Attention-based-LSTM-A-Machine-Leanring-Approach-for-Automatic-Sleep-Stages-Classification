from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.recurrent import LSTM
from keras.layers.recurrent import GRU
from keras.optimizers import Adam
from keras.optimizers import SGD
from keras.optimizers import RMSprop
from keras.utils.np_utils import to_categorical
from sklearn.preprocessing import MinMaxScaler
from keras.callbacks import EarlyStopping
from keras.layers import Flatten
from keras.models import Model
from sklearn.metrics import confusion_matrix
from keras.layers.normalization import BatchNormalization
from keras.callbacks import ModelCheckpoint
from sklearn.model_selection import KFold

import seq2seq
from seq2seq.models import AttentionSeq2Seq

import numpy as np
import pandas as pd

from sklearn.cross_validation import train_test_split
from sklearn.model_selection import KFold
from sklearn.utils import class_weight



filepath=unicode('/mnt/nas/eeg/processed_data_Dream/','utf8')
print filepath
import os
fileName = sorted(os.listdir(filepath))
len(fileName)


print fileName


def encode1(label):
    for i in range(label.shape[0]):
        if label[i] == "W":
            label[i] = 0
        elif label[i] == "N1":
            label[i] = 1
        elif label[i] == "N2":
            label[i] = 1
        elif label[i] == "N3":
            label[i] = 1
        elif label[i] == "R":
            label[i] = 0
    return label
def encode2(label):
    for i in range(label.shape[0]):
        if label[i] == "W":
            label[i] = 0
        elif label[i] == "N1":
            label[i] = 1
        elif label[i] == "N2":
            label[i] = 2
        elif label[i] == "N3":
            label[i] = 3
        elif label[i] == "R":
            label[i] = 0
    return label
def encode3(label):
    for i in range(label.shape[0]):
        if label[i] == "W":
            label[i] = 0
        elif label[i] == "N1":
            label[i] = 1
        elif label[i] == "N2":
            label[i] = 2
        elif label[i] == "N3":
            label[i] = 3
        elif label[i] == "R":
            label[i] = 0
    return label
def encode4(label):
    for i in range(label.shape[0]):
        # if label[i] == "W":
        #     label[i] = 0
        # elif label[i] == "N1":
        #     label[i] = 1
        # elif label[i] == "N2":
        #     label[i] = 2
        # elif label[i] == "N3":
        #     label[i] = 3
        # elif label[i] == "R":
        #     label[i] = 4
        if label[i] == "5":
            label[i] = 0
        elif label[i] == "3":
            label[i] = 1
        elif label[i] == "2":
            label[i] = 2
        elif label[i] == "1":
            label[i] = 3
        elif label[i] == "4":
            label[i] = 4
    return label



# n_splits = 5
# kf = KFold(n_splits=n_splits, random_state=17, shuffle=True)
# for train_index, test_index in kf.split(fileName):
#     print("TRAIN:", train_index, "TEST:", test_index)
    
    
    
def create_model():
    model = Sequential()
    # model.add(LSTM(128,input_shape = (5,660), return_sequences = True, activation='tanh'))
#     model.add(LSTM(512, return_sequences=True, dropout=0.2, activation='tanh'))
#     model.add(LSTM(256, return_sequences=True, activation='tanh'))
    # model.add(LSTM(128, return_sequences=True, dropout=0.5, activation='tanh'))
#     model.add(LSTM(64, return_sequences=True, dropout=0.2, activation='tanh'))
    # model.add(LSTM(128, return_sequences=False, activation='tanh'))
    # model.add(GRU(128, input_shape = (5,660),return_sequences=True, activation='relu'))
    # model.add(GRU(128, input_shape = (30,770), return_sequences=True, activation='tanh'))
    # model.add(GRU(256, input_shape = (30,770), return_sequences=False, activation='tanh'))
#     model.add(GRU(128, input_shape = (6,1246), return_seqences=False, activation='relu'))

    model = AttentionSeq2Seq(input_dim=660, input_length=5*3, hidden_dim=64, 
                             output_length=1, output_dim=64, depth=(3,3), bidirectional=False)
    # model.add(Dropout(0.8))
     
    # model.add(Flatten())
#     model.add(Dense(128, activation='relu'))
    # model.add(Dense(64, activation='relu'))
    # model.add(Dense(5, activation='softmax'))
    
    a = model.inputs
    d0 = BatchNormalization()(model.outputs[-1])
    # drop = Dropout(0.5)(d0)
    d1 = Dense(5, activation='tanh')(d0)
    d2 = Dense(5, activation='softmax')(d1)
    model = Model(inputs=a, outputs=d2)
    
    sgd = SGD(lr=0.000001, decay=1e-8, momentum=0.9, nesterov=True)
    adam = Adam(lr = 0.00005, clipnorm = 4)
    rmsprop = RMSprop(lr=0.0007, rho=0.9, epsilon=None, decay=0.0)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    
    print model.summary()
    return model    
    
def mix(data):
    data.label = data.label.replace(np.nan, '?')
    train = data[data.label != '?']
    train = train[data.label != '0']
    train = train[data.label != '-1']
    train = train[data.label != '-2']
    train = train[data.label != '-3']
    train = train.replace([np.inf, -np.inf], np.nan)
    train = train.fillna(value = 0)
    train = np.array(train)
    # train = train.reshape(-1, 23101)
    train = train.reshape(-1, 3301)
    temp = train[::, :-1]
    temp_l = train[::,:-1]
    temp_r = train[::,:-1]
    temp_l[:-1,::] = temp[1:,::]
    temp_r[1:,::] = temp[:-1,::]
    temp = np.append(temp_l, temp, axis=1)
    temp = np.append(temp, temp_r, axis=1)
    label = train[1:-1,-1]
    temp = temp[1:-1,::]
    # train = train[::,:-1].reshape(-1,30,770)
    # temp = temp.reshape(-1,30,770)
    # temp = np.concatenate([temp,temp], axis=2)
    # temp = np.concatenate([temp,train], axis=2)
    # temp[:-1,::,:770] = train[:-1,::,::] - train[1:,::,::]
    # temp[1:,::,770:1540] = train[:-1,::,::] - train[1:,::,::]
    return temp, label


n_splits = 5
kf = KFold(n_splits=n_splits, random_state=17, shuffle=True)
fold = 0

matrix = np.array([])
acc_final = np.array([])
filepath1=unicode('/mnt/nas/eeg/processed_data_Dream/','utf8')

dataArr = np.array([])
labelArr = np.array([])
for i in range(len(fileName)):
    f = fileName[i]
    data = pd.read_pickle(filepath+f)
    print data.shape
    train,label = mix(data)
    print train.shape,label.shape
    dataArr = np.append(dataArr, train)
    labelArr = np.append(labelArr, label)
        
dataArr = dataArr.reshape(-1, 3300*3)
labelArr = labelArr.reshape(-1,1)

min_max_scaler = MinMaxScaler()
dataArr = min_max_scaler.fit_transform(dataArr)
dataArr = dataArr.astype("float16")
dataArr = dataArr.reshape(-1, 5*3, 660)
N_train = encode4(labelArr)
labelArr = to_categorical(labelArr)
labelArr = labelArr.reshape(-1, 1, 5)
# labelArr = labelArr.reshape(-1, 5)
    
for train_index, test_index in kf.split(dataArr):
    
    train, test = dataArr[train_index], dataArr[test_index]
    label_train, label_test = labelArr[train_index], labelArr[test_index]

    print train.shape, test.shape, label_train.shape, label_test.shape
    
    X_train, X_eval, Y_train, Y_eval = train_test_split(
                            train, label_train, test_size=0.1)
    print X_train.shape, X_eval.shape, Y_train.shape, Y_eval.shape
    

    print "trianing the model"

    model = create_model()
    
    check_point = ModelCheckpoint(filepath = 'check_point/weights.{epoch:02d}_{val_acc:.4f}.hdf5', 
                                  monitor = 'val_acc', verbose = 1, save_best_only = True)
    
#     class_w = class_weight.compute_class_weight('balanced', np.unique(Y_train), Y_train)
    model.fit(X_train, Y_train, batch_size=1024, epochs=200, verbose = True,
            shuffle=True, validation_data=(X_eval, Y_eval),callbacks=[check_point])
    score = model.evaluate(test, label_test, batch_size=1024)
    print score
    pred = model.predict(test, batch_size = 1024)
    model.reset_states()
    
    # for i in range(3):
    #     model.pop()
    
    del model
    
    acc_final = np.append(acc_final,score[1])
    print acc_final
    pred = pred.reshape(-1,5)
    pred = pred.argmax(axis=-1).reshape(-1,1).tolist()
    label_test = label_test.argmax(axis=-1).reshape(-1,1).tolist()

    matrix = np.append(matrix,confusion_matrix(label_test, pred))
    break

print acc_final
print acc_final.mean()
print matrix.reshape(-1,5,5)




    
