import os

import asyncio
from MyScanner import MyScanner

try:
    from colorama import init, Fore, Style
except:
    os.system('pip install colorama==0.4.6')

init()

def main(i):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    #start_serial = int(input('Type start serial (only six numers): '))
    #end_serial = int(input('Type start serial (only six numers): '))
    #timeout = int(input('Type time in seconds for timeout scanning: '))
    my_scanner = MyScanner(timeout=120, start_serial=400043, end_serial=400052, device_type='TD', loop=loop)
    loop.run_until_complete(my_scanner.run())
    print(Fore.GREEN + '\t\tПредпросмотр данных:'+ Style.RESET_ALL)
    print(my_scanner.get_dataframe().head(10))
    report_path = r'C:/Users/User/Desktop/TEST'
    filename = str(i) + '.xlsx'
    my_scanner.to_excel(report_path + '/' + filename)


if __name__ == '__main__':
    for i in range(100):
        main(i)