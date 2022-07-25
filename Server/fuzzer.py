import random
from bleak import BleakClient
import asyncio

address="A4:06:E9:79:ED:16"
#channel to write to 
CUSTOM_DATA_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"

class BluetoothClient:
    async def send_signal(self,ble):
        # send code to bluetooth
        random_value= random.randrange(0, 255)
        await ble.write_gatt_char(CUSTOM_DATA_UUID, bytes([random_value]))
        print(random_value)

    
    async def bluetooth_main(self,address):
        async with BleakClient(address) as client:
            while True:
                await self.send_signal(client)


bluetooth= BluetoothClient()
asyncio.run(bluetooth.bluetooth_main(address))









    
    

