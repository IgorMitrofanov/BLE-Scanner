import asyncio
from bleak import BleakClient
from bleak.backends.winrt.client import WinRTClientArgs

args = WinRTClientArgs()


class BLEClient:
    def __init__(self):
        self.client = None

    async def connect(self, device_address):
        self.client = BleakClient(device_address, timeout=100, winrt=args)
        await self.client.connect()

    async def disconnect(self):
        await self.client.disconnect()

    async def send_message(self, message):
        await self.client.write_gatt_char(12, message)

    async def receive_notification(self):
        while True:
            notification = await self.client.start_notify(14)
            print(notification)

async def main():
    client = BLEClient()
    await client.connect("E2:F1:F3:8C:E1:45")
    await client.send_message(b'GA\r')
    await client.receive_notification()
    await client.disconnect()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())