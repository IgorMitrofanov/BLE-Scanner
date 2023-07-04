import os
import asyncio
from MyScanner import MyScanner


try:
    from colorama import init, Fore, Style
except:
    os.system('pip install colorama==0.4.6')


init()

loop = asyncio.new_event_loop()
loop.set_debug(True)
asyncio.set_event_loop(loop)

async def run_scanner():
    #start_serial = int(input('Type start serial (only six numers): '))
    #end_serial = int(input('Type start serial (only six numers): '))
    #timeout = int(input('Type time in seconds for timeout scanning: '))
    my_scanner = MyScanner(timeout=120, start_serial=400043, end_serial=400052, device_type='TD', loop=loop)
    await my_scanner.run()
    print(my_scanner.get_dataframe())
    report_path = r'C:/Users/User/Desktop/TEST'
    filename = '1111.xlsx'
    my_scanner.to_excel(report_path + '/' + filename)

async def main():
    await run_scanner()

loop.run_until_complete(main())
