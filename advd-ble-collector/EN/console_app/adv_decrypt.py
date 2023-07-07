def adv_decrypt(data, device_type):
    """
    Sends out these advertising packages, outputs and uploads as an advertiser.

    Arguments:
        Data (bytes): Encrypted data from which to extract information.
        device_type (str): The type of device for which data is being installed.

    Returns:
    Depending on the type of devices:
    TD: oil_level_low, battery_voltage, TD_temp_raw, version_raw, cnt_raw
    TH: TH09_temp, TH09_light_raw, TH09_humidity, TH09_battery, TH09_version_raw
    """
    if device_type == "TD":
        
        oil_level_raw = int.from_bytes(data[1:3], byteorder='little', signed=False)
        print(f"Oil level: {oil_level_raw}")

        battery_voltage_raw = int.from_bytes(data[3:4], byteorder='little', signed=False)
        battery_voltage = battery_voltage_raw / 10.0
        print(f"Battery voltage: {battery_voltage}V")

        TD_temp_raw = int.from_bytes(data[4:5], byteorder='little', signed=True)
        print(f"Temperature: {TD_temp_raw}°C")

        version_raw = int.from_bytes(data[11:12], byteorder='big', signed=False)
        print(f"version: {version_raw}")
        
        return oil_level_raw, battery_voltage, TD_temp_raw, version_raw

    elif device_type == "TH":
        TH09_temp_raw = int.from_bytes(data[1:3], byteorder='little', signed=True)
        TH09_temp = TH09_temp_raw / 10.0
        print(f"Temperature: {TH09_temp}°C")

        TH09_light_raw = int.from_bytes(data[3:5], byteorder='little', signed=False)
        print(f"Illumination: {TH09_light_raw} lux")

        TH09_humidity_raw = int.from_bytes(data[5:7], byteorder='little', signed=False)
        TH09_humidity = TH09_humidity_raw / 10.0
        print(f"Humidity: {TH09_humidity}%")

        TH09_battery_raw = int.from_bytes(data[10:11], byteorder='big', signed=False)
        TH09_battery = TH09_battery_raw / 10.0
        print(f"Battery voltage: {TH09_battery}V")

        TH09_version_raw = int.from_bytes(data[11:12], byteorder='big', signed=False)
        print(f"version: {TH09_version_raw}")

        return TH09_temp, TH09_light_raw, TH09_humidity, TH09_battery, TH09_version_raw