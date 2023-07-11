import os
from bleak import BleakClient
from colorama import init, Fore, Style
import asyncio
import re
import datetime


class BleakClientAssistant:
    """
    Description of the BleakClientAssistant class.

    Attributes:
    - fl (int): fuel level.
    - period (int): period.
    - temp (int): temperature.
    - temp_corr (int): thermal correction coefficient.
    - device (str): string parameter representing the device (can be TD and TH).
    - - connected (boolean): flag indicating the connection status.
    - hk (int): the upper level after calibration.
    - lk (int): lower level after calibration.
    - ul (int): fuel level after calibration.

    Methods:
    - __init__(self, fl, period, temp, temp_corr, device): constructor of the class.
    - run(self): a method that connects and sends a message for calibration.
    - notification_callback(self, sender, data): a callback method for processing notifications.
    """
    def __init__(self, device, period, temp, fl, loop):
        """
        Constructor of the ClassName class.

        Parameters:
        - fl (int): fuel level.
        - period (int): period.
        - temp (int): temperature.
        - temp_corr (int): thermal correction coefficient.
        - device (str): string parameter representing the device (can be TD and TH).
        """
        self.device = device
        self.period = period
        self.temp = temp
        self.fl = fl
        self.hk = None
        self.lk = None
        self.ul = None
        self.loop = loop
        self.connected = False

        # Calculation of the correction factor
        if temp >= 0:
            self.temp_corr = 6
        else:
            self.temp_corr = 11


    async def run(self):
        """
        A method that connects and sends a message for calibration.

        Returns:
        - tuple: tuple with values hk, lk, ul or connection error.
        """
        # If the sensor is defective, then do not calibrate
        if self.fl == 6500 or self.fl == 7000: 
                return 1, 1, 7000
        try:
            empty = int(self.period - self.temp_corr * self.temp + 50)
            full = int(2.03*(self.period - 9400) + 9400 - self.temp*(self.temp_corr-self.period / 2400))

            # Collecting a package to send
            data = b"SD, LK:1:%s, HK:1:%s" % (str(empty).encode(), str(full).encode())
            print(Fore.GREEN + f'Trying to establish a connection with {self.device}...' )

            # Connecting to the device and sending a message with a calibration command
            async with BleakClient(self.device, timeout=60) as client:
                if client is not None and not self.connected:
                    await client.start_notify(14, self.notification_callback)
                    await client.write_gatt_char(12, data)
                    await client.write_gatt_char(12, b"GA\r") 
                    await asyncio.sleep(1)
                    self.connected = True
        except AttributeError as e:
            # Attributeerror crutch for the bleak library (in rare cases, an incomprehensible error occurs in the library itself, if it appears, the dachik will no longer be able to connect in this session)
            self.hk = 10
            self.lk = 10
            self.ul = 10
        except Exception as e:

            #print(e, type(e)) # Debugging message

            pass
        finally:
            if self.hk and self.lk and self.ul is not None:
                print(Fore.GREEN + f'\t\tDevice {self.device}: is calibrated!'+ Style.RESET_ALL)
                return self.hk, self.lk, self.ul
            else:
                print(Fore.RED + f'\t\tDevice {self.device}: filed connection!'+ Style.RESET_ALL)
                await asyncio.sleep(2) # Delay before reconnecting
                return 0, 0, 0


    def notification_callback(self, sender, data):
        """
        Callback method for handling notifications.

        Parameters:
        - sender: the sender of the notification.
        - data: notification data.
        """
        match = re.search(b"UL:1:(\d+),HK:1:(\d+),LK:1:(\d+)", data) # UL:1:(\d+),
        if match:
            self.ul = int(match.group(1))
            self.hk = int(match.group(2))
            self.lk = int(match.group(3))



init()


if __name__ == '__main__':
    for i in range(100):
        print('iteration: ', i)
        print('time', datetime.datetime.now().strftime('%H:%M:%S '))
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        device = 'D1:4B:69:BE:F0:C5'
        client_assistant = BleakClientAssistant(device, period=25000, fl=24496, temp=25, loop=loop)
        hk, lk, ul = loop.run_until_complete(client_assistant.run())
        print(hk, lk, ul)

