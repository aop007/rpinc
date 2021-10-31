#!/usr/bin/env python3

"""
Services
----------------
An example showing how to fetch all services and print them.
Updated on 2019-03-25 by hbldh <henrik.blidh@nedomkull.com>

Services for WH-1000XM3:

Services:
00001801-0000-1000-8000-00805f9b34fb (Handle: 1): Generic Attribute Profile
69a7f243-e52f-4443-a7f9-cb4d053c74d6 (Handle: 10): Unknown
fe59bfa8-7fe3-4a05-9d94-99fadc69faff (Handle: 18): Unknown
91c10d9c-aaef-42bd-b6d6-8a648c19213d (Handle: 31): Unknown
0000fe03-0000-1000-8000-00805f9b34fb (Handle: 44): Vendor specific
5b833e05-6bc7-4802-8e9a-723ceca4bd8f (Handle: 50): Unknown
5b833e06-6bc7-4802-8e9a-723ceca4bd8f (Handle: 58): Unknown


.. code-block:: bash

   bluetoothctl info "CC:98:8B:4A:70:57"

   Device CC:98:8B:4A:70:57 (public)
        Name: LE_WH-1000XM3
        Alias: LE_WH-1000XM3
        Class: 0x00240404
        Icon: audio-card
        Paired: yes
        Trusted: yes
        Blocked: no
        Connected: no
        LegacyPairing: no
        UUID: Vendor specific           (00000000-deca-fade-deca-deafdecacaff)
        UUID: Headset                   (00001108-0000-1000-8000-00805f9b34fb)
        UUID: Audio Sink                (0000110b-0000-1000-8000-00805f9b34fb)
        UUID: A/V Remote Control Target (0000110c-0000-1000-8000-00805f9b34fb)
        UUID: A/V Remote Control        (0000110e-0000-1000-8000-00805f9b34fb)
        UUID: Handsfree                 (0000111e-0000-1000-8000-00805f9b34fb)
        UUID: PnP Information           (00001200-0000-1000-8000-00805f9b34fb)
        UUID: Generic Access Profile    (00001800-0000-1000-8000-00805f9b34fb)
        UUID: Generic Attribute Profile (00001801-0000-1000-8000-00805f9b34fb)
        UUID: Unknown                   (0000fe03-0000-1000-8000-00805f9b34fb)
        UUID: Vendor specific           (5b833e05-6bc7-4802-8e9a-723ceca4bd8f)
        UUID: Vendor specific           (5b833e06-6bc7-4802-8e9a-723ceca4bd8f)
        UUID: Vendor specific           (69a7f243-e52f-4443-a7f9-cb4d053c74d6)
        UUID: Vendor specific           (7b265b0e-2232-4d45-bef4-bb8ae62f813d)
        UUID: Vendor specific           (81c2e72a-0591-443e-a1ff-05f988593351)
        UUID: Vendor specific           (91c10d9c-aaef-42bd-b6d6-8a648c19213d)
        UUID: Vendor specific           (931c7e8a-540f-4686-b798-e8df0a2ad9f7)
        UUID: Vendor specific           (96cc203e-5068-46ad-b32d-e316f5e069ba)
        UUID: Vendor specific           (b9b213ce-eeab-49e4-8fd9-aa478ed1b26b)
        UUID: Vendor specific           (f8d1fbe4-7966-4334-8024-ff96c9330e15)
        UUID: Vendor specific           (fe59bfa8-7fe3-4a05-9d94-99fadc69faff)
        Modalias: usb:v054Cp0CD3d0422
        ManufacturerData Key: 0x012d
        ManufacturerData Value:
  04 00 01 31 00 01 a2 7a c7 32 00 60 d0 00 00 00  ...1...z.2.`....
  00 00 00                                         ...


sound record: `mabdrabo/sound_recorder.py <https://gist.github.com/mabdrabo/8678538>`

"""

import sys
import asyncio
import platform

from bleak import BleakClient

ADDRESS = "CC:98:8B:4A:70:57"

if False:
    A2DP_SOURCE_UUID = "0000110a-0000-1000-8000-00805f9b34fb"
    A2DP_SINK_UUID = "0000110b-0000-1000-8000-00805f9b34fb"


    async def main(address: str):
        async with BleakClient(address) as client:
            svcs = await client.get_services()
            print("Services:")
            for service in svcs:
                print(service)


    if __name__ == "__main__":
        asyncio.run(main(sys.argv[1] if len(sys.argv) == 2 else ADDRESS))
    # end if
# end if

import sys

import bluetooth

if len(sys.argv) < 2:
    print("Usage: sdp-browse.py <addr>")
    print("   addr - can be a bluetooth address, \"localhost\", or \"all\"")
    sys.exit(2)

target = sys.argv[1]
if target == "all":
    target = None

services = bluetooth.find_service(address=target)

if len(services) > 0:
    print("Found {} services on {}.".format(len(services), sys.argv[1]))
else:
    print("No services found.")

for svc in services:
    print("\nService Name:", svc["name"])
    print("    Host:       ", svc["host"])
    print("    Description:", svc["description"])
    print("    Provided By:", svc["provider"])
    print("    Protocol:   ", svc["protocol"])
    print("    channel/PSM:", svc["port"])
    print("    svc classes:", svc["service-classes"])
    print("    profiles:   ", svc["profiles"])
    print("    service id: ", svc["service-id"])
