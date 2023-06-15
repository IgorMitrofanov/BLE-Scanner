import os

try:
    import pandas as pd
except:
    os.system('pip install pandas==2.0.2')
    import pandas as pd

try:
    from openpyxl import Workbook
except:
    os.system('pip install openpyxl==3.1.2')

class DataCollector:
    def __init__(self, start_serial, end_serial, device_type):
        self.start_serial = start_serial
        self.end_serial = end_serial
        self.device_names = [device_type + '_' + str(i) for i in range(start_serial, end_serial+1)]
        self.start_len = len(self.device_names)
        self.device_type = device_type

        if device_type == 'TD':

            self.df = pd.DataFrame({'Name': self.device_names, 
                                    'MAC': [None] * len(self.device_names),
                                    'RSSI': [None] * len(self.device_names),
                                    'version': [None] * len(self.device_names),
                                    'Battery Voltage': [None] * len(self.device_names),
                                    'Temperature': [None] * len(self.device_names),
                                    'Fuel Level' : [None] * len(self.device_names),
                                    'Period': [None] * len(self.device_names)})
        elif device_type == 'TH':
        
            self.df = pd.DataFrame({'Name': self.device_names, 
                                    'MAC': [None] * len(self.device_names),
                                    'RSSI': [None] * len(self.device_names),
                                    'version': [None] * len(self.device_names),
                                    'Battery Voltage': [None] * len(self.device_names),
                                    'Temperature': [None] * len(self.device_names),
                                    'Humidity': [None] * len(self.device_names),
                                    'Light' : [None] * len(self.device_names)})

    def update_char(self, device_name, char_name, value):
        index = self.df.index[self.df['Name'] == device_name][0]
        self.df.loc[index, char_name] = value
            
    def get_dataframe(self):
        return self.df
