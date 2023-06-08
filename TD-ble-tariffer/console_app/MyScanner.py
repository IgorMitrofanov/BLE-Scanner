import os

try:
    from bleak import BleakScanner
except:
    os.system('pip install bleak')
    from bleak import BleakScanner

import asyncio
import random
import datetime
# from queue import Queue

from DataCollector import DataCollector
from adv_decrypt import adv_decrypt
from BleakClientAssistant import BleakClientAssistant

try:
    from colorama import init, Fore, Style
except:
    os.system('pip install colorama==0.4.6')

init()

class MyScanner:
    def __init__(self, timeout, start_serial, end_serial, pattern, loop):
        self._scanner = BleakScanner(detection_callback=self.detection_callback, loop=loop)
        self.scanning = asyncio.Event()
        self.timeout = timeout
        self.dc = DataCollector(start_serial, end_serial, pattern)
        self.queue_devices_to_connect = [] # Queue()
        self.retry_devices_list = []
        self.loop = loop

    def detection_callback(self, device, advertisement_data):
        try:
            if device.name in self.dc.device_names: 
                
                
                self.queue_devices_to_connect.append(device)
            
                self.dc.device_names.remove(device.name)
            
                print(Fore.GREEN + f'found device with name: {device.name} {self.dc.start_len-len(self.dc.device_names)}/{self.dc.start_len}'+ Style.RESET_ALL)


                self.dc.update_char(device.name, 'MAC', device.address)
                self.dc.update_char(device.name, 'RSSI', advertisement_data.rssi)

                oil_level_raw, battery_voltage, TD_temp_raw, version_raw, cnt_raw = adv_decrypt(advertisement_data.manufacturer_data[3862])

                self.dc.update_char(device.name, 'Battery Voltage', battery_voltage)
                self.dc.update_char(device.name, 'version', version_raw)
                self.dc.update_char(device.name, 'Temperature', TD_temp_raw)
                self.dc.update_char(device.name, 'Oil Level', oil_level_raw)
                self.dc.update_char(device.name, 'Period', cnt_raw)


        except Exception as e:
            print(Fore.RED + f"Error in callback (scanner): {e}")
            
    async def run(self):
        try:
            print(Fore.GREEN + f'\t\tStarted scanning with {self.timeout} seconds timeout...')
            await self._scanner.start()
            self.scanning.set()
            end_time = self.loop.time() + self.timeout
            while self.scanning.is_set():
                if self.loop.time() > end_time or len(self.dc.device_names) == 0:
                    self.scanning.clear()
                    if len(self.dc.device_names) == 0:
                        print(Fore.GREEN + '\t\tAll devices have been found.')
                        break
                    else:
                        print(Fore.RED + f"\t\tTimeout. Can't find all devices ({len(self.dc.device_names)*100/self.dc.start_len:.2f}%)")
                        print(Fore.RED + f'Devices not found: {self.dc.device_names}' + Style.RESET_ALL)
                        answer = input(f"Do you want to scan again? (Y for yes/ANY for no): ").lower()
                        if answer == 'y':
                            self.scanning.set()
                            change_timeout = input(f"Would you like to change timeout? (Y for yes/ANY for no): ").lower()
                            if change_timeout == 'y':
                                try:
                                    new_timeout = int(input('Timeout secdonds (only int): '))
                                    self.timeout = new_timeout
                                    end_time = self.loop.time() + self.timeout
                                    print(Fore.GREEN + f'\t\tStarted scanning with {self.timeout} seconds timeout...')
                                except:
                                    print(Fore.RED + 'timeout can be int only!')
                                    new_timeout = int(input('Timeout secdonds (only int):'))
                                    self.timeout = new_timeout
                                    end_time = self.loop.time() + self.timeout
                                    print(Fore.YELLOW + f'\t\tStarted scanning with {self.timeout} seconds timeout...')
                            else:
                                end_time = self.loop.time() + self.timeout
                                print(Fore.YELLOW + f'\t\tStarted scanning with {self.timeout} seconds timeout...')
                        else:
                            print(Fore.RED + f"Scan terminated. Devices no found: {self.dc.device_names}")
                else:
                    await asyncio.sleep(0.1)
            await self._scanner.stop()
            await self.queue_to_connection(self.loop)
        except Exception as e:
            print(Fore.RED + f"Error in run (scanner): {e}")

    def get_dataframe(self):
        return self.dc.get_dataframe()
    
    def to_excel(self, xls_path):
        date_and_time_write = datetime.datetime.now().strftime('%Y_%m_%d %H-%M')
        self.dc.get_dataframe().to_excel(xls_path, sheet_name=date_and_time_write)

    async def connect_device(self, device, loop):
        client_assistant = BleakClientAssistant(device, loop)
        hk, lk = await client_assistant.run()
        if hk == 0 and lk == 0:
            self.queue_devices_to_connect.append(device)
        else:
            self.dc.update_char(device.name, 'HK', hk)
            self.dc.update_char(device.name, 'LK', lk)

    async def queue_to_connection(self, loop):
        while not len(self.queue_devices_to_connect) == 0:
            random_device = random.choice(self.queue_devices_to_connect)
            self.queue_devices_to_connect.remove(random_device)
            print(Fore.GREEN + f'Trying to connect {random_device}')
            await self.connect_device(random_device, loop)

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    start_serial = int(input('Type start serial (only six numers): '))
    end_serial = int(input('Type start serial (only six numers): '))
    timeout = int(input('Type time in seconds for timeout scanning: '))
    my_scanner = MyScanner(timeout=timeout, start_serial=start_serial, end_serial=end_serial, pattern='TD_', loop=loop)
    loop.run_until_complete(my_scanner.run())
    print(my_scanner.get_dataframe())