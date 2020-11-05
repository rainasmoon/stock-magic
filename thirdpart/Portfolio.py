import numpy as np
import datetime
import copy
import DBUtils
import Utils

def count_sharp(a_list, b_list):
    sharp_temp = np.array(copy.copy(a_list)) * b_list
    sharp_exp = sharp_temp.mean()
    sharp_base = 0.04
    sharp_std = np.std(sharp_temp)
    if sharp_std == 0.00:
        sharp = 0.00
    else:
        sharp = (sharp_exp - sharp_base) / sharp_std

    return sharp

def count_cov(alist):
    return np.cov(np.array(alist).T)

def count_ans(acov):
    ans = np.linalg.eig(acov)
    # 求特征值和其对应的特征向量
    # 排序，特征向量中负数置0，非负数归一
    return ans

def count_ans_index(aans):
    ans_index = copy.copy(aans[0])
    ans_index.sort()

    return ans_index

def calculate(ans, ans_index, stock_matrix):

    resu = []
    
    print()
    print(ans_index)
    for k in range(len(ans_index)):
        one_case = []
        
        # risk
        one_case.append(ans_index[k])

        content_temp1 = ans[1][np.argwhere(ans[0] == ans_index[k])[0][0]]
        print(content_temp1)
        r_position = []
        position_sum = np.array([x for x in content_temp1 if x >= 0.00]).sum()
        
        for m in range(len(content_temp1)):
            if content_temp1[m] >= 0 and position_sum > 0:
                r_position.append(content_temp1[m]/position_sum)
            else:
                r_position.append(0.00)
        
        # position
        one_case.append(r_position)
        
        # 计算夏普率
        sharp = count_sharp(stock_matrix, r_position)

        # sharp
        one_case.append(sharp)
        resu.append(one_case)

    return resu


# 返回的resu中 特征值按由小到大排列，对应的是其特征向量
def get_portfolio(stock_list, state_dt, para_window):

    portfilio = stock_list

    # 建评估时间序列, para_window参数代表回测窗口长度
    model_test_date_start =Utils.to_date(state_dt) - datetime.timedelta(days=para_window)
    date_temp = DBUtils.get_stock_calender(model_test_date_start, state_dt)
    model_test_date_seq = [(Utils.d2date(x)) for x in date_temp]

    stock_matrix = []
    for i in range(len(model_test_date_seq)-4):
        
        ti = model_test_date_seq[i]
        ri = []
        
        for j in range(len(portfilio)):
            
            done_set = DBUtils.select_stock(portfilio[j],
                                            model_test_date_seq[i],
                                            model_test_date_seq[i+4] )
            
            temp = [x[3] for x in done_set]

            base_price = 0.00
            after_mean_price = 0.00
            
            if len(temp) <= 1:
                r = 0.00
            else:
                base_price = temp[0]
                after_mean_price = np.array(temp[1:]).mean()
                r = (float(after_mean_price/base_price)-1.00)*100.00
            ri.append(r)
        
            del done_set
            del temp
            del base_price
            del after_mean_price

        stock_matrix.append(ri)

    # 求协方差矩阵
    cov = count_cov(stock_matrix) 
    ans = count_ans(cov) 
    ans_index = count_ans_index(ans)

    resu = calculate(ans, ans_index, stock_matrix)

    return resu

if __name__ == '__main__':

    stocks = Utils.stock_pool
    results = get_portfolio(stocks, '2020-11-04', 90)

    print('**************  Market Trend  ****************')
    print('Risk : ' + str(round(results[0][0], 2)))
    print('Sharp ratio : ' + str(round(results[0][2], 2)))

    for i in range(5):
        print('----------------------------------------------')
        print('Stock_code : ' + str(stocks[i]) + '  Position : ' + str(round(results[0][1][i] * 100, 2)) + '%')
    
    print('----------------------------------------------')

    print('**************  Best Return  *****************')
    print('Risk : ' + str(round(results[1][0], 2)))
    print('Sharp ratio : ' + str(round(results[1][2], 2)))
    
    for j in range(5):
        print('----------------------------------------------')
        print('Stock_code : ' + str(stocks[j]) + '  Position : ' + str(
            round(results[1][1][j] * 100, 2)) + '%')
    
    print('----------------------------------------------')
