import os
import sys

# Установка библиотек при первом запуске

try:
    import openpyxl
    from openpyxl.styles import PatternFill, Font
except:
    os.system('pip install openpyxl==3.1.2')

try:
    from bleak import BleakClient


except:
    os.system('pip install bleak')
    from bleak import BleakClient

try:
    from bleak import BleakScanner
except:
    os.system('pip install bleak==0.20.2')


try:
    from colorama import init, Fore, Style
except:
    os.system('pip install colorama==0.4.6')


try:
    import pandas as pd
except:
    os.system('pip install pandas==2.0.2')
    import pandas as pd

import tkinter as tk
import tkinter as tk
from tkinter import filedialog

import subprocess

"""
Отличия от консольной версии в main.py и Core.py:
В десктоп версии main.py содержит минимальный пользовательский интерфейс, в консольной версии это только точка входа в программу.
Core.py отличается только наличием argparse данных с гуи.

"""

class ScannerGUI:
    """
    Класс для создания графического интерфейса сканера
    
    """
    def __init__(self, master):
        """
        Инициализация объекта класса ScannerGUI

        :param master: Родительское окно 

        """
        self.master = master
        master.title("Установка параметров сканирования:")
        master.geometry("320x300+{}+{}".format(int(master.winfo_screenwidth()/2 - 400), int(master.winfo_screenheight()/2 - 300)))
        master.resizable(False, False)


        self.timeout_label = tk.Label(master, text="Время сканирования:")
        self.timeout_label.pack()
        self.timeout_entry = tk.Entry(master)
        self.timeout_entry.pack()
        self.timeout_entry.insert(0, "150")

        self.start_serial_label = tk.Label(master, text="Начальный серийный номер:")
        self.start_serial_label.pack()
        self.start_serial_entry = tk.Entry(master)
        self.start_serial_entry.pack()
        self.start_serial_entry.insert(0, "400043")

        self.end_serial_label = tk.Label(master, text="Конечный серийный номер:")
        self.end_serial_label.pack()
        self.end_serial_entry = tk.Entry(master)
        self.end_serial_entry.pack()
        self.end_serial_entry.insert(0, "400052")

        self.length_label = tk.Label(master, text="Длина ДУТа:")
        self.length_label.pack()

        self.TD_length = tk.StringVar(value="1 м")
        self.length_options = ["1 м", "1.5 м", "2 м", "3 м"]
        for option in self.length_options:
            rb = tk.Radiobutton(master, text=option, variable=self.TD_length, value=option)
            rb.pack()

        self.select_report_path_button = tk.Button(master, text="Путь к отчету", command=self.select_report_path)
        self.select_report_path_button.pack()

        self.scan_button = tk.Button(master, text="Перейти в режим сканирования и тарировки", command=self.start_scan)
        self.scan_button.pack()


    def select_report_path(self):
        """
        Метод вызывается при нажатии кнопки 'Путь к отчету'
        и открывает диалоговое окно для выбора пути к отчету

        """
        file_path = filedialog.askdirectory()
        if file_path:
            self.report_path = file_path


    def start_scan(self):
        """
        Метод вызывается при нажатии кнопки 'Перейти в режим сканирования и тарировки'
        Проверяет, выбран ли путь к отчету. Если не выбран, показывает всплывающее окно с предупреждением.
        Затем запускает сканирование и тарировку.

        """
        timeout = int(self.timeout_entry.get())
        start_serial = int(self.start_serial_entry.get())
        end_serial = int(self.end_serial_entry.get())
        TD_length = float(self.TD_length.get().split()[0])


        if not hasattr(self, "report_path"):
            tk.messagebox.showerror("Выберите путь", "Для создания отчета нужно выбрать путь для его сохранения!")
            return

        self.master.destroy()

        current_dir = os.path.dirname(os.path.abspath(__file__))

        script_path = os.path.join(current_dir, "Core.py")

        subprocess.Popen(["python", script_path, str(start_serial), str(end_serial), str(timeout), self.report_path], creationflags=subprocess.CREATE_NEW_CONSOLE)


root = tk.Tk()
scanner_gui = ScannerGUI(root)
root.mainloop()
