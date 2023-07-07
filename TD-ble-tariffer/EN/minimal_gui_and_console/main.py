import os
import sys

# Installing libraries on first launch

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
Differences from the console version in main.py and Core.py :
In the desktop version of main.py contains a minimal user interface, in the console version it is only the entry point to the program.
Core.py it differs only in the presence of argparse data from gui.
"""

class ScannerGUI:
    """
    Class for creating a graphical scanner interface
    """
    def __init__(self, master):
        """
        Initializing an object of the Scanner GUI class

        :param master: Parent window
        """
        self.master = master
        master.title("Setting scan parameters:")
        master.geometry("320x180+{}+{}".format(int(master.winfo_screenwidth()/2 - 400), int(master.winfo_screenheight()/2 - 300)))
        master.resizable(False, False)


        self.timeout_label = tk.Label(master, text="Timeout:")
        self.timeout_label.pack()
        self.timeout_entry = tk.Entry(master)
        self.timeout_entry.pack()
        self.timeout_entry.insert(0, "150")

        self.start_serial_label = tk.Label(master, text="Start serial:")
        self.start_serial_label.pack()
        self.start_serial_entry = tk.Entry(master)
        self.start_serial_entry.pack()
        self.start_serial_entry.insert(0, "400043")

        self.end_serial_label = tk.Label(master, text="End serial:")
        self.end_serial_label.pack()
        self.end_serial_entry = tk.Entry(master)
        self.end_serial_entry.pack()
        self.end_serial_entry.insert(0, "400052")

        self.select_report_path_button = tk.Button(master, text="Report path", command=self.select_report_path)
        self.select_report_path_button.pack()

        self.scan_button = tk.Button(master, text="Switch to scanning and calibration mode", command=self.start_scan)
        self.scan_button.pack()


    def select_report_path(self):
        """
        The method is called when the 'Path to Report' button is clicked
        and opens a dialog box to select the path to the report
        """
        file_path = filedialog.askdirectory()
        if file_path:
            self.report_path = file_path


    def start_scan(self):
        """
        The method is called when the 'Switch to scan and Calibration mode' button is pressed
        Checks whether the path to the report is selected. If not selected, it shows a pop-up window with a warning.
        Then it starts scanning and calibration.
        """
        timeout = int(self.timeout_entry.get())
        start_serial = int(self.start_serial_entry.get())
        end_serial = int(self.end_serial_entry.get())


        if not hasattr(self, "report_path"):
            tk.messagebox.showerror("Select the path", "To create a report, select the path to save it!")
            return

        self.master.destroy()

        current_dir = os.path.dirname(os.path.abspath(__file__))

        script_path = os.path.join(current_dir, "Core.py")

        subprocess.Popen(["python", script_path, str(start_serial), str(end_serial), str(timeout), self.report_path], creationflags=subprocess.CREATE_NEW_CONSOLE)


root = tk.Tk()
scanner_gui = ScannerGUI(root)
root.mainloop()