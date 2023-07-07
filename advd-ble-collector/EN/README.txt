--------------------
Program Description:
--------------------

The advd-ble-collector program is a BLE scanner-collector of advertising packages for two types of sensors produced
by Escort Monitoring Systems with the function of recording a report in MS Excel.

------------------
Supported sensors:
------------------

1. TD;
2. TH.

--------------------
System Requirements:
--------------------

1. Windows 10, version 16299 (Fall Creators Update) or higher;
2. Python 3.11 or higher;
	2.1. To install the latest version of Python, follow the link (when installing, set the "Add" flag python.exe to Path"): https://www.python.org/downloads/
2.2 Instructions for installing pip in environment variables: https://www.activestate.com/resources/quick-reads/how-to-install-pip-on-windows/
3. Bluetooth 4.0 or higher;
4. Internet access is required at the first launch of the program. At the first launch, the program installs its dependencies and closes, a restart is required.

-------------------------
Working with the program:
-------------------------

1. When starting the main.py file, the auxiliary window "Setting scan parameters:" appears, where you need to enter:
	1.1 Scan time in seconds (only integer values are accepted);
	1.2 Initial serial number - the serial number of the first sensor;
	1.3 Final serial number - the serial number of the last sensor;
	1.4 If necessary, select the "Create Report" function to generate a report in MS Excel;
	1.5 If the "Create report" function is selected, the key for selecting the way to save the report is unlocked: "Path for report";
	1.6 Pressing the "Switch to Scan mode" key will close the auxiliary window with the selection of parameters and switch to console mode;
2. In the console mode of operation, the requested devices are searched in dynamic mode, with output to the screen. There are two possible outcomes in the search:
	2.1 All devices found. A green message appears: "All devices have been found.", after which if the report recording function 
	    if enabled, the program will report that the report file has been recorded. Example: "The file is written to the directory C:/Users/User/Desktop / with the name collected_X-Y.xlsx " (where X is the serial number of the first sensor and Y is the last one). If
	    the report recording function was not selected - a red text warning will appear indicating that the report recording function was not
	    selected: "warning: the mode without recording the report was selected."
2.2 Scan time elapsed - not all devices were found: "Time is up. Not all devices were found.". In addition, the following line 
	    the program will output all the device names not found. The user will be prompted to start searching for devices not found during
the previous scan and change the scan time if necessary.
3. Two tests are carried out in the report:
3.1 If the fuel level is equal to 6500 or 7000, the entire line is marked in red, the corresponding reason is written in the "Reason for rejection" column.
	3.2 If the current signal level is less than 20000, the entire line is marked in red, the corresponding reason is written in the "Reason for rejection" column.