from pybit.unified_trading import HTTP
from _system.logger import system_logger
import pandas as pd
import json
import sys
import os
import time

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(project_root)
from bybit_req import bybit
bybit = bybit()

class tcl_control:
    def __init__(self):
         self.df_state = pd.DataFrame({'hit': ['No'], 'takeprofit_hit': ['No']})
         self.orders = False

    def getdata(self, data):
        df = pd.DataFrame(data, index=[0])

        with open ("_system/settings.json", "r") as f:
            settings = json.load(f)

            if settings['testnet'] == 'False':
                settings = False
            elif settings['testnet'] == 'True':
                settings = True

        system_logger.info(f'\n{df}')

        session = HTTP(testnet=settings)
        while True:
            flag = True
            if self.df_state['takeprofit_hit'].iloc[-1] != 'No':
                system_logger.info(f'Тейкпрофит достигнут \n{self.df_state}')
                try:
                    bybit.cancel_orders(df['name'].iloc[-1], df['category'].iloc[-1])
                except Exception as e:
                    system_logger.error(f'Error cancel_orders 1 {e}')
                break
            else:
                if self.orders == False:
                    bybit.set_leverage(df)
                    try:
                        bybit.set_order(df)
                        self.orders = True
                    except Exception as e:
                        system_logger.error(f'Error setting order 1{e}')
                        bybit.cancel_orders(df['name'].iloc[-1], df['category'].iloc[-1])
                        break

            kline = session.get_kline(
                category='linear',
                symbol=df['name'].iloc[-1],
                interval=1,
                limit=1
            )
            kline = kline['result']['list'][0]

            low = float(kline[3])
            high = float(kline[2])

            try:
                try:
                    if df['type'].iloc[-1] == 'Long' and self.df_state['hit'].iloc[-1] == 'No':
                        if high > df['fib_1'].iloc[-1] and flag:  # Проверка только при значении self.flag
                            flag = False  # Сбрасываем флаг, чтобы избежать повторных вызовов
                            system_logger.info('Обновление данных...')
                            try:
                                if self.orders == True:
                                    self.orders = False
                                    try:
                                        bybit.cancel_orders(df['name'].iloc[-1], df['category'].iloc[-1])
                                    except Exception as e:
                                        system_logger.error(f'Error cancel_orders 2 {e}')
                                        break
                                time.sleep(2)
                                from launch import main
                                main(high, df['fib_0'].iloc[-1], df['category'].iloc[-1], df['name'].iloc[-1])
                                break
                            except Exception as e:
                                system_logger.error(f'Ошибка обновления данных - {e}')
                                break
                    elif df['type'].iloc[-1] == 'Short' and self.df_state['hit'].iloc[-1] == 'No':
                        if low < df['fib_1'].iloc[-1] and flag:  # Проверка только при значении self.flag
                            flag = False  # Сбрасываем флаг, чтобы избежать повторных вызовов
                            system_logger.info('Обновление данных...')
                            try:
                                if self.orders == True:
                                    self.orders = False
                                    try:
                                        bybit.cancel_orders(df['name'].iloc[-1], df['category'].iloc[-1])
                                    except Exception as e:
                                        system_logger.error(f'Error cancel_orders 2 {e}')
                                        break
                                from launch import main
                                main(low, df['fib_0'].iloc[-1], df['category'].iloc[-1], df['name'].iloc[-1])
                                break
                            except Exception as e:
                                system_logger.error(f'Ошибка обновления данных - {e}')
                                break
                except Exception as e:
                    system_logger.error(f'Ошибка изменения флага - {e}')

                if df['type'].iloc[-1] == 'Long' and flag:
                    if low <= df['limit0'].iloc[-1] and self.df_state['hit'].iloc[-1] == 'No':
                        self.df_state.loc[0, 'hit'] = 'L0'
                        system_logger.info(f'Поставлен L0 -\n {df}')
                        try:
                            pass #tcl_l0(type_)
                        except Exception as e:
                            system_logger.error(f'Ошибка открытия позиции - {e}')
                    elif high >= df['takeprofit'].iloc[-1] and self.df_state['hit'].iloc[-1] == 'L0':
                        self.df_state.loc[0, 'takeprofit_hit'] = 'TP0'
                    elif low <= df['limit1'].iloc[-1] and self.df_state['hit'].iloc[-1] == 'L0':
                        self.df_state.loc[0, 'hit'] = 'L1'
                    elif high >= df['takeprofit1'].iloc[-1] and self.df_state['hit'].iloc[-1] == 'L1':
                        self.df_state.loc[0, 'takeprofit_hit'] = 'TP1'
                    elif low <= df['limit2'].iloc[-1] and self.df_state['hit'].iloc[-1] == 'L1':
                        self.df_state.loc[0, 'hit'] = 'L2'
                    elif high >= df['takeprofit2'].iloc[-1] and self.df_state['hit'].iloc[-1] == 'L2':
                        self.df_state.loc[0, 'takeprofit_hit'] = 'TP2'
                    elif low <= df['stoploss'].iloc[-1] and self.df_state['hit'].iloc[-1] == 'L2':
                        self.df_state.loc[0, 'hit'] = 'SL'
                        self.df_state.loc[0, 'takeprofit_hit'] = 'SL'
                elif df['type'].iloc[-1] == 'Short' and flag:
                    if high >= df['limit0'].iloc[-1] and self.df_state['hit'].iloc[-1] == 'No':
                        self.df_state.loc[0, 'hit'] = 'L0'
                        system_logger.info(f'Поставлен L0 -\n {df}')
                        try:
                            pass #tcl_l0(type_)
                        except Exception as e:
                            system_logger.error(f'Ошибка открытия позиции - {e}')
                    elif low <= df['takeprofit'].iloc[-1] and self.df_state['hit'].iloc[-1] == 'L0':
                        self.df_state.loc[0, 'takeprofit_hit'] = 'TP0'
                    elif high >= df['limit1'].iloc[-1] and self.df_state['hit'].iloc[-1] == 'L0':
                        self.df_state.loc[0, 'hit'] = 'L1'
                    elif low <= df['takeprofit1'].iloc[-1] and self.df_state['hit'].iloc[-1] == 'L1':
                        self.df_state.loc[0, 'takeprofit_hit'] = 'TP1'
                    elif high >= df['limit2'].iloc[-1] and self.df_state['hit'].iloc[-1] == 'L1':
                        self.df_state.loc[0, 'hit'] = 'L2'
                    elif low <= df['takeprofit2'].iloc[-1] and self.df_state['hit'].iloc[-1] == 'L2':
                        self.df_state.loc[0, 'takeprofit_hit'] = 'TP2'
                    elif high >= df['stoploss'].iloc[-1] and self.df_state['hit'].iloc[-1] == 'L2':
                        self.df_state.loc[0, 'hit'] = 'SL'
                        self.df_state.loc[0, 'takeprofit_hit'] = 'SL'
            except Exception as e:
                system_logger.error(f'Ошибка обработки сообщения - {e}')
                break