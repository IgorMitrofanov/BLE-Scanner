import os

try:
    from tqdm import tqdm
except:
    os.system('pip install tqdm')
    from tqdm import tqdm

try:
    from bleak import BleakClient
    from bleak.exc import BleakError
except:
    os.system('pip install bleak')
    from bleak import BleakClient
    from bleak.exc import BleakError

import asyncio
import re

class BleakClientAssistant:
    def __init__(self, address, timeout=30):
        self.address = address
        self.timeout = timeout
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.client = None
        self.hk = None
        self.lk = None

    async def connect(self):
        self.client = BleakClient(self.address, timeout=self.timeout, cache_timeout=600)
        try:
            success = await self.client.is_connected()
            if success:
                await asyncio.sleep(1)  
                await self.client.start_notify(14, self.callback)
            else:
                print("Failed to connect to device")
        except BleakError as e:
            print(f"Could not connect to device: {e}")
            for i in range(10):
                print(f"Retrying connect {i+1}/10...")
                try:
                    with tqdm(total=100, desc=f"Connecting and sending data on {self.address}:") as pbar:
                        for i in range(100):
                            pbar.update(1)
                            await asyncio.sleep(0.01)
                        success = await self.client.connect()
                        if success:
                            await asyncio.sleep(1)  
                            await self.client.start_notify(14, self.callback)
                            return
                        else:
                            print("Failed to connect to device")
                except BleakError as e:
                    print(f"Could not connect to device: {e}")
            retry = input("Would you like to retry connect? (y/n) ")
            if retry.lower() == "y":
                await self.connect()
            else:
                return
    
    async def disconnect(self):
        await self.client.stop_notify(14)
        await self.client.disconnect()
        
    async def send_message(self, message):
        try:
            await self.client.write_gatt_char(12, message)
           # print(f'WRITE: {message} on TX_char')
            await asyncio.sleep(1)
        except Exception as e:
            print(f"Error in send message (client): {e}")
    async def callback(self, sender: int, data: bytearray):
        try:
            response = data.decode().strip()
            print(f'Received notification from RX_char on {self.address}: {response}')
            match = re.search(r"HK:1:(\d+),LK:1:(\d+)", response)
            if match:
                self.hk = int(match.group(1))
                self.lk = int(match.group(2))
        except Exception as e:
            print(f"Error in callback (client): {e}")
    def run(self, message):
        try:
            self.loop.run_until_complete(self.connect())
            self.loop.run_until_complete(self.send_message(message))
            self.loop.run_until_complete(self.disconnect())
            return self.hk, self.lk
        except Exception as e:
            print(f"Error in run (client): {e}")



if __name__ == '__main__':
    assistant = BleakClientAssistant('CA:17:37:73:61:98')
    hl, lk = assistant.run(b'GA\r')
