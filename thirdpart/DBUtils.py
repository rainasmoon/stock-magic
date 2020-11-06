## encoding: utf-8 ##
import pymysql
import datetime
import Utils
from sqlalchemy import create_engine 
from pylab import np

def get_mysql_conn():
    return pymysql.connect(host='localhost', user='stock', passwd='stock',
                           db='stocks',
                           charset='utf8')
def get_engine():
    return create_engine('mysql://stock:stock@127.0.0.1:3306/stocks?charset=utf8&use_unicode=1')


def get_conn():
    return get_mysql_conn()

def truncate(table_name):
    db = get_conn()
    cursor = db.cursor()

    sql = 'truncate table ' + table_name
    cursor.execute(sql)
    
    db.commit();
    db.close();

def clear_db():
    db = get_conn()
    cursor = db.cursor()

    # 先清空之前的测试记录,并创建中间表
    sql_wash1 = 'delete from my_capital where seq != 1'
    cursor.execute(sql_wash1)

    sql_wash3 = 'truncate table my_stock_pool'
    cursor.execute(sql_wash3)

    # 清空行情源表，并插入相关股票的行情数据。该操作是为了提高回测计算速度而剔除行情表(stock_all)中的冗余数据。
    sql_wash4 = 'truncate table stock_info'
    cursor.execute(sql_wash4)
    db.commit()
    db.close()

def clear_stock():
    db = get_conn()
    cursor = db.cursor()
    sql = 'truncate table stock_all'
    cursor.execute(sql)
    db.commit()
    db.close()

def clear_ev_mid():
    db = get_conn()
    cursor = db.cursor()
    sql_truncate_model_test = 'truncate table model_ev_mid'
    cursor.execute(sql_truncate_model_test)
    db.commit()
    db.close()


def init_stock_pool():
    db = get_conn()
    cursor = db.cursor()
    stock_pool = Utils.stock_pool
    
    in_str = '('
    for x in range(len(stock_pool)):
        if x != len(stock_pool)-1:
            in_str += str('\'') + str(stock_pool[x])+str('\',')
        else:
            in_str += str('\'') + str(stock_pool[x]) + str('\')')
    
    sql_insert = "insert into stock_info(select * from stock_all a where a.stock_code in %s)"%(in_str)
    cursor.execute(sql_insert)
    db.commit()
    db.close()


def select_stock_info(opdate, stock_code):
    db = get_conn()
    cursor = db.cursor()

    sql_buy = "select * from stock_info a where a.state_dt = '%s' and a.stock_code = '%s'" % (opdate, stock_code)
    cursor.execute(sql_buy)
    done_set_buy = cursor.fetchall()

    db.commit()
    db.close()

    return done_set_buy


def insert_stock(state_dt,stock_code,open_price,close,high,low,vol,amount,pre_close,amt_change,pct_change):
    db = get_conn()
    cursor = db.cursor()

    sql_insert = "INSERT INTO stock_all(state_dt,stock_code,open,close,high,low,vol,amount,pre_close,amt_change,pct_change) VALUES ('%s', '%s', '%.2f', '%.2f','%.2f','%.2f','%i','%.2f','%.2f','%.2f','%.2f')" % (state_dt,stock_code,open_price,close,high,low,vol,amount,pre_close,amt_change,pct_change) 
    cursor.execute(sql_insert)
    db.commit()


def select_stock(stock, start_dt, end_dt):
    db = get_conn()
    cursor = db.cursor()
    sql_done_set = "SELECT * FROM stock_all a where stock_code = '%s' and state_dt >= '%s' and state_dt <= '%s' order by state_dt asc" % (stock , start_dt, end_dt)
    cursor.execute(sql_done_set)
    done_set = cursor.fetchall()

    db.commit()
    db.close()
    
    return done_set


def select_my_capital():    
    db = get_conn()
    cursor = db.cursor()

    sql_cap = "select * from my_capital a order by seq asc"
    cursor.execute(sql_cap)
    done_exp = cursor.fetchall()
    db.commit()
    db.close()
    
    return done_exp


def select_my_newest_capital():    
    db = get_conn()
    cursor = db.cursor()

    sql_cap = "select * from my_capital a order by seq desc limit 1"
    cursor.execute(sql_cap)
    newest_wallet = cursor.fetchall()
    db.commit()
    db.close()
    
    return newest_wallet

def count_recall():
    db = get_conn()
    cursor = db.cursor()

    sql_resu_recall_son = "select count(*) from model_ev_mid a where a.resu_predict = 1 and a.resu_real = 1"
    cursor.execute(sql_resu_recall_son)
    recall_son = cursor.fetchall()[0][0]

    sql_resu_recall_mon = "select count(*) from model_ev_mid a where a.resu_real = 1"
    cursor.execute(sql_resu_recall_mon)
    recall_mon = cursor.fetchall()[0][0]

    db.commit()
    db.close()

    if recall_mon == 0:
        print('WARN: recall_mon is 0!')
        return 0
    
    recall = recall_son / recall_mon
    
    return recall


