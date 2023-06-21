import os

import asyncio
from MyScanner import MyScanner
import argparse
import sys
import time

try:
    from colorama import init, Fore, Style
except:
    os.system('pip install colorama==0.4.6')

init()


parser = argparse.ArgumentParser(description='Scan devices')
parser.add_argument('device_type', type=str, help='Device type')
parser.add_argument('start_serial', type=int, help='Start serial number')
parser.add_argument('end_serial', type=int, help='End serial number')
parser.add_argument('timeout', type=int, help='Timeout')
parser.add_argument('report_path', type=str, help='Report path')


args = parser.parse_args()

device_type = args.device_type
start_serial = args.start_serial
end_serial = args.end_serial
timeout = args.timeout
report_path = args.report_path
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

my_scanner = MyScanner(timeout=timeout, start_serial=start_serial, end_serial=end_serial, device_type='TD', loop=loop)
loop.run_until_complete(my_scanner.run())
print(Fore.GREEN + '\t\tПредпросмотр данных:'+ Style.RESET_ALL)
print(my_scanner.get_dataframe().head(10))

if report_path != 'WITHOUT_WRITE':
    filename = 'tariffy_' + device_type + '_' + str(start_serial)+ '-' + str(end_serial) + '.xlsx'
    my_scanner.to_excel(report_path + '/' + filename)
    print(Fore.GREEN + f'Файл записан в директорию {report_path} с именем {filename}')
    print(Fore.YELLOW + '\t\tПрограмма закончена.')
    for i in range(10, 0, -1):
        print(Fore.YELLOW + f"Консоль закроется автоматически через {i} секунд...")
        time.sleep(1)

    sys.exit()
else:
    print(Fore.RED + 'Предупреждение: был выбран режим без записи отчета.')
    print(Fore.YELLOW + '\t\tПрограмма закончена.')
    for i in range(10, 0, -1):
        print(Fore.YELLOW + f"Консоль закроется автоматически через {i} секунд...")
        time.sleep(1)

    sys.exit()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    start_serial = int(input('Type start serial (only six numers): '))
    end_serial = int(input('Type start serial (only six numers): '))
    timeout = int(input('Type time in seconds for timeout scanning: '))
    my_scanner = MyScanner(timeout=timeout, start_serial=start_serial, end_serial=end_serial, device_type='TD', loop=loop)
    loop.run_until_complete(my_scanner.run())
