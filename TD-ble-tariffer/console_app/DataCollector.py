import os

try:
    import numpy as np
except:
    os.system('pip install numpy')
    import numpy as np

try:
    import pandas as pd
except:
    os.system('pip install pandas')

class DataCollector:
    def __init__(self, start_serial, end_serial, pattern):
        self.start_serial = start_serial
        self.end_serial = end_serial
        self.device_names = [pattern + str(i) for i in range(start_serial, end_serial+1)]
        self.start_len = len(self.device_names)
        self.df = pd.DataFrame({'Name': self.device_names, 
                                'MAC': [None] * len(self.device_names),
                                'RSSI': [None] * len(self.device_names),
                                'Oil Level' : [None] * len(self.device_names),
                                'Temperature': [None] * len(self.device_names),
                                'Battery Voltage': [None] * len(self.device_names),
                                'HK': [None] * len(self.device_names),
                                'LK': [None] * len(self.device_names)})
        
    def update_MAC(self, name, address):
        index = self.df.index[self.df['Name'] == name][0]
       # if self.df.at[index, 'MAC'] is None:   
        self.df.at[index, 'MAC'] = address
            
    def update_RSSI(self, name, RSSI):
        index = self.df.index[self.df['Name'] == name][0]
       # if self.df.at[index, 'RSSI'] is None:   
        self.df.at[index, 'RSSI'] = RSSI
            
    def update_oil_level(self, name, oil_level_raw):
        index = self.df.index[self.df['Name'] == name][0]
       # if self.df.at[index, 'Oil Level'] is None:   
        self.df.at[index, 'Oil Level'] = oil_level_raw
            
    def update_temp(self, name, TD_temp_raw):
        index = self.df.index[self.df['Name'] == name][0]
       # if self.df.at[index, 'Temperature'] is None:   
        self.df.at[index, 'Temperature'] = TD_temp_raw
            
    def update_battery_voltage(self, name, battery_voltage):
        index = self.df.index[self.df['Name'] == name][0]
        # if self.df.at[index, 'Battery Voltage'] is None:   
        self.df.at[index, 'Battery Voltage'] = battery_voltage
            
    def update_HK(self, name, hk):
        index = self.df.index[self.df['Name'] == name][0]
       # if self.df.at[index, 'HK'] is None:   
        self.df.at[index, 'HK'] = hk
            
    def update_LK(self, name, lk):
        index = self.df.index[self.df['Name'] == name][0]
       # if self.df.at[index, 'LK'] is None:   
        self.df.at[index, 'LK'] = lk
            
    def get_dataframe(self):
        return self.df
