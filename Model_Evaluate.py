## -*- encoding: utf-8 -*- ##
import datetime
import DC
import utils.DBUtils as DBUtils
import utils.utils as Utils
import utils.ModelUtils as ModelUtils

import traceback

def model_eva(stock, state_dt, para_window, para_dc_window):
    
    if DBUtils.select_ev_result(state_dt, stock) :
        print('Already ev:' + stock + ':' + state_dt)
        return 0
    
    # 建评估时间序列, para_window参数代表回测窗口长度

    ev_start = Utils.date2d((Utils.to_date(state_dt) -
                             datetime.timedelta(days=para_window)))
    ev_end = state_dt
    date_temp = DBUtils.get_stock_calender(ev_start,
                                            ev_end)
    ev_dt_seq = [(Utils.d2date(x)) for x in date_temp]

    # 清空评估用的中间表model_ev_mid
    DBUtils.clear_ev_mid()

    return_flag = 0
    # 开始回测，其中para_dc_window参数代表建模时数据预处理所需的时间窗长度
    for d in range(len(ev_dt_seq)):
        dc_start_dt = Utils.d2date(Utils.to_date(ev_dt_seq[d]) - datetime.timedelta(days=para_dc_window))
        dc_end_dt = ev_dt_seq[d]
        try:
            dc = DC.data_collect(stock, dc_start_dt, dc_end_dt)
            if len(set(dc.data_target)) <= 1:
                print('WARN: DC target is less than 1 record.')
                continue
        except Exception as exp:
            print("DC Error")
            print(exp)
            return_flag = 1
            break

        train = dc.data_train
        target = dc.data_target
        test_case = [dc.test_case]
        
        aresult = ModelUtils.use_svm(train, target, test_case)
       
        # 将预测结果插入到中间表
        DBUtils.insert_predict(dc_end_dt, stock, aresult)

    if return_flag == 1:
        print('WARN: something maybe wrong... when svm')
        acc = recall = acc_neg = f1 = 0
        return -1
    
    # 在中间表中刷真实值
    for i in range(len(ev_dt_seq)):
        r = DBUtils.update_ev_mid_with_real(stock, ev_dt_seq[i])
        if r != 0:
            print('WARN: break ev mid with real:' + stock)
            break

    # 计算查全率
    recall = DBUtils.count_recall()
    # 计算查准率
    acc = DBUtils.count_acc()
    # 计算查准率(负样本)
    acc_neg = DBUtils.count_acc_neg()
    # 计算 F1 分值
    f1 = Utils.count_F1(acc, recall)

    # 将评估结果存入结果表model_ev_resu中
    predict = DBUtils.get_predict(ev_dt_seq[-1])
    DBUtils.insert_ev_result(state_dt, stock, acc, recall, f1, acc_neg, 'svm',
                            predict)   
   
    print(str(state_dt) + '   Precision : ' + str(acc) + '   Recall : ' + str(recall) + '   F1 : ' + str(f1) + '   Acc_Neg : ' + str(acc_neg))
    
    return 1

if __name__ == '__main__':
    stock_pool = [Utils.stock_pool[0]]
    print('truncate model_ev_resu')
    DBUtils.truncate('model_ev_resu')
    for stock in stock_pool :
        ans = model_eva(stock,'2020-11-04',90,365)
    print('All Finished !!')

