def adv_decrypt(data, device_type):
        
    if device_type == 'TD':

        battery_voltage_raw = int.from_bytes(data[3:4], byteorder='little', signed=False)
        battery_voltage = battery_voltage_raw / 10.0
        print(f"Напряжение батареи: {battery_voltage}В")

        version_raw = int.from_bytes(data[5:6], byteorder='big', signed=False)
        print(f"Версия прошивки: {version_raw}")

        TD_temp_raw = int.from_bytes(data[4:5], byteorder='little', signed=True)
        print(f"Температура: {TD_temp_raw}°C")

        oil_level_raw = int.from_bytes(data[1:3], byteorder='little', signed=False)
        print(f"Уровень топлива: {oil_level_raw}")

        cnt_raw = int.from_bytes(data[6:10], byteorder='little', signed=False)
        print(f"Период: {cnt_raw}")
        
        return oil_level_raw, battery_voltage, TD_temp_raw, version_raw, cnt_raw

    elif device_type == "TH":

        TH09_battery_raw = int.from_bytes(data[10:11], byteorder='big', signed=False)
        TH09_battery = TH09_battery_raw / 10.0
        print(f"Напряжение батареи: {TH09_battery}V")

        TH09_version_raw = int.from_bytes(data[11:12], byteorder='big', signed=False)
        print(f"Версия прошивки: {TH09_version_raw}")

        TH09_temp_raw = int.from_bytes(data[1:3], byteorder='little', signed=True)
        TH09_temp = TH09_temp_raw / 10.0
        print(f"Температура: {TH09_temp}°C")

        TH09_humidity_raw = int.from_bytes(data[5:7], byteorder='little', signed=False)
        TH09_humidity = TH09_humidity_raw / 10.0
        print(f"Влажность: {TH09_humidity}%")

        TH09_light_raw = int.from_bytes(data[3:5], byteorder='little', signed=False)
        print(f"Освещенность: {TH09_light_raw} люкс")

        return TH09_temp, TH09_light_raw, TH09_humidity, TH09_battery, TH09_version_raw