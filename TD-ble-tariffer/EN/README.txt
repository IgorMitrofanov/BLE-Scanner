--------------------
Program Description:
--------------------

The TD-BLE-tariffer program is a BLE scanner-collector of advertising packages and automatic calibration of the upper (H) and lower (L)
levels for TD sensors manufactured by Escort Monitoring Systems with the function of recording a report in MS Excel.

------------------
Supported sensors:
------------------

1. TD.

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

1. When starting the main.py file, the auxiliary window "Set the scan parameters:" appears, where you need to enter:
	1.1 Timeout - scan time in seconds (only integer values are accepted);
	1.2 Start serial - serial number of the first sensor;
	1.3 End serial - serial number of the last sensor;
	1.4 If necessary, select the "Create report" function to generate a report in MS Excel;
	1.5 If the "Create report" function is selected, the key for selecting the way to save the report is unlocked: "Path for report";
	1.6 Pressing the "Switch to scan mode" key will close the auxiliary window with the selection of parameters and switch to console mode;
2. In the console mode of operation, the requested devices are searched in dynamic mode, with output to the screen. There are two possible outcomes in the search:
	2.1 All devices found. A green message appears: "All devices have been found.", after which if the report recording function 
	    if enabled, the program will report that the report file has been recorded. Example: "File written to C:/Users/User/Desktop / with name output.xlsx ". If
	    the report recording function was not selected - a red text warning will appear indicating that the report recording function was not
	    selected: "Warning: the mode without recording the report was selected".
	2.2 Scan time expiration - not all devices were found: "Timeout. Can't find all devices.". In addition, the following line 
	    the program will output all the device names not found. The user will be prompted to start searching for devices not found during
the previous scan and change the timeout if necessary.
3. Four tests are performed in the report: 
	3.1 If the temperature of the sensor being tested differs from the average for all tested by more than 5 units up or down, the entire line 
	    marked in red, the corresponding reason is written in the "Reason for rejection" column.
	3.2 If the current fuel level after calibration is more than 15 units, the entire line is marked in red, in the column "Reason for rejection" is written 
	    the corresponding reason.
	3.3 If the upper (H) calibration level is greater than 43000 - the entire line is marked in red, in the column "Reason for rejection" is written 
	    the corresponding reason.
	3.4 If the lower (L) calibration level is less than 20000 - the entire row is marked in red, in the column "Reason for rejection" is written 
	    the corresponding reason.
	

--------------------------------------------------------------------------
Update 07.07.2023 of the dextop and console version of the TD-BLE-tariffer
--------------------------------------------------------------------------

1. Fixed the problem with the program hanging when connecting and calibrating devices;
	2. The check mark for creating a report has been removed, now the report is always generated;
	3. Fixed an error when highlighting defects in the report;
	4. Improved the logic of the program, the code is simplified and optimized;
	5. Added documentation to the code;