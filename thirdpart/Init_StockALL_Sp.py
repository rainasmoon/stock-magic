import datetime
import tushare as ts
import TSUtils
import DBUtils
import Utils

if __name__ == '__main__':

    # 设置tushare pro的token并获取连接
    pro = TSUtils.get_pro()
    # 设定获取日线行情的初始日期和终止日期，其中终止日期设定为昨天。
    start_dt = '20100101'
    time_temp = datetime.datetime.now() - datetime.timedelta(days=1)
    end_dt = time_temp.strftime('%Y%m%d')

    # 设定需要获取数据的股票池
    stock_pool = Utils.stock_pool
    total = len(stock_pool)
    # 循环获取单个股票的日线行情
    for i in range(len(stock_pool)):
        try:
            DBUtils.clear_stock()

            df = TSUtils.get_daily(stock_pool[i], start_dt, end_dt)
			# 打印进度
            print('Seq: ' + str(i+1) + ' of ' + str(total) + '   Code: ' + str(stock_pool[i]))
            c_len = df.shape[0]
        except Exception as aa:
            print(aa)
            print('No DATA Code: ' + str(i))
            continue
        for j in range(c_len):
            resu0 = list(df.iloc[c_len-1-j])
            resu = []
            for k in range(len(resu0)):
                if str(resu0[k]) == 'nan':
                    resu.append(-1)
                else:
                    resu.append(resu0[k])
            state_dt = (datetime.datetime.strptime(resu[1], "%Y%m%d")).strftime('%Y-%m-%d')
            try:
                DBUtils.insert_stock (state_dt,str(resu[0]),float(resu[2]),float(resu[5]),float(resu[3]),float(resu[4]),float(resu[9]),float(resu[10]),float(resu[6]),float(resu[7]),float(resu[8]))
            except Exception as err:
                print('ERR: insert error:' + err)
                continue
    print('All Finished!')
