import DBUtils

def cap_update_daily(state_dt):
    para_norisk = (1.0 + 0.04/365)
    
    done_set = DBUtils.select_my_stock_pool()
    
    new_lock_cap = 0.00
    for i in range(len(done_set)):
        stock_code = str(done_set[i][0])
        stock_vol = float(done_set[i][2])
        done_temp = DBUtils.select_stock_info(state_dt, stock_code)
        
        if len(done_temp) > 0:
            cur_close_price = float(done_temp[0][3])
            new_lock_cap += cur_close_price * stock_vol
        else:
            print('Cap_Update_daily Err!!')
            raise Exception
    
    done_cap = DBUtils.select_my_capital()
    
    new_cash_cap = float(done_cap[-1][2]) * para_norisk
    new_total_cap = new_cash_cap + new_lock_cap
    
    DBUtils.insert_my_capital(new_total_cap,new_lock_cap,new_cash_cap, 'sum',
                              'm', 0, 0, 0, str('Daily_Update'),state_dt, 0)
    
    return 1

if __name__ == '__main__':
    print('daily update...')
    cap_update_daily('2020-11-03')
    print('done.')
