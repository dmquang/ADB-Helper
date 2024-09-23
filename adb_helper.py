from adbutils import adb
import os, subprocess, cv2, re
import xml.etree.ElementTree as ET

class ADBHelper:
    def __init__(self):
        pass
    
    def get_devices(self) -> list:
        # Lấy thông tin toàn bộ các thiết bị
        devices = adb.device_list()
        listDevices = {}
        for i in devices:
            os.system(f'adb -s {i.serial} shell input keyevent 3')
            platformVersion = subprocess.run(f'adb -s {i.serial} shell getprop ro.build.version.release', text=True, stdout=subprocess.PIPE).stdout.split()[0]
            deviceName = subprocess.run(f'adb -s {i.serial} shell getprop ro.product.model', text=True, stdout=subprocess.PIPE).stdout.split()[0]
            result = subprocess.run(f'adb -s {i.serial} shell "dumpsys activity activities | grep mResumedActivity"', text=True, stdout=subprocess.PIPE).stdout.replace(' ', '+')
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
    
    def install_APK(self, device_id, apk_path):
        # Cài đặt file APK
        subprocess.run(f'adb -s {device_id} install "{apk_path}"', text=True, stdout=subprocess.PIPE).stdout
        return
    
    def check_exits(self, device_id, appPackage):
        # Kiểm tra nếu ứng dụng đã được cài đặt trên thiết bị
        result = subprocess.run(f'adb -s {device_id} shell pm list packages', text=True, stdout=subprocess.PIPE).stdout
        if not appPackage in result:
            return False
        return True

    def open_app(self, device_id, appPackage, appActivity) -> str:
        # Mở ứng dụng trên thiết bị
        result = subprocess.run(f'adb -s {device_id} shell am start -n {appPackage}/{appActivity}', text=True, stdout=subprocess.PIPE).stdout
        return result

    def transfer_media(self, device_id, media_path) -> str:
        # Chuyển toàn bộ 1 thư mục media sang thiết bị
        transfer = subprocess.run(f'adb -s {device_id} push "{media_path}" /sdcard/Pictures/', text=True, stdout=subprocess.PIPE).stdout.strip().split(': ')[1]
        return transfer # 90 files pushed, 0 skipped. 9.6 MB/s (5063214 bytes in 0.504s)

    def click_screen(self, device_id, coordinates:tuple) -> bool:
        # Click vào một vị trí trên màn hình thiết bị theo toạ độ
        # coordinates: (x, y)
        xtap, ytap = coordinates
        result = subprocess.run(f'adb -s {device_id} shell input tap {xtap} {ytap}', text=True, stdout=subprocess.PIPE).stdout
        return True
    
    def swipe_screen(self, device_id, start_coordinates:tuple, end_coordinates:tuple, duration:int) -> bool:
        # Thực hiện thao tác vuốt màn hình từ một vị trí đến một vị trí khác trên thiết bị Android. Thời gian thực hiện vuốt được điều chỉnh bằng tham số duration.
        xtap1, ytap1 = start_coordinates
        xtap2, ytap2 = end_coordinates
        result = subprocess.run(f'adb -s {device_id} shell input swipe {xtap1} {ytap1} {xtap2} {ytap2} {duration}', text=True, stdout=subprocess.PIPE).stdout
        return True
    
    def click_image(self, device_id, template_path: str, threshold=0.8) -> bool:
        # Click vào vị trí của một đối tượng dựa trên hình ảnh mẫu.
        # threshold: Ngưỡng để xác định sự khớp giữa mẫu và ảnh (mặc định là 0.8).

        # Chụp màn hình của thiết bị
        screenshot_path = f"{device_id}-screen.png"
        subprocess.run(f'adb -s {device_id} exec-out screencap -p > {screenshot_path}', shell=True)
        
        # Đọc ảnh chụp màn hình và ảnh mẫu
        screen = cv2.imread(screenshot_path)
        template = cv2.imread(template_path)
        
        if screen is None or template is None:
            print("Không đọc được ảnh chụp màn hình hoặc ảnh mẫu.")
            return False
        
        # Tìm đối tượng trong ảnh màn hình
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        
        # Lấy vị trí khớp
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        # Nếu giá trị khớp lớn hơn hoặc bằng ngưỡng so sánh, click vào đối tượng
        if max_val >= threshold:
            top_left = max_loc
            template_height, template_width = template.shape[:2]
            center_x = top_left[0] + template_width // 2
            center_y = top_left[1] + template_height // 2
            
            # Click vào vị trí (center_x, center_y) trên thiết bị
            subprocess.run(f'adb -s {device_id} shell input tap {center_x} {center_y}', shell=True)
            return True
        else:
            print("Không tìm thấy đối tượng.")
            return False

    def click_id(self, device_id: str, resource_id: str) -> bool:
        # Click vào đối tượng theo resource-id.
        # resource_id: Giá trị resource-id cần tìm.

        try:
            # Lấy XML hiện tại từ UI Automator
            subprocess.run(f'adb -s {device_id} shell uiautomator dump', text=True, stdout=subprocess.PIPE)
            
            # Lấy nội dung XML
            xml_content = subprocess.run(f'adb -s {device_id} shell cat /sdcard/window_dump.xml', text=True, stdout=subprocess.PIPE, encoding='utf-8')

            # Phân tích root XML để tìm resource-id và lấy tọa độ trung tâm
            root = ET.fromstring(xml_content.stdout)

            for elem in root.iter():
                if elem.attrib.get('resource-id') == resource_id:
                    bounds = elem.attrib.get('bounds')

                    # Tính tọa độ trung tâm của đối tượng
                    bounds = re.findall(r'\d+', bounds)
                    if len(bounds) == 4:
                        x1, y1, x2, y2 = map(int, bounds)
                        center_x = (x1 + x2) // 2
                        center_y = (y1 + y2) // 2
                        
                        # Click vào tọa độ
                        subprocess.run(f'adb -s {device_id} shell input tap {center_x} {center_y}', shell=True)
                        return True

            # Nếu không tìm thấy đối tượng
            print("Không tìm thấy đối tượng")
            return False

        except Exception as e:
            print(f"Lỗi: {e}")
            return False




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
    
