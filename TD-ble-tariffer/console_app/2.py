import asyncio
from bleak import BleakClient 
import re
from tqdm import tqdm


address = "C7:B3:53:CE:54:E9"


class BleakClientAssistant:
    def __init__(self, address, loop, timeout=20):
        self.address = address
        self.loop = loop
        self.timeout = timeout
        self.hk = None
        self.lk = None

    async def run(self):
        with tqdm(total=100, desc="Connecting to device") as pbar:
            while True:
                try:
                    async with BleakClient(self.address, loop=self.loop, timeout=self.timeout) as client:
                        if client is not None:
                            pbar.set_description("Connected")
                            await client.start_notify(14, self.notification_callback)
                            await client.write_gatt_char(12, b"GA\r")
                            await asyncio.sleep(0.5)
                except Exception as e:
                    print(f"Error: {e}. Retrying...")
                    pbar.update(10)
                    await asyncio.sleep(0.1)
                finally:
                    if self.hk and self.lk is not None:
                        pbar.set_description("Values received")
                        pbar.update(100)
                        return self.hk, self.lk

    def notification_callback(self, sender, data):
        match = re.search(b"HK:1:(\d+),LK:1:(\d+)", data)
        if match:
            self.hk = int(match.group(1))
            self.lk = int(match.group(2))


loop = asyncio.new_event_loop()
client_assistant = BleakClientAssistant(address, loop)
asyncio.set_event_loop(loop)
hk, lk = asyncio.run(client_assistant.run())