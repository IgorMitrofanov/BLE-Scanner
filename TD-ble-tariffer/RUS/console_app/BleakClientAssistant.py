from bleak import BleakClient
from colorama import init, Fore, Style
import asyncio
import re
import datetime


init()


class BleakClientAssistant:
    """
    Описание класса BleakClientAssistant.

    Атрибуты:
    - fl (int): уровень топлива.
    - period (int): период.
    - temp (int): температура.
    - temp_corr (int): коэффициент термокоррекции.
    - device (str): строковый параметр, представляющий устройство (может быть TD и TH).
    - connected (bool): флаг, указывающий на состояние подключения.
    - hk (int): верхний уровень после тарировки.
    - lk (int): нижний уровень после тарировки.
    - ul (int): уровень топлива после тарировки.

    Методы:
    - __init__(self, fl, period, temp, temp_corr, device): конструктор класса.
    - run(self): метод, выполняющий подключение и отправку сообщения для тарировки.
    - notification_callback(self, sender, data): метод обратного вызова для обработки уведомлений.

    """
    def __init__(self, device, period, temp, fl, loop):
        """
        Конструктор класса ClassName.

        Параметры:
        - fl (int): уровень топлива.
        - period (int): период.
        - temp (int): температура.
        - temp_corr (int): коэффициент термокоррекции.
        - device (str): строковый параметр, представляющий устройство (может быть TD и TH).

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

        # Расчет коэффициента коррекции

        if temp >= 0:
            self.temp_corr = 6
        else:
            self.temp_corr = 11


    async def run(self):
        """
        Метод, выполняющий подключение и отправку сообщения для тарировки.

        Возвращает:
        - tuple: кортеж с значениями hk, lk, ul или ошибкой подключения.

        """
        # если датчик бракованный, то не тарировать
        if self.fl == 6500 or self.fl == 7000: 
                return 1, 1, 7000
        try:
            empty = int(self.period - self.temp_corr * self.temp + 50)
            full = int(2.03*(self.period - 9400) + 9400 - self.temp*(self.temp_corr-self.period / 2400))
            # сбор пакета для отправки
            data = b"SD, LK:1:%s, HK:1:%s" % (str(empty).encode(), str(full).encode())
            print(Fore.GREEN + f'Пытаюсь установить соединение с {self.device}...' )
            # Подключение к устройству и отправка сообщения с тарировочной командой
            async with BleakClient(self.device, timeout=60) as client:
                if client is not None and not self.connected:
                    await client.start_notify(14, self.notification_callback)
                    await client.write_gatt_char(12, data)
                    await client.write_gatt_char(12, b"GA\r") 
                    await asyncio.sleep(1)
                    self.connected = True
        except AttributeError as e:
            # костыль AtributeError для библиотеки bleak (в редких случаях возникает непонятная ошибка в самой библиотеке, если она появилось - дачик уже не сможет подключиться в этой сессии)
            self.hk = 10
            self.lk = 10
            self.ul = 10
        except Exception as e:
            #print(e, type(e)) отладочное сообщение
            pass
        finally:
            if self.hk and self.lk and self.ul is not None:
                print(Fore.GREEN + f'\t\tУстройство {self.device}: оттарировано!'+ Style.RESET_ALL)
                return self.hk, self.lk, self.ul
            else:
                print(Fore.RED + f'\t\tУстройство {self.device}: ошибка подключения!'+ Style.RESET_ALL)
                return 0, 0, 0


    def notification_callback(self, sender, data):
        """
        Метод обратного вызова для обработки уведомлений.

        Параметры:
        - sender: отправитель уведомления.
        - data: данные уведомления.
        
        """
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
        hk, lk, ul = loop.run_until_complete(client_assistant.run())
        print(hk, lk, ul)

