import evdev
from evdev import ecodes, UInput

devices_map = {}

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

for device in devices:
    device_path = device.path
    device_number = device_path.split('/')[-1][5:]

    print(f"[{device_number}]: {device.name}")
    devices_map[device_number] = device


device_query = input("Select a device.\n--> ").strip()

if device_query in devices_map:
    print("Device found")

    device = devices_map[device_query]

    
    capabilities = {
        ecodes.EV_KEY: [ecodes.BTN_LEFT],
    }

    ui = UInput(capabilities)

    for event in device.read_loop():

        if event.type == ecodes.EV_KEY:

            if event.code == ecodes.BTN_SOUTH and event.value == 1:
                ui.write(ecodes.EV_KEY, ecodes.BTN_LEFT, 1)  # press
                ui.write(ecodes.EV_KEY, ecodes.BTN_LEFT, 0)  # release
                ui.syn()

else:
    print("Device unavailable")