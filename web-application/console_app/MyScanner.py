import os

try:
    from bleak import BleakScanner
except:
    os.system('pip install bleak')
    from bleak import BleakScanner

import asyncio
from queue import Queue

from DataCollector import DataCollector
from adv_decrypt import adv_decrypt
from BleakClientAssistant import BleakClientAssistant

class MyScanner:
    def __init__(self, timeout, start_serial, end_serial, pattern, loop):
        self._scanner = BleakScanner(detection_callback=self.detection_callback)
        self.scanning = asyncio.Event()
        self.timeout = timeout
        self.dc = DataCollector(start_serial, end_serial, pattern)
        self.queue_devices_to_connect = Queue()
        self.loop = loop

    def detection_callback(self, device, advertisement_data):
        try:
            if device.name in self.dc.device_names: 
                
                
                self.queue_devices_to_connect.put(device)
            
                self.dc.device_names.remove(device.name)
            
                print(f'found device with name: {device.name} {self.dc.start_len-len(self.dc.device_names)}/{self.dc.start_len}')
                self.dc.update_MAC(device.name, device.address)
                self.dc.update_RSSI(device.name, advertisement_data.rssi)
            
                oil_level_raw, battery_voltage, TD_temp_raw = adv_decrypt(advertisement_data.manufacturer_data[3862])
                self.dc.update_oil_level(device.name, oil_level_raw)
                self.dc.update_battery_voltage(device.name, battery_voltage)
                self.dc.update_temp(device.name, TD_temp_raw)
        except Exception as e:
            print(f"Error in callback (scanner): {e}")
            
    async def run(self):
        try:
            print(f'\t\tStarted scanning with {self.timeout} seconds timeout...')
            await self._scanner.start()
            self.scanning.set()
            end_time = self.loop.time() + self.timeout
            while self.scanning.is_set():
                if self.loop.time() > end_time or len(self.dc.device_names) == 0:
                    self.scanning.clear()
                    if len(self.dc.device_names) == 0:
                        print('All devices have been found.')
                        return
                    else:
                        answer = input(f"Timeout. Can't find all devices ({len(self.dc.device_names)*100/self.dc.start_len:.2f}%): {self.dc.device_names}. Do you want to scan again? (Y for yes/ANY for no): ").lower()
                        if answer == 'y':
                            self.scanning.set()
                            change_timeout = input(f"Would you like to change timeout? (Y for yes/ANY for no): ").lower()
                            if change_timeout == 'y':
                                try:
                                    new_timeout = int(input('Timeout secdonds (only int): '))
                                    self.timeout = new_timeout
                                    end_time = self.loop.time() + self.timeout
                                    print(f'\t\tStarted scanning with {self.timeout} seconds timeout...')
                                except:
                                    print('timeout can be int only!')
                                    new_timeout = int(input('Timeout secdonds (only int):'))
                                    self.timeout = new_timeout
                                    end_time = self.loop.time() + self.timeout
                                    print(f'\t\tStarted scanning with {self.timeout} seconds timeout...')
                            else:
                                end_time = self.loop.time() + self.timeout
                                print(f'\t\tStarted scanning with {self.timeout} seconds timeout...')
                        else:
                            print(f"Scan terminated. Devices no found: {self.dc.device_names}")
                else:
                    await asyncio.sleep(0.1)
            await self._scanner.stop()
        except Exception as e:
            print(f"Error in run (scanner): {e}")

    def get_dataframe(self):
        return self.dc.get_dataframe()
    
    def queue_connection(self, message):
        while not self.queue_devices_to_connect.empty():
            print('Devices in queue:', self.queue_devices_to_connect.queue)
            device = self.queue_devices_to_connect.get()
            assistant = BleakClientAssistant(device)
            try:
                hk, lk = assistant.run(message)
                self.dc.update_HK(device.name, hk)
                self.dc.update_LK(device.name, lk)
            except Exception as e:
                print('Exception in Scanner (queue):', e)