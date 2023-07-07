from MyScanner import MyScanner
from BleakClientAssistant import BleakClientAssistant
import asyncio
import random
import datetime
from colorama import init, Fore, Style


init()


class Core:
    """
    Описание класса Core. Это ядро программы.

    Атрибуты:
    - loop (asyncio.AbstractEventLoop): объект цикла событий async.
    - devices_to_connect (list): список устройств для подключения.
    - my_scanner (MyScanner): экземпляр класса MyScanner для сканирования устройств.

    Методы:
    - __init__(self, loop, timeout, start_serial, end_serial, device_type): конструктор класса.
    - run_scanner(self): метод для запуска сканирования устройств.
    - connect_device(self, device): метод для подключения к устройству и тарировки.
    - queue_to_connection(self): метод для организации очереди подключения.

    """
    def __init__(self, loop, timeout, start_serial, end_serial, device_type):
        """
        Конструктор класса Core.

        Параметры:
        - loop (asyncio.AbstractEventLoop): объект цикла событий async.
        - timeout (int): таймаут для сканирования устройств.
        - start_serial (str): начальный серийный номер для сканирования устройств.
        - end_serial (str): конечный серийный номер для сканирования устройств.
        - device_type (str): тип устройства для сканирования.
        - atrribute_error_flag (bool) костыль для библиотеки bleak
        """
        self.loop = loop
        self.devices_to_connect = []
        self.my_scanner = MyScanner(timeout=timeout, start_serial=start_serial, end_serial=end_serial, device_type=device_type, loop=loop)
        self.atrribute_error_flag = False

    async def run_scanner(self):
        """
        Метод для запуска сканирования устройств.

        Возвращает:
        - list: список устройств для подключения.
        """
        self.devices_to_connect = await self.my_scanner.run() 
        return self.devices_to_connect


    async def connect_device(self, device):
            """
            Метод для подключения к устройству.

            Параметры:
            - device: устройство для подключения.

            Возвращает:
            1 в случае успеха, 0 в случае неудачи.
            """
            try:
                # получение необходимых параметров для расчета верхнего и нижнего тарировочного значения
                temp = int(self.my_scanner.dc.df.loc[self.my_scanner.dc.df['Имя'] == device.name, 'Температура'].values[0])
                period = int(self.my_scanner.dc.df.loc[self.my_scanner.dc.df['Имя'] == device.name, 'Период'].values[0])
                fl = int(self.my_scanner.dc.df.loc[self.my_scanner.dc.df['Имя'] == device.name, 'Уровень топлива'].values[0])
                # инициализация клиента для подключения и тарировки
                client_assistant = BleakClientAssistant(device, period, temp, fl, self.loop)
                hk, lk, ul = await client_assistant.run()
                # если тарировку провести не удалось
                if hk == 0 and lk == 0 and ul == 0:
                    self.devices_to_connect.append(device)
                    return 0
                # костыль для библиотеки bleak
                elif hk == 10 and lk == 10 and ul == 10:
                    print(Fore.YELLOW + f'Не удалось провести тарировку {device}, требуется перезапуск программы.')
                    self.atrribute_error_flag = True
                    return 0
                # если тарировка прошла успешно - пишем параметры в объект DataCollector
                else:
                    self.my_scanner.dc.update_char(device.name, 'H', int(hk))
                    self.my_scanner.dc.update_char(device.name, 'L', int(lk))
                    self.my_scanner.dc.update_char(device.name, 'Уровень топлива после тарировки', int(ul))
                    # self.my_scanner.dc.get_dataframe().to_excel('temp.xlsx') # Если потребуется сохранение временного файла после каждой тарировки
                    return 1
            except Exception as e:
                #print(e) # отладочный вывод 
                pass


    async def queue_to_connection(self):
            """
            Метод для организации очереди подключения.
            """
            while not len(self.devices_to_connect) == 0: 
                random_device = random.choice(self.devices_to_connect)
                self.devices_to_connect.remove(random_device)
                coro = self.connect_device(random_device)
                task = asyncio.create_task(coro)
                print(Style.RESET_ALL + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + Fore.GREEN + f'\t\tСчетчик успешных тарировок: {self.my_scanner.dc.start_len-len(self.devices_to_connect)-1}/{self.my_scanner.dc.start_len}')
                try:
                    # Запускаем задачу с вачдогом в 30 секунд
                    done, pending = await asyncio.wait([task], timeout=30) 
                except asyncio.TimeoutError:
                    # Если вачдог сработал, возвращаем устройство назад в список для подключения
                    self.devices_to_connect.append(random_device)

async def core_program(loop, i):
    core = Core(loop, timeout=120, start_serial=400043, end_serial=400052, device_type='TD')
    await core.run_scanner()
    await core.queue_to_connection()
    await asyncio.sleep(1)
    print(core.my_scanner.dc.get_dataframe())
    core.my_scanner.dc.to_excel(str(i)+'.xlsx', core.atrribute_error_flag)

async def main(loop):
    for i in range(0, 100):
        await core_program(loop, i)

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.set_debug(True)
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(loop))