import os

import asyncio
from MyScanner import MyScanner

try:
    from colorama import init, Fore, Style
except:
    os.system('pip install colorama==0.4.6')

init()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    start_serial = int(input('Type start serial (only six numers): '))
    end_serial = int(input('Type start serial (only six numers): '))
    timeout = int(input('Type time in seconds for timeout scanning: '))
    my_scanner = MyScanner(timeout=timeout, start_serial=start_serial, end_serial=end_serial, pattern='TD_', loop=loop)
    loop.run_until_complete(my_scanner.run())
    print(Fore.GREEN + '\t\tData preview:'+ Style.RESET_ALL)
    print(my_scanner.get_dataframe().head(10))