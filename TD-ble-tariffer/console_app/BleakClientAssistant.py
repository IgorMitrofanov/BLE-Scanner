import os

try:
    from bleak import BleakClient

except:
    os.system('pip install bleak')
    from bleak import BleakClient

try:
    from colorama import init, Fore, Style
except:
    os.system('pip install colorama==0.4.6')

init()


import asyncio
import re

class BleakClientAssistant:
    def __init__(self, device):
        self.device = device
       # self.timeout = timeout
        self.hk = None
        self.lk = None
        self.ss_count = 0

    async def run(self):
        try:
            print(Fore.GREEN + f'Trying to connect {self.device}...' )
            async with BleakClient(self.device) as client:
                if client is not None:
                    await client.start_notify(14, self.notification_callback)
                    await client.write_gatt_char(12, b"GA\r") 
                    await asyncio.sleep(1)
                    await client.disconnect()
                    await asyncio.sleep(1)
                else:
                    await client.disconnect()
                    await asyncio.sleep(1)
        except Exception as e:
            pass
        finally:
            if self.hk and self.lk is not None:
                print(Fore.GREEN + f'\t\tDevice {self.device}: successfull connection!')
                self.ss_count += 1
                return self.hk, self.lk, self.ss_count
            else:
                print(Fore.RED + f'\t\tDevice {self.device}: failed connection!')
                return 0, 0, 0

    def notification_callback(self, sender, data):
        print(data)
        match = re.search(b"HK:1:(\d+),LK:1:(\d+)", data)
        if match:
            self.hk = int(match.group(1))
            self.lk = int(match.group(2))