def count_acc():
    db = get_conn()
    cursor = db.cursor()

    sql_resu_acc_son = "select count(*) from model_ev_mid a where a.resu_predict = 1 and a.resu_real = 1"
    cursor.execute(sql_resu_acc_son)
    acc_son = cursor.fetchall()[0][0]

    sql_resu_acc_mon = "select count(*) from model_ev_mid a where a.resu_predict = 1"
    cursor.execute(sql_resu_acc_mon)
    acc_mon = cursor.fetchall()[0][0]

    db.commit()
    db.close()

    if acc_mon == 0:
        print('INFO: ev mid predict result is 0. no up predict in db...')
        acc = 0
    else:
        acc = acc_son / acc_mon

    return acc


def count_acc_neg():
    db = get_conn()
    cursor = db.cursor()

    sql_resu_acc_neg_son = "select count(*) from model_ev_mid a where a.resu_predict = -1 and a.resu_real = -1"
    cursor.execute(sql_resu_acc_neg_son)
    acc_neg_son = cursor.fetchall()[0][0]

    sql_resu_acc_neg_mon = "select count(*) from model_ev_mid a where a.resu_predict = -1"
    cursor.execute(sql_resu_acc_neg_mon)
    acc_neg_mon = cursor.fetchall()[0][0]

    db.commit()
    db.close()

    if acc_neg_mon == 0:
        acc_neg_mon = -1
        acc_neg = -1
    else:
        acc_neg = acc_neg_son / acc_neg_mon
    
    return acc_neg    


def update_ev_mid_with_real(stock, adate):
    db = get_conn()
    cursor = db.cursor()

    sql_select = "select * from stock_all a where a.stock_code = '%s' and a.state_dt >= '%s' order by a.state_dt asc limit 2" % (stock, adate)
    cursor.execute(sql_select)
    latest_2_days_record = cursor.fetchall()

    if len(latest_2_days_record) <= 1:
        print('WARN: less than 2 record in stock_all. so return.(%s, %s)'% (stock, adate))
        return -1
    resu = 0
    if float(latest_2_days_record[1][3]) / float(latest_2_days_record[0][3]) > (1.00 + Utils.DAY_WAVE):
        resu = 1
    elif float(latest_2_days_record[1][3])/ float(latest_2_days_record[0][3]) < (1.00 - Utils.DAY_WAVE):
        resu = Utils.MINUS

    sql_update = "update model_ev_mid w set w.resu_real = '%.2f' where w.state_dt = '%s' and w.stock_code = '%s'" % (resu, adate, stock)
    cursor.execute(sql_update)
    db.commit()
    db.close()
    return 0

def get_predict(adate):
    db = get_conn()
    cursor = db.cursor()

    sql_predict = "select resu_predict from model_ev_mid a where a.state_dt = '%s'" % (adate)
    cursor.execute(sql_predict)
    done_predict = cursor.fetchall()

    db.commit()
    db.close()

    predict = 0
    if len(done_predict) != 0:
        predict = int(done_predict[0][0])

    return predict

def get_stock_predict(adate, stock):
    db = get_conn()
    cursor = db.cursor()

    sql_predict = "select predict from model_ev_resu a where a.state_dt = '%s' and a.stock_code = '%s'"%(adate, stock)
    cursor.execute(sql_predict)
    done_set_predict = cursor.fetchall()

    db.commit()
    db.close()

    predict = 0
    if len(done_set_predict) > 0:
        predict = int(done_set_predict[0][0])
    
    return predict

def insert_predict(adate, stock, predict):
    db = get_conn()
    cursor = db.cursor()
    sql_insert = "insert into model_ev_mid(state_dt,stock_code,resu_predict)values('%s','%s','%.2f')" % (adate, stock, predict)
    cursor.execute(sql_insert)
    db.commit()
    db.close()

def select_ev_result(state_dt, stock):
    db = get_conn()
    cursor = db.cursor()

    sql = "select * from model_ev_resu where state_dt = '%s' and stock_code = '%s'" % (state_dt, stock)

    cursor.execute(sql)
    ev_result = cursor.fetchall()

    db.commit()
    db.close()

    return ev_result

