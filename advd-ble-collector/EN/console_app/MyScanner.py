import os
import pandas as pd
from bleak import BleakScanner
import asyncio
import datetime
from DataCollector import DataCollector
from adv_decrypt import adv_decrypt


class MyScanner:
    """
    Initializes the Myscaner object.

    Parameters:
    - timeout: scan timeout in seconds
    - start_serial: initial serial number
    - end_serial: the final serial number
    - device_type: device type
    - loop: asynchronous execution loop
    """
    def __init__(self, timeout, start_serial, end_serial, device_type, loop):
        self._scanner = BleakScanner(detection_callback=self.detection_callback, loop=loop)
        self.scanning = asyncio.Event()
        self.timeout = timeout
        self.dc = DataCollector(start_serial, end_serial, device_type)
        self.loop = loop
        self.device_type = device_type


    def detection_callback(self, device, advertisement_data):
        """
        Callback is a function for processing detected devices.

        Parameters:
        - device: detected device
        - advertisement_data: device ad data
        """
        try:
            if device.name in self.dc.device_names: 
                
                
            
                self.dc.device_names.remove(device.name)
            
                print(f'found device with name: {device.name} {self.dc.start_len-len(self.dc.device_names)}/{self.dc.start_len}')
                self.dc.update_char(device.name, 'MAC', device.address)
                self.dc.update_char(device.name, 'RSSI', advertisement_data.rssi)

                if self.device_type == 'TD':

                    oil_level_raw, battery_voltage, TD_temp_raw, version_raw = adv_decrypt(advertisement_data.manufacturer_data[3862], device_type=self.device_type)

                    self.dc.update_char(device.name, 'Battery Voltage', battery_voltage)
                    self.dc.update_char(device.name, 'version', version_raw)
                    self.dc.update_char(device.name, 'Temperature', TD_temp_raw)
                    self.dc.update_char(device.name, 'Oil Level', oil_level_raw)


                elif self.device_type == 'TH':

                    TH09_temp, TH09_light_raw, TH09_humidity, TH09_battery, TH09_version_raw = adv_decrypt(advertisement_data.manufacturer_data[3862], device_type=self.device_type)

                    self.dc.update_char(device.name, 'Battery Voltage', TH09_battery)
                    self.dc.update_char(device.name, 'version', TH09_version_raw)
                    self.dc.update_char(device.name, 'Temperature', TH09_temp)
                    self.dc.update_char(device.name, 'Humidity', TH09_humidity)
                    self.dc.update_char(device.name, 'Light', TH09_light_raw)

        except Exception as e:
            
            # print(f"Error in callback (scanner): {e}") # Debugging output

            pass
            

    async def run(self):
        """
        Starts scanning and collecting data for the specified range of serial numbers and device type.
        """
        try:
            print(f'\t\tStarted scanning with {self.timeout} seconds timeout...')
            await self._scanner.start()
            self.scanning.set()
            end_time = self.loop.time() + self.timeout
            while self.scanning.is_set():
                if self.loop.time() > end_time or len(self.dc.device_names) == 0:
                    self.scanning.clear()
                    if len(self.dc.device_names) == 0:
                        print('\t\tAll devices have been found.')
                        return
                    else:
                        print(f"\t\tTimeout. Can't find all devices ({len(self.dc.device_names)*100/self.dc.start_len:.2f}%)")
                        print(f'Devices not found: {self.dc.device_names}')
                        answer = input(f"Do you want to scan again? (Y for yes/ANY for no): ").lower()
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

            #print(f"Error in run (scanner): {e}") # Debugging output
            
            pass


    def get_dataframe(self):
        """
        Returns the Data Frame with the collected data.

        Returns:
        - DataFrame with collected data
        """
        return self.dc.get_dataframe()
    

    def to_excel(self, xls_path):
        date_and_time_write = datetime.datetime.now().strftime('%Y_%m_%d %H-%M')
        self.dc.get_dataframe().to_excel(xls_path, sheet_name=date_and_time_write)
