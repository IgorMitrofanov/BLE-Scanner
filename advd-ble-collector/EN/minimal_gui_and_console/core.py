import os
import asyncio
from MyScanner import MyScanner
import argparse
import time
import sys
from colorama import init, Fore, Style


init()

# Receiving parameters from gui

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

my_scanner = MyScanner(timeout=timeout, start_serial=start_serial, end_serial=end_serial, device_type=device_type, loop=loop)
loop.run_until_complete(my_scanner.run())

print(Fore.GREEN + '\t\tData preview:'+ Style.RESET_ALL)
print(my_scanner.get_dataframe().head())

if report_path != 'WITHOUT_WRITE':
    filename = 'collected_' + device_type + '_' + str(start_serial)+ '-' + str(end_serial) + '.xlsx'
    my_scanner.to_excel(report_path + '/' + filename)

    print(Fore.GREEN + f'File writed to {report_path} with name {filename}')
    print(Fore.YELLOW + '\t\tProgram terminated.')

    for i in range(5, 0, -1):
        print(Fore.YELLOW + f"Closing console in {i} seconds...")
        time.sleep(1)
    sys.exit()

else:
    print(Fore.RED + 'Warning: the mode without recording the report was selected')
    print(Fore.YELLOW + '\t\tProgram terminated.')
    
    for i in range(5, 0, -1):
        print(Fore.YELLOW + f"Closing console in {i} seconds...")
        time.sleep(1)
    sys.exit()
