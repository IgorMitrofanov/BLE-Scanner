import asyncio
from MyScanner import MyScanner

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QSpinBox, QPushButton, QFileDialog, QTextEdit, QVBoxLayout, QHBoxLayout
from MyScanner import MyScanner

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Создаем виджеты
        self.label1 = QLabel("Выберите тип устройства:")
        self.combo_box = QComboBox()
        self.combo_box.addItem("TH")
        self.combo_box.addItem("TD")

        self.label2 = QLabel("Введите начальный серийный номер:")
        self.start_serial_spinbox = QSpinBox()
        self.start_serial_spinbox.setMinimum(0)
        self.start_serial_spinbox.setMaximum(999999)

        self.label3 = QLabel("Введите конечный серийный номер:")
        self.end_serial_spinbox = QSpinBox()
        self.end_serial_spinbox.setMinimum(0)
        self.end_serial_spinbox.setMaximum(999999)

        self.label4 = QLabel("Введите таймаут:")
        self.timeout_spinbox = QSpinBox()
        self.timeout_spinbox.setMinimum(1)
        self.timeout_spinbox.setMaximum(60)

        self.scan_button = QPushButton("Сканировать")
        self.scan_button.clicked.connect(self.scan_devices)

        self.result_textedit = QTextEdit()

        self.save_button = QPushButton("Сохранить логи")
        self.save_button.clicked.connect(self.save_logs)

        # Создаем вертикальный лейаут
        vbox = QVBoxLayout()

        # Добавляем виджеты в лейаут
        vbox.addWidget(self.label1)
        vbox.addWidget(self.combo_box)
        vbox.addWidget(self.label2)
        vbox.addWidget(self.start_serial_spinbox)
        vbox.addWidget(self.label3)
        vbox.addWidget(self.end_serial_spinbox)
        vbox.addWidget(self.label4)
        vbox.addWidget(self.timeout_spinbox)
        vbox.addWidget(self.scan_button)
        vbox.addWidget(self.result_textedit)

        # Создаем горизонтальный лейаут для кнопки сохранения логов
        hbox = QHBoxLayout()
        hbox.addWidget(self.save_button)
        hbox.addStretch()

        # Добавляем горизонтальный лейаут в вертикальный
        vbox.addLayout(hbox)

        # Устанавливаем лейаут для окна
        self.setLayout(vbox)

        # Переменные для сохранения выбранных значений
        self.device_type = None
        self.start_serial = None
        self.end_serial = None
        self.timeout = None

    def scan_devices(self):
        # Сохраняем выбранные значения
        self.device_type = self.combo_box.currentText()
        self.start_serial = self.start_serial_spinbox.value()
        self.end_serial = self.end_serial_spinbox.value()
        self.timeout = self.timeout_spinbox.value()

        # Запускаем сканирование устройств
        my_scanner = MyScanner(loop=asyncio.get_event_loop(), timeout=self.timeout, start_serial=self.start_serial, end_serial=self.end_serial, device_type=self.device_type)
        result = my_scanner.run()

        # Выводим результат в текстовое поле
        self.result_textedit.setText(str(result))

    def save_logs(self):
        # Выбираем папку для сохранения логов
        xls_path, _ = QFileDialog.getSaveFileName(self, "Выберите папку для сохранения логов", "", "Excel Files (*.xls)")

        # Сохраняем логи
        my_scanner = MyScanner(timeout=self.timeout, start_serial=self.start_serial, end_serial=self.end_serial, device_type=self.device_type)
        my_scanner.to_excel(xls_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())



'''

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    devices_type_list = ['1. TH', '2. TD']
    [print(device_type) for device_type in devices_type_list]
    device_type_num = int(input('Choice device type (1 or 2): '))
    if device_type_num == 1:
        device_type = 'TH'
    elif device_type_num == 2:
        device_type = 'TD'
    start_serial = int(input('Type start serial (only six numers): '))
    end_serial = int(input('Type end serial (only six numers): '))
    timeout = int(input('Type time in seconds for timeout scanning: '))
    my_scanner = MyScanner(timeout=timeout, start_serial=start_serial, end_serial=end_serial, device_type=device_type, loop=loop)
    loop.run_until_complete(my_scanner.run())
    print('\t\tData preview:')
    print(my_scanner.get_dataframe().head())
    write_or_not = input(f"Would you like to save data in xlsx? (Y for yes/ANY for no): ").lower()
    if write_or_not == 'y':
        path = str(input('Type path to excel file (example: C:/Users/User/Desktop/TH/): '))
        filename = str(input('Type name of excel file (example: 100001-100102): '))

        xls_path = path + filename + '.xlsx'

        my_scanner.to_excel(xls_path)
        print(f'File writed to {path} with name {filename}.xlsx')
        print('Program terminated.')
    else:
        print('Program terminated.')
'''