import os
from adbutils import adb

class DeviceDebug:
    def __init__(self):
        pass
    
    def get_devices(self):
        # Lấy thông tin toàn bộ các thiết bị
        devices = adb.device_list()
        listDevices = {}
        for i in devices:
            os.system(f'adb -s {i.serial} shell input keyevent 3')
            platformVersion = os.popen(f'adb -s {i.serial} shell getprop ro.build.version.release').read().split()[0]
            deviceName = os.popen(f'adb -s {i.serial} shell getprop ro.product.model').read().split()[0]
            result = os.popen(f'adb -s {i.serial} shell "dumpsys activity activities | grep mResumedActivity"').read().replace(' ', '+')
            pack_and_act = result.replace(' ', '+').split('+com.')[1].split('+')[0]
            appPackage = 'com.' + pack_and_act.split('/')[0]
            appActivity = pack_and_act.split('/')[1]
            listDevices[i.serial] = {
                'platformVersion': platformVersion,
                'deviceName': deviceName,
                'appPackage': appPackage,
                'appActivity': appActivity,
                'udid': i.serial
            }
        return listDevices
    
    def check_exits(self, device_id, appPackage):
        result = os.popen(f'adb -s {device_id} shell pm list packages').read()
        if not appPackage in result:
            return False
        return True
    
    def install_APK(self, device_id, apk_path):
        os.system(f'adb -s {device_id} install "{apk_path}"')

    



class LD_Player:
    def __init__(self, path) -> None:
        # Khai báo đường dẫn LD Player
        # D:\LDPlayer\LDPlayer9\dnconsole.exe
        self.path = path
    
    def shell(self, command:str):
        # thực thi lệnh
        os.system(f'{self.path} {command}')

    def add_device(self, name):
        # Thêm thiết bị
        self.shell(f'add --name {name}')

    def copy_device(self, name, soucre_device):
        # Sao chép thiết bị
        self.shell(f'copy --name {name} --from {soucre_device}')
    
    def remove_device(self, name):
        # Xóa thiết bị
        self.shell(f'remove --name {name}')

    def fast_sort(self):
        # Auto sắp xếp
        self.shell('sortWnd')
    
