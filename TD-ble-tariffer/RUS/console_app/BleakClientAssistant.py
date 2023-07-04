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


import asyncio
import re
import datetime



init()

class BleakClientAssistant:
    def __init__(self, device, period, temp, fl, loop):
        self.device = device
        self.period = period
        self.temp = temp
        self.fl = fl
        self.hk = None
        self.lk = None
        self.ul = None
        self.loop = loop
        self.connected = False

        if temp >= 0:
            self.temp_corr = 6
        else:
            self.temp_corr = 11


    async def run(self):
        if self.fl == 6500 or self.fl == 7000: # если бракованный, то не тарировать
                return 1, 1, 7000
        try:
            empty = int(self.period - self.temp_corr * self.temp + 50)
            full = int(2.03*(self.period - 9400) + 9400 - self.temp*(self.temp_corr-self.period / 2400))
            data = b"SD, LK:1:%s, HK:1:%s" % (str(empty).encode(), str(full).encode())
            print(Fore.GREEN + f'Пытаюсь установить соединение с {self.device}...' )     
            async with BleakClient(self.device, timeout=30) as client:
                if client is not None and not self.connected:
                    await client.start_notify(14, self.notification_callback)
                    await client.write_gatt_char(12, data)
                    await client.write_gatt_char(12, b"GA\r") 
                    await asyncio.sleep(1)
                    self.connected = True
                else:
                   await asyncio.sleep(1)
                   pass
        except Exception as e:
            #print(e, type(e))
            pass
        finally:
            if self.hk and self.lk and self.ul is not None:
                print(Fore.GREEN + f'\t\tУстройство {self.device}: оттарировано!')
                return self.hk, self.lk, self.ul
            else:
                print(Fore.RED + f'\t\tУстройство {self.device}: ошибка подключения!')
                return 0, 0, 0


    def notification_callback(self, sender, data):
        match = re.search(b"UL:1:(\d+),HK:1:(\d+),LK:1:(\d+)", data) # UL:1:(\d+),
        if match:
            self.ul = int(match.group(1))
            self.hk = int(match.group(2))
            self.lk = int(match.group(3))


if __name__ == '__main__':
    for i in range(100):
        print('iteration: ', i)
        print('time', datetime.datetime.now().strftime('%H:%M:%S '))
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        device = 'D1:4B:69:BE:F0:C5'
        client_assistant = BleakClientAssistant(device, period=25000, fl=24496, temp=25, loop=loop)
        loop.run_until_complete(client_assistant.run())