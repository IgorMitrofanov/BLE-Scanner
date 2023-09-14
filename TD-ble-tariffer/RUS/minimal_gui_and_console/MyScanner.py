import os
from bleak import BleakScanner
import datetime
import asyncio
from DataCollector import DataCollector
from adv_decrypt import adv_decrypt
from colorama import init, Fore, Style


class MyScanner:
    """
    Инициализирует объект MyScanner.

    Параметры:
    - timeout: время (в секундах) сканирования устройств
    - start_serial: начальный серийный номер устройства
    - end_serial: конечный серийный номер устройства
    - device_type: тип устройства
    - TD_length (float): длина ДУТа
    - loop: объект asyncio event loop

    """
    def __init__(self, timeout, start_serial, end_serial, device_type, TD_length, loop):
        self._scanner = BleakScanner(detection_callback=self.detection_callback, loop=loop)
        self.scanning = asyncio.Event()
        self.timeout = timeout
        self.dc = DataCollector(start_serial, end_serial, device_type, TD_length)
        self.devices_to_connect = [] 
        self.retry_devices_list = []
        self.loop = loop
        self.device_type = device_type


    async def detection_callback(self, device, advertisement_data):
        """
        Callback-функция, вызываемая при обнаружении нового устройства.

        Параметры:
        - device: объект устройства
        - advertisement_data: данные рекламного пакета

        """
        try:
            if device.name in self.dc.device_names: 
                
                
                self.devices_to_connect.append(device)
            
                self.dc.device_names.remove(device.name)
            
                print(Fore.GREEN + f'Найдено устройство: {device.name} {self.dc.start_len-len(self.dc.device_names)}/{self.dc.start_len}'+ Style.RESET_ALL)


                self.dc.update_char(device.name, 'MAC', device.address)
                self.dc.update_char(device.name, 'RSSI', advertisement_data.rssi)

                oil_level_raw, battery_voltage, TD_temp_raw, version_raw, cnt_raw = adv_decrypt(advertisement_data.manufacturer_data[3862], device_type=self.device_type)

                self.dc.update_char(device.name, 'Напряжение батареи', battery_voltage)
                self.dc.update_char(device.name, 'Версия прошивки', version_raw)
                self.dc.update_char(device.name, 'Температура', TD_temp_raw)
                self.dc.update_char(device.name, 'Уровень топлива', oil_level_raw)
                self.dc.update_char(device.name, 'Период', cnt_raw)

        except Exception as e:
            #print(Fore.RED + f"Error in callback (scanner): {e}") # отладочный вывод
            pass


    async def run(self):
        """
        Запускает процесс сканирования устройств и выполнения других задач.

        Параметры:
        - timeout: время (в секундах) сканирования устройств
        """
        try:
            print(Style.RESET_ALL + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + Fore.GREEN + f'\t\tВыполняется сканирование в течение {self.timeout} секунд...')
            await self._scanner.start()
            self.scanning.set()
            end_time = self.loop.time() + self.timeout
            while self.scanning.is_set():
                if self.loop.time() > end_time or len(self.dc.device_names) == 0:
                    self.scanning.clear()
                    if len(self.dc.device_names) == 0:
                        print(Style.RESET_ALL + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + Fore.GREEN + '\t\tВсе устройства найдены.')
                        break
                    else:
                        print(Style.RESET_ALL + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + Fore.RED + f"\t\t Время сканирования вышло. Не все устройства найдены ({len(self.dc.device_names)*100/self.dc.start_len:.2f}%).")
                        print(Fore.RED + f'Не найденные устройства: {self.dc.device_names}' + Style.RESET_ALL)
                        answer = input(f"Хотите искать снова? (д/любая клавиша для нет): ").lower()
                        if answer == 'д':
                            self.scanning.set()
                            change_timeout = input(f"Хотите изменить время поиска? (д/любая клавиша для нет): ").lower()
                            if change_timeout == 'д':
                                try:
                                    new_timeout = int(input('Время сканирования (только целые числа): '))
                                    self.timeout = new_timeout
                                    end_time = self.loop.time() + self.timeout
                                    print(Style.RESET_ALL + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + Fore.GREEN + f'\t\tВыполняется сканирование в течение {self.timeout} секунд...')
                                except:
                                    print(Fore.RED + 'Время сканирования может быть только целочисленное!' + Style.RESET_ALL)
                                    new_timeout = int(input('Время сканирования (только целые числа): '))
                                    self.timeout = new_timeout
                                    end_time = self.loop.time() + self.timeout
                                    print(Style.RESET_ALL + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + Fore.GREEN + f'\t\tВыполняется сканирование в течение {self.timeout} секунд...')
                            else:
                                end_time = self.loop.time() + self.timeout
                                print(Style.RESET_ALL + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + Fore.GREEN + f'\t\tВыполняется сканирование в течение {self.timeout} секунд...')
                        else:
                            print(Style.RESET_ALL + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + Fore.RED + f"\t\tВремя сканирования вышло. Не найденные устройства: {self.dc.device_names}")
                else:
                    await asyncio.sleep(0)
            await asyncio.sleep(0)
            await self._scanner.stop()
            return self.devices_to_connect
        except Exception as e:
            #print(Fore.RED + f"Error in run (scanner): {e}") # отладочный вывод
            pass

async def run_scanner(self):
    # start_serial = int(input('Type start serial (only six numers): '))
    # end_serial = int(input('Type start serial (only six numers): '))
    # timeout = int(input('Type time in seconds for timeout scanning: '))
    my_scanner = MyScanner(timeout=10, start_serial=400043, end_serial=400052, device_type='TD', loop=loop)
    result = await my_scanner.run()
    return result


init()

async def main():
    result = await run_scanner()
    print(result)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.set_debug(True)
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())