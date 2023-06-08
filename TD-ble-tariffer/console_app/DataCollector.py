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
                                    'version': [None] * len(self.device_names),
                                    'Battery Voltage': [None] * len(self.device_names),
                                    'Temperature': [None] * len(self.device_names),
                                    'Oil Level' : [None] * len(self.device_names),
                                    'Period': [None] * len(self.device_names)})
        
    def update_char(self, device_name, char_name, value):
        index = self.df.index[self.df['Name'] == device_name][0]
        self.df.loc[index, char_name] = value
            
    def get_dataframe(self):
        return self.df
