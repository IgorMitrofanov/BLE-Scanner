from colorama import init, Fore, Style

# Инициализируем colorama
init()

# Выводим текст с разными цветами и стилями
print(Fore.RED + "Ошибка: не удалось подключиться к устройству")
print(Fore.GREEN + "Успех: устройство подключено")
print(Fore.YELLOW + "Предупреждение: низкий уровень заряда батареи")
print(Style.RESET_ALL + "Обычный текст")