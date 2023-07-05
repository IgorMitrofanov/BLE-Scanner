from MyScanner import MyScanner
from BleakClientAssistant import BleakClientAssistant
import asyncio
import random
import datetime
from colorama import init, Fore, Style


init()


class Core:
    def __init__(self, loop, timeout, start_serial, end_serial, device_type):
        self.loop = loop
        self.devices_to_connect = []
        self.my_scanner = MyScanner(timeout=timeout, start_serial=start_serial, end_serial=end_serial, device_type=device_type, loop=loop)

    async def run_scanner(self):
        self.devices_to_connect = await self.my_scanner.run() 
        return self.devices_to_connect


    async def connect_device(self, device):
            try:
                temp = int(self.my_scanner.dc.df.loc[self.my_scanner.dc.df['Имя'] == device.name, 'Температура'].values[0])
                period = int(self.my_scanner.dc.df.loc[self.my_scanner.dc.df['Имя'] == device.name, 'Период'].values[0])
                fl = int(self.my_scanner.dc.df.loc[self.my_scanner.dc.df['Имя'] == device.name, 'Уровень топлива'].values[0])
                client_assistant = BleakClientAssistant(device, period, temp, fl, loop)
                hk, lk, ul = await client_assistant.run()
                if hk == 0 and lk == 0 and ul == 0:
                    self.devices_to_connect.append(device)
                    return 0
                else:
                    self.my_scanner.dc.update_char(device.name, 'H', int(hk))
                    self.my_scanner.dc.update_char(device.name, 'L', int(lk))
                    self.my_scanner.dc.update_char(device.name, 'Уровень топлива после тарировки', int(ul))
                    #self.my_scanner.dc.get_dataframe().to_excel('temp.xlsx') 
                    return 1
            except Exception as e:
                print(e)


    async def queue_to_connection(self):
            while not len(self.devices_to_connect) == 0:
                random_device = random.choice(self.devices_to_connect)
                self.devices_to_connect.remove(random_device)
                coro = self.connect_device(random_device)
                task = asyncio.create_task(coro)
                print(Style.RESET_ALL + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + Fore.GREEN + f'\t\tСчетчик успешных тарировок: {self.my_scanner.dc.start_len-len(self.devices_to_connect)-1}/{self.my_scanner.dc.start_len}')
                try:
                    done, pending = await asyncio.wait([task], timeout=30) 
                except asyncio.TimeoutError:
                     self.devices_to_connect.append(random_device)

    
async def core_program(loop, i):
    core = Core(loop, timeout=120, start_serial=400043, end_serial=400052, device_type='TD')
    devices_to_connect = await core.run_scanner()
    await core.queue_to_connection()
    await asyncio.sleep(1)
    print(core.my_scanner.dc.get_dataframe())
    core.my_scanner.dc.to_excel(str(i)+'.xlsx')
    #print(my_scanner.dc.get_dataframe())
    #my_scanner.dc.to_excel('1.xlsx')

async def main(loop):
    for i in range(10):
        await core_program(loop, i)

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.set_debug(True)
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(loop))










    '''async def queue_to_connection(self):
            while not len(self.devices_to_connect) == 0:
                print(self.devices_to_connect, len(self.devices_to_connect))
                random_device = random.choice(self.devices_to_connect)
                self.devices_to_connect.remove(random_device)
                coro = self.connect_device(random_device)
                task = asyncio.create_task(coro)
                try:
                    done, pending = await asyncio.wait([task], timeout=30) 
                except asyncio.TimeoutError:
                     self.devices_to_connect.append(random_device)'''

















"""async def connect_device(self, device, loop):
        temp = int(self.dc.df.loc[self.dc.df['Имя'] == device.name, 'Температура'].values[0])
        period = int(self.dc.df.loc[self.dc.df['Имя'] == device.name, 'Период'].values[0])
        fl = int(self.dc.df.loc[self.dc.df['Имя'] == device.name, 'Уровень топлива'].values[0])
        client_assistant = BleakClientAssistant(device, period, temp, fl, loop)
        hk, lk, ul = await client_assistant.run()
        if hk == 0 and lk == 0 and ul == 0:
            self.queue_devices_to_connect.append(device)
            return 0
        else:
            self.dc.update_char(device.name, 'H', int(hk))
            self.dc.update_char(device.name, 'L', int(lk))
            self.dc.update_char(device.name, 'Уровень топлива после тарировки', int(ul))
            self.get_dataframe().to_excel('temp.xlsx')
            return 1


    async def queue_to_connection(self):
        while not len(self.queue_devices_to_connect) == 0:
            devices_to_connect = random.sample(self.queue_devices_to_connect, min(5, len(self.queue_devices_to_connect)))

            coros = [self.connect_device(device, self.loop) for device in devices_to_connect]
            tasks = [asyncio.create_task(coro) for coro in coros]  # Создаем задачи с помощью asyncio.create_task()

            try:
                done, pending = await asyncio.wait(tasks, timeout=60)  # Ожидаем выполнение задачи в течение 1 минуты
               # print(done)
            except asyncio.TimeoutError:
                print('autoclose')
                print(len(self.queue_devices_to_connect))
                for task in pending:
                    device = task.get_coro().cr_frame.f_locals['device']
                    if device not in self.queue_devices_to_connect:
                        self.queue_devices_to_connect.append(device)
                continue
            self.queue_devices_to_connect = list(set(self.queue_devices_to_connect) - set(devices_to_connect))
"""