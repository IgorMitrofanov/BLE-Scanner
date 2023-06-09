import os

# Установка библиотек при первом запуске при необходимости

try:
    from bleak import BleakScanner
except:
    os.system('pip install bleak==0.20.2')
    from bleak import BleakScanner

try:
    import pandas as pd
except:
    os.system('pip install pandas==2.0.2')
    import pandas as pd

try:
    from openpyxl import Workbook
except:
    os.system('pip install openpyxl==3.1.2')

try:
    from colorama import init, Fore, Style
except:
    os.system('pip install colorama==0.4.6')


import asyncio
import datetime
import sys
import tkinter as tk
import tkinter as tk
from tkinter import filedialog
import subprocess


class ScannerGUI:
    def __init__(self, master):
        """
        Инициализирует объект ScannerGUI.

        Параметры:
        - master: родительское окно

        """
        self.master = master
        self.generate_report = False

        master.title("Установка параметров сканирования:")

        master.geometry("300x300+{}+{}".format(int(master.winfo_screenwidth()/2 - 400), int(master.winfo_screenheight()/2 - 300)))

        master.resizable(False, False)


        self.timeout_label = tk.Label(master, text="Время сканирования:")
        self.timeout_label.pack()
        self.timeout_entry = tk.Entry(master)
        self.timeout_entry.pack()
        self.timeout_entry.insert(0, "200")

        self.start_serial_label = tk.Label(master, text="Начальный серийный номер:")
        self.start_serial_label.pack()
        self.start_serial_entry = tk.Entry(master)
        self.start_serial_entry.pack()
        self.start_serial_entry.insert(0, "100001")

        self.end_serial_label = tk.Label(master, text="Конечный серийный номер:")
        self.end_serial_label.pack()
        self.end_serial_entry = tk.Entry(master)
        self.end_serial_entry.pack()
        self.end_serial_entry.insert(0, "100001")

        self.device_type_label = tk.Label(master, text="Тип датчка:")
        self.device_type_label.pack()

        self.device_type_var = tk.StringVar()
        self.device_type_var.set("TD")

        self.th_radiobutton = tk.Radiobutton(master, text="TD", variable=self.device_type_var, value="TD")
        self.th_radiobutton.pack()

        self.td_radiobutton = tk.Radiobutton(master, text="TH", variable=self.device_type_var, value="TH")
        self.td_radiobutton.pack()

        self.generate_report_var = tk.BooleanVar()
        self.generate_report_var.set(False)
        self.generate_report_checkbutton = tk.Checkbutton(master, text="Создать отчет", variable=self.generate_report_var, command=self.toggle_report)
        self.generate_report_checkbutton.pack()

        self.select_report_path_button = tk.Button(master, text="Путь для отчета", command=self.select_report_path, state="disabled")
        self.select_report_path_button.pack()

        self.scan_button = tk.Button(master, text="Перейти в режим сканирования", command=self.start_scan)
        self.scan_button.pack()


    def toggle_report(self):
        """
        Изменяет состояние генерации отчета.

        Если флаг генерации отчета был установлен, то он сбрасывается. Если флаг генерации отчета был сброшен, то он устанавливается.

        """
        self.generate_report = not self.generate_report

        if self.generate_report:
            self.select_report_path_button.config(state="normal")
        else:
            self.select_report_path_button.config(state="disabled")


    def select_report_path(self):
        """
        Открывает диалоговое окно для выбора пути для сохранения отчета.

        Возвращает:
        - путь к выбранной директории

        """
        file_path = filedialog.askdirectory()

        if file_path:
            self.report_path = file_path


    def start_scan(self):
        """
        Запускает сканирование с установленными параметрами.

        Получает значение таймаута из поля ввода и выполняет сканирование.

        """
        timeout = int(self.timeout_entry.get())
        start_serial = int(self.start_serial_entry.get())
        end_serial = int(self.end_serial_entry.get())
        device_type = self.device_type_var.get()

        generate_report = self.generate_report_var.get()

        if generate_report:
            if not hasattr(self, "report_path"):
                tk.messagebox.showerror("Выберите путь", "Для создания отчета нужно выбрать путь для его сохранения!")
                return

        self.master.destroy()

        current_dir = os.path.dirname(os.path.abspath(__file__))

        script_path = os.path.join(current_dir, "core.py")

        if generate_report:
            subprocess.Popen(["python", script_path, device_type, str(start_serial), str(end_serial), str(timeout), self.report_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen(["python", script_path, device_type, str(start_serial), str(end_serial), str(timeout), 'WITHOUT_WRITE'], creationflags=subprocess.CREATE_NEW_CONSOLE)


root = tk.Tk()
scanner_gui = ScannerGUI(root)
root.mainloop()
