## *-* encoding: utf-8 *-*

import ts_utils
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from pylab import mpl
import seaborn as sns
from sklearn import svm
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM

# 正常显示画图时出现的中文
# 这里使用微软雅黑字体
mpl.rcParams['font.sans-serif'] = ['SimHei']
# 画图时显示负号
mpl.rcParams['axes.unicode_minus'] = False

def draw_index(sh_index):
    mas = [21, 89]
    for ma in mas:
        col_name = 'ma' + str(ma)
        sh_index[col_name] = sh_index['close'].rolling(ma).mean()
    print(sh_index.tail())
    cols = ['close']
    for ma in mas:
        cols.append('ma' + str(ma))
    stock_mas = sh_index[cols]
    stock_mas.plot()
    plt.title('上证指数移动平均线')
    plt.show()

    stock_close = sh_index['close']
    
    stock_close.plot()
    plt.title('上证指数')
    plt.xlabel('日期')
    plt.ylabel('指数')
    plt.show()

    stock_close.hist(bins=100)
    plt.title('指数分布')
    plt.show()

    stock_close = stock_close.sort_values(ascending=True)
    stock_close = stock_close.reset_index(drop=True)
    stock_close.plot()
    plt.title('指数分布')
    plt.xlabel('天数')
    plt.ylabel('指数')
    plt.grid(True)
    plt.show()

    stock_vol = sh_index['volume']
    stock_vol.plot()
    plt.title('大盘成交量')
    plt.xlabel('日期')
    plt.ylabel('成交量')
    plt.show()

    stock_vol = stock_vol.sort_values(ascending = True)
    stock_vol = stock_vol.reset_index(drop=True)
    stock_vol.plot()
    plt.title('成交量分布')
    plt.xlabel('天数')
    plt.ylabel('成交量')
    plt.grid(True)
    plt.show()

    sns.jointplot('close', 'volume', sh_index, kind='scatter')
    plt.title('量价关系')
    plt.show()


    relationship = sh_index[['open', 'close', 'high', 'low', 'volume']]
    relationship = relationship.reset_index(drop=True)
    print(relationship.tail())

#    sns.pairplot(relationship)
#    plt.title('相关性分析')
#    plt.show()

def model_lstm(dt):
    dt = dt.reset_index() 
    dt = dt[['close']]
    myseriesdataset = dt.values
    l = len(myseriesdataset)
    totrain = myseriesdataset[0:l,:]
    tovalid = myseriesdataset[l:,:]
    #converting dataset into x_train and y_train
    scalerdata = MinMaxScaler(feature_range=(0, 1))
    scale_data = scalerdata.fit_transform(myseriesdataset)
    x_totrain, y_totrain = [], []
    length_of_totrain=len(totrain)
    for i in range(60,length_of_totrain):
        x_totrain.append(scale_data[i-60:i,0])
        y_totrain.append(scale_data[i,0])
    x_totrain, y_totrain = np.array(x_totrain), np.array(y_totrain)
    x_totrain = np.reshape(x_totrain, (x_totrain.shape[0],x_totrain.shape[1],1))
    
    #LSTM neural network
    lstm_model = Sequential()
    lstm_model.add(LSTM(units=50, return_sequences=True, input_shape=(x_totrain.shape[1],1)))
    lstm_model.add(LSTM(units=50))
    lstm_model.add(Dense(1))
    lstm_model.compile(loss='mean_squared_error', optimizer='adadelta')

    print('training...')
    lstm_model.fit(x_totrain, y_totrain, epochs=3, batch_size=1, verbose=2)
    print('yeah.')
    
    #predicting next data stock price
    myinputs = dt[len(dt) - (len(tovalid)+1) - 60:].values
    myinputs = myinputs.reshape(-1,1)
    myinputs  = scalerdata.transform(myinputs)
    tostore_test_result = []
    for i in range(60,myinputs.shape[0]):
        tostore_test_result.append(myinputs[i-60:i,0])
    tostore_test_result = np.array(tostore_test_result)
    tostore_test_result = np.reshape(tostore_test_result,(tostore_test_result.shape[0],tostore_test_result.shape[1],1))

    print('predict...')
    myclosing_priceresult = lstm_model.predict(tostore_test_result)
    print('yeah.')

    myclosing_priceresult = scalerdata.inverse_transform(myclosing_priceresult)
    
    print(len(tostore_test_result))
    print(myclosing_priceresult)

def model_svm(sh_index):
    relationship = sh_index[['open', 'close', 'high', 'low', 'volume']]

    train_datas = []
    target = []

    train_datas = relationship.to_numpy()

    for i in range(len(train_datas)-1):
        if train_datas[i+1][1]/train_datas[i][1] > 1:
            target.append(float(1.00))
        else:
            target.append(float(0.00))

    test_case = train_datas[-1].reshape(1, 5)
    train_datas = train_datas[:-1]

    model = svm.SVC(gamma = 'auto')
    model.fit(train_datas, target)
    ans2 = model.predict(test_case)

    print(test_case)
    print(ans2)

if __name__ == '__main__':
    print('hi...')
    sh_index = ts_utils.call_sh_index_v1()

    sh_index = sh_index.loc['2000-01-01':'2020-11-16']
   
    print(sh_index.tail())
    
    print(len(sh_index))

    model_lstm(sh_index)
