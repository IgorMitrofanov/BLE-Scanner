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
    def __init__(self, device, loop, timeout=20):
        self.device = device
        self.loop = loop
        self.timeout = timeout
        self.hk = None
        self.lk = None

    async def run(self):
        try:
            async with BleakClient(self.device, timeout=self.timeout, detection_callback=self.notification_callback, loop=self.loop) as client:
               # client = BleakClient(self.device, timeout=self.timeout)
               # await client.connect()
                if client is not None:
                    await client.start_notify(14, self.notification_callback)
                    await client.write_gatt_char(12, b"GA\r", response=True) # сообщение для получения всех характеристик, дальнеший парсинг строки и получение hk и lk завершает цикл событий
                    await asyncio.sleep(0.1)
                    await client.disconnect()

        except Exception as e:
            if str(e).startswith("Could not get"):
                try:
                    async with BleakClient(self.device, timeout=self.timeout, detection_callback=self.notification_callback, loop=self.loop) as client:
                        # client = BleakClient(self.device, timeout=self.timeout)
                        # await client.connect()
                        if client is not None:
                            await client.start_notify(14, self.notification_callback)
                            await client.write_gatt_char(12, b"GA\r", response=True) # сообщение для получения всех характеристик, дальнеший парсинг строки и получение hk и lk завершает цикл событий
                            await asyncio.sleep(0.1)
                            await client.disconnect()
                except:
                    print()
            else:
                await asyncio.sleep(0.1)
        finally:
            if self.hk and self.lk is not None:
                print(Fore.GREEN + '\t\tSuccess!')
                return self.hk, self.lk
            else:
                print(Fore.RED + '\t\Failed!')
                return 0, 0

    def notification_callback(self, sender, data):
        match = re.search(b"HK:1:(\d+),LK:1:(\d+)", data)
        if match:
            self.hk = int(match.group(1))
            self.lk = int(match.group(2))

if __name__ == '__main__':
    address = "E2:F1:F3:8C:E1:45"
    loop = asyncio.new_event_loop()
    client_assistant = BleakClientAssistant(address, loop)
    asyncio.set_event_loop(loop)
    hk, lk = asyncio.run(client_assistant.run())
    print(hk, lk)
