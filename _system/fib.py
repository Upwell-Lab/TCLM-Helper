from _system.logger import system_logger
from _system.req.bybit_req import bybit
bybit = bybit()

class tcl():
    def TCL_fib(self, fib_1, fib_0, category, name): #расчет TCL
        fib_1 = float(fib_1)
        fib_0 = float(fib_0)

        if fib_1 > fib_0:
            type_trade = 'Long'
        else:
            type_trade = 'Short'

        try:
            decimal_places = self.count_decimal_places(fib_1)
        except Exception as e:
            print(f'Ошибка decimal_places {e}')

        stoploss = -5
        takeprofit = 127.2
        limit0 = 61.8
        limit1 = 38.2
        limit2 = 17

        difference = fib_1 - fib_0
        stoploss_lvl = round(fib_0 + (stoploss / 100) * difference, decimal_places)
        takeprofit_lvl = round(fib_0 + (takeprofit / 100) * difference, decimal_places)
        limit0_lvl = round(fib_0 + (limit0 / 100) * difference, decimal_places)
        limit1_lvl = round(fib_0 + (limit1 / 100) * difference, decimal_places)
        limit2_lvl = round(fib_0 + (limit2 / 100) * difference, decimal_places)

        return {
            'name': name,
            'type': type_trade,
            'category': category,
            'fib_1': fib_1,
            'fib_0': fib_0,
            'limit0': limit0_lvl,
            'limit1': limit1_lvl, 
            'limit2': limit2_lvl,
            'stoploss': stoploss_lvl,
            'takeprofit': takeprofit_lvl
        }

    def count_decimal_places(self, number):
        number_str = str(number)
        if '.' in number_str:
            return len(number_str.split('.')[1])
        return 0
    
    def leverage(self, A3_DD, A6_DD, D4_TC):
        for leverage in range(1, 51):
            result = (A3_DD * A6_DD) / ((D4_TC * leverage) * 0.6)

            if result < 1.0:
                return leverage
    
    def qty(self, data, wallet): #cколько нужно покупать/продавать на каждом ордере
        D4_TC = wallet
        D3_DD = 4
        D4_DD = 7.4
        D5_DD = 26.67 #40
        C6_TC = data['limit0']
        C7_TC = data['takeprofit']
        C8_TC = data['stoploss']
        C13_TC = data['limit1']
        C14_TC = data['limit2']

        A2_DD = round((C6_TC + (C13_TC * 3)) / 4, 6)
        A3_DD = round((C6_TC + (C13_TC * 3) + (C14_TC * 5)) / 9, 6)
        if data['type'] == 'Long':
            B6_DD = C7_TC - C6_TC
        elif data['type'] == 'Short':
            B6_DD = C6_TC - C7_TC
        
        B6_DD = round(B6_DD, 2)

        A5_DD = B6_DD / C6_TC

        if data['type'] == 'Long':
            A6_DD = (D4_TC * (D3_DD / D5_DD)) / (A3_DD - C8_TC)
        elif data['type'] == 'Short':
            A6_DD = (D4_TC * (D3_DD / D5_DD)) / (C8_TC - A3_DD)
        
        D6_TC = A6_DD / 9 # qty0

        D13_TC = D6_TC * 3  # qty1
        D14_TC = D6_TC * 5  # qty2

        qty1 = round(D6_TC, 1)
        qty2 = round(D13_TC, 1)
        qty3 = round(D14_TC, 1)

        if data['type'] == 'Long':
            E13_TC = A2_DD + ((A5_DD / D3_DD) * A2_DD)
            if E13_TC >= C6_TC:
                E13_TC = C6_TC
        elif data['type'] == 'Short':
            E13_TC = A2_DD - ((A5_DD / D3_DD) * A2_DD)  # TP1
            if E13_TC <= C6_TC:
                E13_TC = C6_TC
        E13_TC = round(E13_TC, 4)
        
        if data['type'] == 'Long':
            E14_TC = A3_DD + ((A5_DD / D4_DD) * A3_DD)
            if E14_TC >= C6_TC:
                E14_TC = C6_TC
        elif data['type'] == 'Short':
            E14_TC = A3_DD - ((A5_DD / D4_DD) * A3_DD)  # TP2
            if E14_TC <= C6_TC:
                E14_TC = C6_TC
        E14_TC = round(E14_TC, 4)

        leverage = self.leverage(A3_DD, A6_DD, D4_TC)

        return {
            'takeprofit1': E13_TC,
            'takeprofit2': E14_TC,
            'qty_l0': qty1, 
            'qty_l1': qty2,
            'qty_l2': qty3, 
            'leverage': leverage,
            'wallet': wallet
        }
