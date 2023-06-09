import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QSpinBox, QPushButton, QFileDialog, QTextEdit, QVBoxLayout, QHBoxLayout, QLineEdit
from MyScanner import MyScanner
import asyncio

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ADVD-BLE-Collector")

        # Создаем виджеты
        self.label1 = QLabel("Выберите тип устройства:")
        self.combo_box = QComboBox()
        self.combo_box.addItem("TH")
        self.combo_box.addItem("TD")
        self.combo_box.setCurrentIndex(1)

        self.label2 = QLabel("Введите начальный серийный номер:")
        self.start_serial_spinbox = QSpinBox()
        self.start_serial_spinbox.setMinimum(0)
        self.start_serial_spinbox.setMaximum(999999)
        self.start_serial_spinbox.setValue(100001)

        self.label3 = QLabel("Введите конечный серийный номер:")
        self.end_serial_spinbox = QSpinBox()
        self.end_serial_spinbox.setMinimum(0)
        self.end_serial_spinbox.setMaximum(999999)
        self.end_serial_spinbox.setValue(100001)

        self.label4 = QLabel("Введите таймаут:")
        self.timeout_spinbox = QSpinBox()
        self.timeout_spinbox.setMinimum(1)
        self.timeout_spinbox.setMaximum(1000)

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
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        my_scanner = MyScanner(timeout=self.timeout, start_serial=self.start_serial, end_serial=self.end_serial, device_type=self.device_type, loop=loop)
        result = loop.run_until_complete(my_scanner.run())
        self.result_textedit.append(str(result))

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