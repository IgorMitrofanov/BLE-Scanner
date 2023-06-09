import os


try:
    from bleak import BleakScanner
except:
    os.system('pip install bleak==0.20.2')
    from bleak import BleakScanner

import datetime
import asyncio
from DataCollector import DataCollector
from adv_decrypt import adv_decrypt


try:
    from colorama import init, Fore, Style
except:
    os.system('pip install colorama==0.4.6')


init()


class MyScanner:
    """
    Initializes the Myscaner object.

    Parameters:
    - timeout: time (in seconds) of scanning devices
    - start_serial: initial serial number of the device
    - end_serial: the final serial number of the device
    - device_type: device type
    - loop: asyncio event loop object

    """
    def __init__(self, timeout, start_serial, end_serial, device_type, loop):
        self._scanner = BleakScanner(detection_callback=self.detection_callback, loop=loop)
        self.scanning = asyncio.Event()
        self.timeout = timeout
        self.dc = DataCollector(start_serial, end_serial, device_type)
        self.devices_to_connect = [] 
        self.retry_devices_list = []
        self.loop = loop
        self.device_type = device_type


    async def detection_callback(self, device, advertisement_data):
        """
        Callback-function called when a new device is detected.

        Parameters:
        - device: device object
        - advertisement_data: data of the advertising package

        """
        try:
            if device.name in self.dc.device_names: 
                
                
                self.devices_to_connect.append(device)
            
                self.dc.device_names.remove(device.name)
            
                print(Fore.GREEN + f'Device found: {device.name} {self.dc.start_len-len(self.dc.device_names)}/{self.dc.start_len}'+ Style.RESET_ALL)


                self.dc.update_char(device.name, 'MAC', device.address)
                self.dc.update_char(device.name, 'RSSI', advertisement_data.rssi)

                oil_level_raw, battery_voltage, TD_temp_raw, version_raw, cnt_raw = adv_decrypt(advertisement_data.manufacturer_data[3862], device_type=self.device_type)

                self.dc.update_char(device.name, 'Battery voltage', battery_voltage)
                self.dc.update_char(device.name, 'version', version_raw)
                self.dc.update_char(device.name, 'Temperature', TD_temp_raw)
                self.dc.update_char(device.name, 'Fuel level', oil_level_raw)
                self.dc.update_char(device.name, 'Period', cnt_raw)

        except Exception as e:
            #print(Fore.RED + f"Error in callback (scanner): {e}") # debugging output
            pass


    async def run(self):
        try:
            print(Style.RESET_ALL + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + Fore.GREEN + f'\t\tScanning started for {self.timeout} seconds...')
            await self._scanner.start()
            self.scanning.set()
            end_time = self.loop.time() + self.timeout
            while self.scanning.is_set():
                if self.loop.time() > end_time or len(self.dc.device_names) == 0:
                    self.scanning.clear()
                    if len(self.dc.device_names) == 0:
                        print(Style.RESET_ALL + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + Fore.GREEN + '\t\tAll devices have been found.')
                        break
                    else:
                        print(Style.RESET_ALL + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + Fore.RED + f"\t\tScan time is up. Not all devices found ({len(self.dc.device_names)*100/self.dc.start_len:.2f}%).")
                        print(Fore.RED + f'Devices not found: {self.dc.device_names}' + Style.RESET_ALL)
                        answer = input(f"Do you want to search again? (y/any for no): ").lower()
                        if answer == 'y':
                            self.scanning.set()
                            change_timeout = input(f"Do you want to change the scan time? (y/any for no): ").lower()
                            if change_timeout == 'y':
                                try:
                                    new_timeout = int(input('Scan time (integers only): '))
                                    self.timeout = new_timeout
                                    end_time = self.loop.time() + self.timeout
                                    print(Style.RESET_ALL + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + Fore.GREEN + f'\t\tScanning started for {self.timeout} seconds...')
                                except:
                                    print(Fore.RED + 'The scan time can only be integer!' + Style.RESET_ALL)
                                    new_timeout = int(input('Scan time (integers only): '))
                                    self.timeout = new_timeout
                                    end_time = self.loop.time() + self.timeout
                                    print(Style.RESET_ALL + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + Fore.GREEN + f'\t\tScanning started for {self.timeout} seconds...')
                            else:
                                end_time = self.loop.time() + self.timeout
                                print(Style.RESET_ALL + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + Fore.GREEN + f'\t\tScanning started for {self.timeout} seconds...')
                        else:
                            print(Style.RESET_ALL + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + Fore.RED + f"\t\tScan time is up. Devices not found: {self.dc.device_names}")
                else:
                    await asyncio.sleep(0)
            await asyncio.sleep(0)
            await self._scanner.stop()
            return self.devices_to_connect
        except Exception as e:
           # print(Fore.RED + f"Error in run (scanner): {e}") # debugging output
            pass

async def run_scanner():
    #start_serial = int(input('Type start serial (only six numers): '))
    #end_serial = int(input('Type start serial (only six numers): '))
    #timeout = int(input('Type time in seconds for timeout scanning: '))
    my_scanner = MyScanner(timeout=10, start_serial=400043, end_serial=400052, device_type='TD', loop=loop)
    result = await my_scanner.run()
    return result

async def main():
    result = await run_scanner()
    print(result)

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.set_debug(True)
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())