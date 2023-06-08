def adv_decrypt(data):
    # Расшифровка уровня топлива
    oil_level_raw = int.from_bytes(data[1:3], byteorder='little', signed=False)
    print(f"Oil level: {oil_level_raw}")

    # Расшифровка напряжения встроенной батареи
    battery_voltage_raw = int.from_bytes(data[3:4], byteorder='little', signed=False)
    battery_voltage = battery_voltage_raw / 10.0
    print(f"Battery voltage: {battery_voltage}V")

    # Расшифровка температуры
    TD_temp_raw = int.from_bytes(data[4:5], byteorder='little', signed=True)
    print(f"Temperature: {TD_temp_raw}°C")

    return oil_level_raw, battery_voltage, TD_temp_raw
