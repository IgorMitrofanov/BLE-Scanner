import asyncio
from MyScanner import MyScanner


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    devices_type_list = ['1. TH', '2. TD']
    [print(device_type) for device_type in devices_type_list]
    device_type_num = int(input('Choice device type (1 or 2): '))
    if device_type_num == 1:
        device_type = 'TH'
    elif device_type_num == 2:
        device_type = 'TD'
    start_serial = int(input('Type start serial (only six numers): '))
    end_serial = int(input('Type end serial (only six numers): '))
    timeout = int(input('Type time in seconds for timeout scanning: '))
    my_scanner = MyScanner(timeout=timeout, start_serial=start_serial, end_serial=end_serial, device_type=device_type, loop=loop)
    loop.run_until_complete(my_scanner.run())
    print('\t\tData preview:')
    print(my_scanner.get_dataframe().head())
    write_or_not = input(f"Would you like to save data in xlsx? (Y for yes/ANY for no): ").lower()
    if write_or_not == 'y':
        path = str(input('Type path to excel file (example: C:/Users/User/Desktop/TH/): '))
        filename = str(input('Type name of excel file (example: 100001-100102): '))

        xls_path = path + filename + '.xlsx'

        my_scanner.to_excel(xls_path)
        print(f'File writed to {path} with name {filename}.xlsx')
        print('Program terminated.')
    else:
        print('Program terminated.')
