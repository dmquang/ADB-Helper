from adb_helper import ADBHelper

device_id = "emulate-5556"
helper = ADBHelper(device_id)

print(helper.get_devices())