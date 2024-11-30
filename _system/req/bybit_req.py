from pybit.unified_trading import HTTP
import sys
import os
import json
import time

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)
from _system.config import bybit_api, bybit_secret
from _system.logger import system_logger

class bybit:
    def __init__(self):
        self.session = HTTP(testnet=True)
        self.symbols = []

    def set_order(self, df):
        session = HTTP(
            testnet=False,
            api_key=bybit_api,
            api_secret=bybit_secret,
        )

        if df['type'].iloc[-1] == 'Long':
            side = 'Buy'
        else:
            side = 'Sell'
        
        order_1 = session.place_order(
            category=df['category'].iloc[-1],
            symbol=df['name'].iloc[-1],
            side=side,
            orderType="Limit",
            qty=df['qty_l0'].iloc[-1],
            price=df['limit0'].iloc[-1],
            takeProfit=df['takeprofit'].iloc[-1],
            isLeverage=0,
        )
        system_logger.info(f'order_1 {order_1}')

        order_2 = session.place_order(
            category=df['category'].iloc[-1],
            symbol=df['name'].iloc[-1],
            side=side,
            orderType="Limit",
            qty=df['qty_l1'].iloc[-1],
            price=df['limit1'].iloc[-1],
            takeProfit=df['takeprofit1'].iloc[-1],
            isLeverage=0,

        )
        system_logger.info(f'order_2 {order_2}')

        order_3 = session.place_order(
            category=df['category'].iloc[-1],
            symbol=df['name'].iloc[-1],
            side=side,
            orderType="Limit",
            qty=df['qty_l2'].iloc[-1],
            price=df['limit2'].iloc[-1],
            takeProfit=df['takeprofit2'].iloc[-1],
            stopLoss=df['stoploss'].iloc[-1],
            isLeverage=0,
        )
        system_logger.info(f'order_3 {order_3}')

    def set_leverage(self, df):
        session = HTTP(
            testnet=False,
            api_key=bybit_api,
            api_secret=bybit_secret,
        )
        
        try:
            i = session.set_leverage(
                category=df['category'].iloc[-1],
                symbol=df['name'].iloc[-1],
                buyLeverage=str(df['leverage'].iloc[-1]),
                sellLeverage=str(df['leverage'].iloc[-1]),
            )
        except Exception:
            i = None
        
        if i:
            return True
        else:
           return False
        
    def get_wallet(self):
        session = HTTP(
            testnet=False,
            api_key=bybit_api,
            api_secret=bybit_secret,
        )

        i = session.get_wallet_balance(
            accountType="UNIFIED",
            coin="USDT",
        )
        
        i = round(float(i['result']['list'][0]['coin'][0]['walletBalance']), 4)
        return i
        
    def cancel_orders(self, name, category):
        session = HTTP(
            testnet=False,
            api_key=bybit_api,
            api_secret=bybit_secret,
        )

        print(session.cancel_all_orders(
            category=category,
            symbol=name,
        ))