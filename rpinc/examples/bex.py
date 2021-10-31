#!/usr/bin/env python3

import asyncio
from bleak import BleakScanner, BleakClient

MODEL_NBR_UUID = '00002a24-0000-1000-8000-00805f9b34fb'

async def show_devices():
    devices = await BleakScanner.discover()

    for d in devices:
        print(d)

async def get_model(address: str):
    async with BleakClient(address) as client:
        model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        print(f"Model for {address}: {model_number}")


# asyncio.run(show_devices())


asyncio.run(get_model('CC:98:8B:4A:70:57'))
