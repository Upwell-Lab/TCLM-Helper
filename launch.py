import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from _system.logger import system_logger
from _system.req.bybit_req import bybit
from _system.req.proccesing import tcl_control
from _system.fib import tcl
tcl = tcl()
tcl_control = tcl_control()
bybit = bybit()

def main(fib_1, fib_0, category, name):
    wallet = bybit.get_wallet()
    try:
        data = tcl.TCL_fib(fib_1, fib_0, category, name)
    except Exception as e:
        system_logger.error(f'Error TCL_fib {e}')

    try:
        data_2 = tcl.qty(data, wallet)
    except Exception as e:
        system_logger.error(f'Error qty {e}')

    tcl_control.getdata({**data, **data_2})

def launcher():
    system_logger.info("Program started")

    while True:
        name = input("Enter the currency pair for tracking (example: BTCUSDT): ")
        category = 'linear'

        fib_1 = input("Enter the fib_1 level: ")
        fib_0 = input("Enter the fib_0 level: ")
        main(fib_1, fib_0, category, name)
        break

if __name__ == "__main__":
    launcher()