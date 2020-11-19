import utils.DBUtils as DBUtils

class Deal(object):
    cur_capital = 0.00
    cur_money_lock = 0.00
    cur_money_rest = 0.00
    stock_pool = []
    stocks_buy_price = {}
    stocks_hold_vol = {}
    stocks_hold_days = {}
    stock_all = []
    ban_list = []

    def __init__(self,state_dt):
        try:
            wallet = DBUtils.select_my_newest_capital()
            
            if len(wallet) > 0:
                self.cur_capital = float(wallet[0][0])
                self.cur_money_rest = float(wallet[0][2])
            
            stock_pool = DBUtils.select_my_stock_pool()

            if len(stock_pool) > 0:
                self.stock_pool = [x[0] for x in stock_pool if x[2] > 0]
                self.stock_all = [x[0] for x in stock_pool]
                self.stocks_buy_price = {x[0]: float(x[1]) for x in stock_pool}
                self.stocks_hold_vol = {x[0]: int(x[2]) for x in stock_pool}
                self.stocks_hold_days = {x[0]: int(x[3]) for x in stock_pool}
                
            for i in range(len(stock_pool)):
                done_temp = DBUtils.select_stock_info(state_dt, stock_pool[i][0])
                self.cur_money_lock += float(done_temp[0][3]) * float(stock_pool[i][2])
                
            # sql_select3 = 'select * from ban_list'
            # cursor.execute(sql_select3)
            # wallet3 = cursor.fetchall()
            # if len(wallet3) > 0:
            #     self.ban_list = [x[0] for x in wallet3]

        except Exception as excp:
            print('ERROR:', excp)

