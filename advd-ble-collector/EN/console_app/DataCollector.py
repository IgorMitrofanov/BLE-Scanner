import os
import numpy as np
import pandas as pd


class DataCollector:
    """
    Description of the Data Collector class.

    Attributes:
    - start_serial (int): the initial serial number.
    - end_serial (int): the final serial number.
    - device_names (list): a list of device names.
    - start_len (int): the initial length of the device list.
    - device_type (str): device type.

    Methods:
    - __init__(self, start_serial, end_serial, device_type): class constructor.
    - update_char(self, device_name, char_name, value): method for updating the characteristic value.
    - - get_data frame(self): a method for getting data in the form of a pandas DataFrame.
    - to_excel(self, xls_path): a method for saving data to an Excel file.
    """
    def __init__(self, start_serial, end_serial, device_type):
        """
        Constructor of the Data Collector class.

        Parameters:
        - start_serial (int): the initial serial number.
        - end_serial (int): the final serial number.
        - device_type (str): device type.
        """
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
                                    'Oil Level' : [None] * len(self.device_names)})
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
        """
        Method for updating the characteristic value.

        Parameters:
        - device_name (str): device name.
        - char_name (str): the name of the characteristic.
        - value: the new value of the characteristic.
        """
        index = self.df.index[self.df['Name'] == device_name][0]
        self.df.loc[index, char_name] = value
            
            
    def get_dataframe(self):
        """
        Method for getting data in the form of pandas DataFrame.

        Returns:
        - pandas.DataFrame: data in the form of a DataFrame.
        """ 
        return self.df
