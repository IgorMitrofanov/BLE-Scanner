# BLE-Scanner
## I.a Описание проекта
Разработка BLE-сканнера для отбраковки и калибровки выпускаемой продукции - датчиков TD (топливные) и TH (температура, давление, влажность, освещенность) - завершена.

Разработка велась на английском языке, позже программа была русифицирована. Репозиторий включает в себя русскую и английскую версию каждой из программ. К тому же есть как десктопная, так и консольная версия каждой из программ (кроме консольной advd-ble-collector на русском языке).

Целью проекта являлось:

1. Автоматизация процессов производства - ранее тарировка каждого датчика выполнялась с помощью смартфонов. Количество производимых датчиков составляет 20 тыс. ежемесячно, и это число постоянно растет.
2. Улучшение процесса отбраковки и калибровки датчиков - программа позволяет исключить человеческий фактор при отбраковке.

## I.b Project Description
The development of a BLE scanner for the sorting and calibration of TD (fuel) and TH (temperature, pressure, humidity, light) sensors has been completed.

The development was initially carried out in English and later localized into Russian. The repository includes both the Russian and English versions of each program. Additionally, there are both desktop and console versions of each program (except for the Russian console version advd-ble-collector).

The objectives of the project were:

1. Automation of production processes (previously, calibration of each sensor was done using smartphones, with 20,000 sensors produced monthly, and the number is increasing).
2. Improvement of the sorting and calibration process of the sensors (the program aims to eliminate human errors in sorting).

## II.a Программы
1. TD-ble-tariffer
Программа TD-ble-tariffer предназначена для отбраковки датчиков на этапе ОТК и последующей тарировки перед отпуском в продажу.

Технологии и библиотеки
- Python: язык программирования, на котором написана программа.

- os: модуль Python для работы с операционной системой.

- bleak: библиотека для работы с Bluetooth Low Energy (BLE) в Python.

- colorama: библиотека для добавления цвета и стиля в консольный вывод.

- asyncio: модуль Python для асинхронного программирования.

- re: модуль Python для работы с регулярными выражениями.

- datetime: модуль Python для работы с датой и временем.

- argparse: модуль Python для парсинга аргументов командной строки.

- sys: модуль Python для взаимодействия с интерпретатором и операционной системой.

- time: модуль Python для работы со временем.

- pandas: библиотека для обработки и анализа данных в Python.

- openpyxl: библиотека для работы с файлами Excel в Python.

- numpy: библиотека для работы с массивами и математическими функциями в Python.

Модули программы
- adv_decrypt.py: модуль для расшифровки данных advertisement-пакетов и вывода их на экран.

- BleakClientAssistant.py: модуль для подключения и отправки сообщений для тарировки с использованием библиотеки bleak.

- Core.py: модуль, содержащий основную логику программы.

- DataCollector.py: модуль, отвечающий за сбор данных.

- main.py: главный модуль программы, который инициализирует и запускает приложение.

- MyScanner.py: модуль, отвечающий за BLE-сканер и передачу данных в DataCollector.

2. advd-ble-collector
Программа advd-ble-collector предназначена для отбраковки датчиков на этапе монтажа.

Технологии и библиотеки

Список используемых технологий и библиотек для консольной версии программы TD-ble-tariffer для advd-ble-collector отличается только отсутствием подключения и калибровки для каждого из устройств.

README

В каждой из программ в соответствующей директории есть README.txt файл, в котором описаны:

1. Описание программы.
2. Поддерживаемые датчики.
3. Требования к системе.
4. Работа с программой.
5. Перечислены обновления при наличии.

## II.a Programs

1. TD-ble-tariffer: a program for sorting the sensors during the quality control stage and subsequent calibration before sale.
List of technologies and libraries used in the console version of TD-ble-tariffer program:

- Python: programming language used for writing the program.

- os: Python module for interacting with the operating system.

- bleak: library for working with Bluetooth Low Energy (BLE) in Python.

- colorama: library for adding color and style to console output.

- asyncio: Python module for asynchronous programming.

- re: Python module for working with regular expressions.

- datetime: Python module for working with date and time.

- argparse: Python module for parsing command-line arguments.

- sys: Python module for interacting with the interpreter and operating system.

- time: Python module for working with time.

- pandas: library for data processing and analysis in Python.

- openpyxl: library for working with Excel files in Python.

- numpy: library for working with arrays and mathematical functions in Python.

Modules of the console program TD-ble-tariffer:

- adv_decrypt.py: module for decrypting advertisement packet data and displaying it on the screen.

- BleakClientAssistant.py: module for connecting and sending messages for calibration using the bleak library.

- Core.py: module containing the main logic of the program.

- DataCollector.py: module responsible for data collection.

- main.py: main module of the program that initializes and runs the application.

- MyScanner.py: module responsible for BLE scanning and data transfer to DataCollector.

This is not an exhaustive list of technologies and libraries used, but it covers the main components and modules used in the console version of TD-ble-tariffer program. The desktop version differs in the presence of a window for entering input data, implemented using tkinter.

2. advd-ble-collector: a program for sorting the sensors during the assembly stage.
List of technologies and libraries used in the console version of TD-ble-tariffer program is similar, with the exception of the absence of connection and calibration for each device.

For each program, there is a README.txt file in the corresponding directory, which includes:

1. Program description.
2. Supported sensors.
3. System requirements.
4. Working with the program.
5. List of updates if available.



## III.a Контактная информация
- Telegram: https://t.me/igor_mtrfnv

## III.b Contact Information
- Telegram: https://t.me/igor_mtrfnv
