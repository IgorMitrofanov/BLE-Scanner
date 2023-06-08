def adv_decrypt(data):
    oil_level_raw = int.from_bytes(data[1:3], byteorder='little', signed=False)
    print(f"Oil level: {oil_level_raw}")

    battery_voltage_raw = int.from_bytes(data[3:4], byteorder='little', signed=False)
    battery_voltage = battery_voltage_raw / 10.0
    print(f"Battery voltage: {battery_voltage}V")

    TD_temp_raw = int.from_bytes(data[4:5], byteorder='little', signed=True)
    print(f"Temperature: {TD_temp_raw}°C")

    version_raw = int.from_bytes(data[11:12], byteorder='big', signed=False)
    print(f"version: {version_raw}")

    cnt_raw = int.from_bytes(data[7:8], byteorder='big', signed=False)
    print(f"Period: {cnt_raw}")
        
    return oil_level_raw, battery_voltage, TD_temp_raw, version_raw, cnt_raw

