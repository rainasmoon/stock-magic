# -*- coding:utf8 -*-
import numpy as np
import utils.DBUtils as DBUtils
import utils.utils as Utils

class data_collect(object):

    def __init__(self, in_code, start_dt, end_dt):
        ans = self.collectDATA(in_code, start_dt, end_dt)

    def __put_all_datas(self, i):
        return [self.open_list[i], self.close_list[i], self.high_list[i], self.low_list[i], self.vol_list[i], self.amount_list[i]]

    def __up(self, i):
        if self.close_list[i]/self.close_list[i-1] > (1.00 + Utils.DAY_WAVE):
            return 1
        elif self.close_list[i]/self.close_list[i-1] < (1.00 - Utils.DAY_WAVE):
            return Utils.MINUS 
        else:
            return 0

    def collectDATA(self, in_code, start_dt, end_dt):
        # 建立数据库连接，获取日线基础行情(开盘价，收盘价，最高价，最低价，成交量，成交额)
        done_set = DBUtils.select_stock(in_code, start_dt, end_dt)
        
        if len(done_set) == 0:
            print("empty data...")
            print('param: %s, %s, %s' %(in_code, start_dt, end_dt))
            raise Exception
        
        self.date_seq = []
        self.open_list = []
        self.close_list = []
        self.high_list = []
        self.low_list = []
        self.vol_list = []
        self.amount_list = []
        
        for i in range(len(done_set)):
            self.date_seq.append(done_set[i][0])
            self.open_list.append(float(done_set[i][2]))
            self.close_list.append(float(done_set[i][3]))
            self.high_list.append(float(done_set[i][4]))
            self.low_list.append(float(done_set[i][5]))
            self.vol_list.append(float(done_set[i][6]))
            self.amount_list.append(float(done_set[i][7]))
        
        # 将日线行情整合为训练集(其中self.train是输入集，self.target是输出集，self.test_case是end_dt那天的单条测试输入)
        self.data_train = []
        self.data_target = []
        self.data_target_onehot = []
        self.cnt_pos = 0
        self.test_case = []

        for i in range(1, len(self.close_list)):
            one_train_case = self.__put_all_datas(i-1)
            self.data_train.append(np.array(one_train_case))

            if self.__up(i) == 1:
                self.data_target.append(float(1.00))
                self.data_target_onehot.append([1,0,0])
            elif self.__up(i) == -1:
                self.data_target.append(float(-1.00))
                self.data_target_onehot.append([0,0,1])
            else:
                self.data_target.append(float(0.00))
                self.data_target_onehot.append([0,1,0])

        self.cnt_pos =len([x for x in self.data_target if x == 1.00])
        
        self.test_case = np.array([self.open_list[-1],self.close_list[-1],self.high_list[-1],self.low_list[-1],self.vol_list[-1],self.amount_list[-1]])
        
        self.data_train = np.array(self.data_train)
        self.data_target = np.array(self.data_target)

        return 1