def insert_ev_result(state_dt, stock, acc, recall, f1, acc_neg, amodel, predict):
    db = get_conn()
    cursor = db.cursor()

    sql_final_insert = "insert into model_ev_resu(state_dt,stock_code,acc,recall,f1,acc_neg,bz,predict)values('%s','%s','%.4f','%.4f','%.4f','%.4f','%s','%s')" % (state_dt, stock, acc, recall, f1, acc_neg, amodel, str(predict))
    cursor.execute(sql_final_insert)

    db.commit()
    db.close()

def select_index(date_seq_start, date_seq_end):
    db = get_conn()
    cursor = db.cursor()

    sql_show_btc = "select * from stock_index a where a.code = 'SH' and a.date>= '%s' and a.date <= '%s' order by date asc"%(date_seq_start,date_seq_end)
    cursor.execute(sql_show_btc)
    done_set_show_btc = cursor.fetchall()

    db.commit()
    db.close()

    return done_set_show_btc

def select_profit():
    db = get_conn()
    cursor = db.cursor()

    sql_show_profit = "select max(a.capital),a.state_dt from my_capital a where a.state_dt is not null group by a.state_dt order by a.state_dt asc"
    cursor.execute(sql_show_profit)
    done_set_show_profit = cursor.fetchall()

    db.commit()
    db.close()

    return done_set_show_profit

def insert_my_capital(new_capital, new_money_lock,new_money_rest, act,
                      stock_code, vol, new_profit, new_profit_rate, bz,  opdate, price):
    db = get_conn()
    cursor = db.cursor()

    sql_sell_insert = "insert into my_capital(capital,money_lock,money_rest,deal_action,stock_code,stock_vol,profit,profit_rate,bz,state_dt,deal_price)values('%.2f','%.2f','%.2f','%s','%s','%.2f','%.2f','%.2f','%s','%s','%.2f')" %(new_capital,new_money_lock,new_money_rest,act,stock_code,vol,new_profit,new_profit_rate,bz,opdate, price)
    cursor.execute(sql_sell_insert)

    db.commit()
    db.close()

def insert_my_stock_poll(stock_code, buy_price, vol):
    db = get_conn()
    cursor = db.cursor()
    sql_buy_update3 = "insert into my_stock_pool(stock_code,buy_price,hold_vol,hold_days) VALUES ('%s','%.2f','%i','%i')" % (stock_code, buy_price, vol, int(1))
    cursor.execute(sql_buy_update3)

    db.commit()
    db.close()

def update_my_stock_poll(stock_code, new_buy_price, new_vol):
    db = get_conn()
    cursor = db.cursor()

    sql_buy_update3 = "update my_stock_pool w set w.buy_price = (select '%.2f' from dual) where w.stock_code = '%s'" % (new_buy_price, stock_code)
    sql_buy_update3b = "update my_stock_pool w set w.hold_vol = (select '%i' from dual) where w.stock_code = '%s'" % (new_vol, stock_code)
    sql_buy_update3c = "update my_stock_pool w set w.hold_days = (select '%i' from dual) where w.stock_code = '%s'" % (1, stock_code)
    cursor.execute(sql_buy_update3)
    cursor.execute(sql_buy_update3b)
    cursor.execute(sql_buy_update3c)

    db.commit()
    db.close()

def delete_my_stock_poll(stock_code):
    db = get_conn()
    cursor = db.cursor()

    sql_sell_update = "delete from my_stock_pool where stock_code = '%s'" % (stock_code)
    cursor.execute(sql_sell_update)

    db.commit()
    db.close()

def update_hold_days():
    db = get_conn()
    cursor = db.cursor()

    sql_update_hold_days = 'update my_stock_pool w set w.hold_days = w.hold_days + 1'
    cursor.execute(sql_update_hold_days)

    db.commit()
    db.close()

def select_my_stock_pool():
    db = get_conn()
    cursor = db.cursor()

    sql_pool = "select * from my_stock_pool"
    cursor.execute(sql_pool)
    done_set = cursor.fetchall()
    db.commit()
    db.close()

    return done_set


def get_stock_calender(startdate, enddate):
    start = startdate
    end = enddate
    if type(startdate) == datetime.datetime:
        start = Utils.format_d(startdate)
    elif(len(startdate) != 8):
        start = Utils.date2d(startdate)
    
    if type(enddate) == datetime.datetime:
        end = Utils.format_d(enddate)
    elif(len(enddate) != 8):
        end = Utils.date2d(enddate)
    
    db = get_conn()
    cursor = db.cursor()

    sql ="select cal_date from calender where cal_date >= '%s' and cal_date < '%s'" % (start, end)

    cursor.execute(sql)

    cal_seq = cursor.fetchall()
    
    db.commit()
    db.close()
    
    return [x[0] for x in cal_seq]

if __name__ == '__main__':
    seq = get_stock_calender('2000-01-01', '2000-01-10')
    print(seq)
