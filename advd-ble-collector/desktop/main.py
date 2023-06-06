import pandas as pd
import tkinter as tk
from MyScanner import MyScanner
import asyncio

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.device_type_label = tk.Label(self, text="Device type:")
        self.device_type_label.pack(side="left")
        self.device_type_var = tk.StringVar(value="TH")
        self.device_type_entry = tk.Entry(self, textvariable=self.device_type_var)
        self.device_type_entry.pack(side="left")

        self.start_serial_label = tk.Label(self, text="Start serial:")
        self.start_serial_label.pack(side="left")
        self.start_serial_var = tk.StringVar(value="100001")
        self.start_serial_entry = tk.Entry(self, textvariable=self.start_serial_var)
        self.start_serial_entry.pack(side="left")

        self.end_serial_label = tk.Label(self, text="End serial:")
        self.end_serial_label.pack(side="left")
        self.end_serial_var = tk.StringVar(value="100102")
        self.end_serial_entry = tk.Entry(self, textvariable=self.end_serial_var)
        self.end_serial_entry.pack(side="left")

        self.timeout_label = tk.Label(self, text="Timeout:")
        self.timeout_label.pack(side="left")
        self.timeout_var = tk.StringVar(value="10")
        self.timeout_entry = tk.Entry(self, textvariable=self.timeout_var)
        self.timeout_entry.pack(side="left")

        self.scan_button = tk.Button(self, text="Scan", command=self.scan)
        self.scan_button.pack(side="left")

        self.quit_button = tk.Button(self, text="Quit", command=self.master.destroy)
        self.quit_button.pack(side="right")

    def scan(self):
        device_type = self.device_type_var.get()
        start_serial = int(self.start_serial_var.get())
        end_serial = int(self.end_serial_var.get())
        timeout = int(self.timeout_var.get())
        loop = asyncio.new_event_loop()
        my_scanner = MyScanner(timeout=timeout, start_serial=start_serial, end_serial=end_serial, device_type=device_type, loop=loop)
        loop.run_until_complete(my_scanner.run())

        data = my_scanner.get_dataframe()

        write_or_not = input(f"Would you like to save data in xlsx? (Y for yes/ANY for no): ").lower()
        if write_or_not == 'y':
            path = str(input('Type path to excel file (example: C:/Users/User/Desktop/TH/): '))
            filename = str(input('Type name of excel file (example: 100001-100102): '))

            xls_path = path + filename + '.xlsx'

            data.to_excel(xls_path)
            print(f'File writed to {path} with name {filename}.xlsx')
            print('Program terminated.')
        else:
            print('Program terminated.')

root = tk.Tk()
app = Application(master=root)
app.mainloop()


'''
import asyncio
from MyScanner import MyScanner


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