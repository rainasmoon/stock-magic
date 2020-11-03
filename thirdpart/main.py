import pymysql
import Model_Evaluate as ev
import Filter
import Portfolio as pf
from pylab import *
import Cap_Update_daily as cap_update
import DBUtils
import TSUtils
import Utils

if __name__ == '__main__':

    DBUtils.clear_db()
    DBUtils.init_stock_pool()

    date_seq_start = Utils.date_start
    date_seq_end = Utils.date_end
 
    # 建回测时间序列
    back_test_date_start = (datetime.datetime.strptime(date_seq_start, '%Y-%m-%d')).strftime('%Y%m%d')
    back_test_date_end = (datetime.datetime.strptime(date_seq_end, "%Y-%m-%d")).strftime('%Y%m%d')
    date_temp = TSUtils.get_stock_canlender(back_test_date_start, back_test_date_end)
    date_seq = [(datetime.datetime.strptime(x, "%Y%m%d")).strftime('%Y-%m-%d') for x in date_temp]
    print(date_seq)

    #开始模拟交易
    index = 1
    day_index = 0
    for i in range(1,len(date_seq)):
        day_index += 1
        # 每日推进式建模，并获取对下一个交易日的预测结果
        for stock in stock_pool:
            try:
                ans2 = ev.model_eva(stock,date_seq[i],90,365)
                # print('Date : ' + str(date_seq[i]) + ' Update : ' + str(stock))
            except Exception as ex:
                print('ERROR:' + ex)
                continue
        # 每5个交易日更新一次配仓比例
        if divmod(day_index+4,5)[1] == 0:
            portfolio_pool = stock_pool
            if len(portfolio_pool) < 5:
                print('Less than 5 stocks for portfolio!! state_dt : ' + str(date_seq[i]))
                continue
            pf_src = pf.get_portfolio(portfolio_pool, date_seq[i-1], Utils.year)
            # 取最佳收益方向的资产组合
            risk = pf_src[1][0]
            weight = pf_src[1][1]
            Filter.filter_main(portfolio_pool,date_seq[i],date_seq[i-1],weight)
        else:
            Filter.filter_main([],date_seq[i],date_seq[i - 1], [])
            cap_update_ans = cap_update.cap_update_daily(date_seq[i])
        print('Runnig to Date :  ' + str(date_seq[i]))
    print('ALL FINISHED!!')

    sharp,c_std = get_sharp_rate()
    print('Sharp Rate : ' + str(sharp))
    print('Risk Factor : ' + str(c_std))

    sql_show_btc = "select * from stock_index a where a.code = 'SH' and a.date>= '%s' and a.date <= '%s' order by date asc"%(date_seq_start,date_seq_end)
    cursor.execute(sql_show_btc)
    done_set_show_btc = cursor.fetchall()
    #btc_x = [x[0] for x in done_set_show_btc]
    btc_x = list(range(len(done_set_show_btc)))
    btc_y = [x[3] / done_set_show_btc[0][3] for x in done_set_show_btc]
    dict_anti_x = {}
    dict_x = {}
    for a in range(len(btc_x)):
        dict_anti_x[btc_x[a]] = done_set_show_btc[a][0]
        dict_x[done_set_show_btc[a][0]] = btc_x[a]

    #sql_show_profit = "select * from my_capital order by state_dt asc"
    sql_show_profit = "select max(a.capital),a.state_dt from my_capital a where a.state_dt is not null group by a.state_dt order by a.state_dt asc"
    cursor.execute(sql_show_profit)
    done_set_show_profit = cursor.fetchall()
    profit_x = [dict_x[x[1]] for x in done_set_show_profit]
    profit_y = [x[0] / done_set_show_profit[0][0] for x in done_set_show_profit]
    # 绘制收益率曲线（含大盘基准收益曲线）
    def c_fnx(val, poz):
        if val in dict_anti_x.keys():
            return dict_anti_x[val]
        else:
            return ''


    fig = plt.figure(figsize=(20, 12))
    ax = fig.add_subplot(111)
    ax.xaxis.set_major_formatter(FuncFormatter(c_fnx))

    plt.plot(btc_x, btc_y, color='blue')
    plt.plot(profit_x, profit_y, color='red')

    plt.show()

    cursor.close()
    db.close()

