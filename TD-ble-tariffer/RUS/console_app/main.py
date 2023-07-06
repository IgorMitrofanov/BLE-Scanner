from Core import Core
import asyncio

async def core_program(loop, timeout, start_serial, end_serial, i):
    core = Core(loop, timeout=timeout, start_serial=start_serial, end_serial=end_serial, device_type='TD')
    await core.run_scanner()
    await core.queue_to_connection()
    await asyncio.sleep(1)
    print(core.my_scanner.dc.get_dataframe())
    core.my_scanner.dc.to_excel('C:/Users/User/Desktop/tariffy_test' + '/' + str(i) + 'tariffy_' + str(start_serial) + '-' + str(end_serial) + '.xlsx', core.atrribute_error_flag)

async def main(loop, timeout, start_serial, end_serial):
    for i in range(100):
        await core_program(loop, timeout, start_serial, end_serial, i)

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.set_debug(True)
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(loop, timeout=200, start_serial=400043, end_serial=400052))
