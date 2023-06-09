from MyScanner import MyScanner
from BleakClientAssistant import BleakClientAssistant
import asyncio
import random
import datetime
from colorama import init, Fore, Style
import argparse
import sys
import time


class Core:
    """
    Description of the Core class. This is the core of the program.

    Attributes:
    - loop (asyncio.AbstractEventLoop): async event loop object.
    - devices_to_connect (list): list of devices to connect.
    - my_scanner (Myscaner): an instance of the MyScanner class for scanning devices.

    Methods:
    - __init__(self, loop, timeout, start_serial, end_serial, device_type): class constructor.
    - run_scanner(self): method for starting device scanning.
    - connect_device(self, device): the method for connecting to the device and calibration.
    - queue_to_connection(self): a method for organizing the connection queue.

    """
    def __init__(self, loop, timeout, start_serial, end_serial, device_type):
        """
        Constructor of the Core class.

        Parameters:
        - loop (asyncio.AbstractEventLoop): async event loop object.
        - - timeout (int): timeout for scanning devices.
        - start_serial (str): the initial serial number for scanning devices.
        - end_serial (str): the final serial number for scanning devices.
        - device_type (str): the type of device to scan.
        - - attribute_error_flag (bool) a crutch for the bleak library

        """
        self.loop = loop
        self.devices_to_connect = []
        self.my_scanner = MyScanner(timeout=timeout, start_serial=start_serial, end_serial=end_serial, device_type=device_type, loop=loop)
        self.atrribute_error_flag = False

    async def run_scanner(self):
        """
        Method for starting device scanning.

        Returns:
        - list: a list of devices to connect.

        """
        self.devices_to_connect = await self.my_scanner.run() 
        return self.devices_to_connect


    async def connect_device(self, device):
            """
            Method for connecting to the device.

            Parameters:
            - device: the device to connect.

            Returns:
            1 in case of success, 0 in case of failure.
            """
            try:
                # Obtaining the necessary parameters for calculating the upper and lower calibration values
                temp = int(self.my_scanner.dc.df.loc[self.my_scanner.dc.df['Name'] == device.name, 'Temperature'].values[0])
                period = int(self.my_scanner.dc.df.loc[self.my_scanner.dc.df['Name'] == device.name, 'Period'].values[0])
                fl = int(self.my_scanner.dc.df.loc[self.my_scanner.dc.df['Name'] == device.name, 'Fuel level'].values[0])

                # Initialization of the client for connection and calibration
                client_assistant = BleakClientAssistant(device, period, temp, fl, self.loop)
                hk, lk, ul = await client_assistant.run()

                # If calibration failed
                if hk == 0 and lk == 0 and ul == 0:
                    self.devices_to_connect.append(device)
                    return 0
                
                # A crutch for the bleak library
                elif hk == 10 and lk == 10 and ul == 10:
                    print(Fore.YELLOW + f'The calibration of {device} failed, the program needs to be restarted')
                    self.atrribute_error_flag = True
                    return 0
                
                # If the calibration was successful, we write the parameters to the Data Collector object
                else:
                    self.my_scanner.dc.update_char(device.name, 'H', int(hk))
                    self.my_scanner.dc.update_char(device.name, 'L', int(lk))
                    self.my_scanner.dc.update_char(device.name, 'Fuel level after calibrate', int(ul))

                    #self.my_scanner.dc.get_dataframe().to_excel('temp.xlsx') # If you need to save a temporary file after each calibration

                    return 1
            except Exception as e:
                #print(e) # Debugging output
                pass


    async def queue_to_connection(self):
            """
            Method for organizing the connection queue.
            """
            while not len(self.devices_to_connect) == 0: 
                random_device = random.choice(self.devices_to_connect)
                self.devices_to_connect.remove(random_device)
                coro = self.connect_device(random_device)
                task = asyncio.create_task(coro)
                print(Style.RESET_ALL + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + Fore.GREEN + f'\t\tSuccessful calibration counter: {self.my_scanner.dc.start_len-len(self.devices_to_connect)-1}/{self.my_scanner.dc.start_len}')
                try:
                    # Starting a task with watchdog in 30 seconds
                    done, pending = await asyncio.wait([task], timeout=30) 
                except asyncio.TimeoutError:
                    # If watchdog has worked, we return the device back to the list for connection
                    self.devices_to_connect.append(random_device)


async def core_program(loop, timeout, start_serial, end_serial, report_path):
    core = Core(loop, timeout=timeout, start_serial=start_serial, end_serial=end_serial, device_type='TD')
    await core.run_scanner()
    await core.queue_to_connection()
    print(core.my_scanner.dc.get_dataframe())
    core.my_scanner.dc.to_excel(report_path + '/' + 'tariffy_' + str(start_serial) + '-' + str(end_serial) + '.xlsx', core.atrribute_error_flag)
    for i in range(10, 0, -1):
        print(Fore.YELLOW + f"The program will terminate automatically after {i} seconds...")
        time.sleep(1)
    sys.exit()


async def main(loop, timeout, start_serial, end_serial, report_path):
    await core_program(loop, timeout, start_serial, end_serial, report_path)


init()

parser = argparse.ArgumentParser()
parser.add_argument('start_serial', type=int, help='Start serial number')
parser.add_argument('end_serial', type=int, help='End serial number')
parser.add_argument('timeout', type=int, help='Timeout')
parser.add_argument('report_path', type=str, help='Report path')

args = parser.parse_args()

start_serial = args.start_serial
end_serial = args.end_serial
timeout = args.timeout
report_path = args.report_path

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

loop.run_until_complete(main(loop, timeout, start_serial, end_serial, report_path))

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.set_debug(True)
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(loop, timeout=120, start_serial=400043, end_serial=400052, report_path='C:/Users/User/Desktop'))
