import os

# Установка библиотек при первом запуске при необходимости

try:
    import openpyxl
    from openpyxl.styles import PatternFill, Font
except:
    os.system('pip install openpyxl==3.1.2')

try:
    from bleak import BleakClient


except:
    os.system('pip install bleak')
    from bleak import BleakClient

try:
    from bleak import BleakScanner
except:
    os.system('pip install bleak==0.20.2')


try:
    from colorama import init, Fore, Style
except:
    os.system('pip install colorama==0.4.6')


try:
    import pandas as pd
except:
    os.system('pip install pandas==2.0.2')
    import pandas as pd


from Core import Core
import asyncio

async def core_program(loop, timeout, start_serial, end_serial):
    core = Core(loop, timeout=timeout, start_serial=start_serial, end_serial=end_serial, device_type='TD')
    await core.run_scanner()
    await core.queue_to_connection()
    await asyncio.sleep(1)
    print(core.my_scanner.dc.get_dataframe())
    report_path = 'C:/Users/User/Desktop/'
    core.my_scanner.dc.to_excel(report_path + '/' + 'tariffy_' + str(start_serial) + '-' + str(end_serial) + '.xlsx', core.atrribute_error_flag)


async def main(loop, timeout, start_serial, end_serial, test=False):
    if test is False:
        start_serial = int(input('Введите начальный серийный номер (всего шесть цифр): '))
        end_serial = int(input('Введите начальный серийный номер (всего шесть цифр): '))
        timeout = int(input('Время сканирования: '))
    await core_program(loop, timeout, start_serial, end_serial)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(loop, timeout=200, start_serial=400043, end_serial=400052))
