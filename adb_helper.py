"""
Author: Rudyy Greyrat
GitHub: dmquang
Telegram: @rudyy_greyrat
"""

from adbutils import adb
import os, subprocess, cv2, re, time
import xml.etree.ElementTree as ET

class ADBHelper:
    def __init__(self, device_id) -> None:
        # Khởi tạo thiết bị với device_id tương ứng
        # Initialize device with corresponding device_id
        self.device_id = device_id
    
    def get_devices(self) -> list:
        # Lấy thông tin toàn bộ các thiết bị
        # Get information of all devices
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
    
    def install_APK(self, apk_path):
        # Cài đặt file APK
        # Install Apk file
        subprocess.run(f'adb -s {self.device_id} install "{apk_path}"', text=True, stdout=subprocess.PIPE).stdout
        return
    
    def check_exits(self, appPackage):
        # Kiểm tra nếu ứng dụng đã được cài đặt trên thiết bị
        # Check if Application is installed on device
        result = subprocess.run(f'adb -s {self.device_id} shell pm list packages', text=True, stdout=subprocess.PIPE).stdout
        if not appPackage in result:
            return False
        return True

    def open_app(self, appPackage, appActivity) -> str:
        # Mở ứng dụng trên thiết bị
        # Open Application on device
        result = subprocess.run(f'adb -s {self.device_id} shell am start -n {appPackage}/{appActivity}', text=True, stdout=subprocess.PIPE).stdout
        return result

    def transfer_media(self, media_path) -> str:
        # Chuyển toàn bộ 1 thư mục media sang thiết bị
        # Transfer a media folder to device
        transfer = subprocess.run(f'adb -s {self.device_id} push "{media_path}" /sdcard/Pictures/', text=True, stdout=subprocess.PIPE).stdout.strip().split(': ')[1]
        return transfer # 90 files pushed, 0 skipped. 9.6 MB/s (5063214 bytes in 0.504s)

    def input_text(self, text_value: str):
        for char in text_value:
            subprocess.run(f'adb -s {self.device_id} shell input text "{char}"', shell=True)
            time.sleep(0.01)
        return True

    def click_screen(self, coordinates: tuple) -> bool:
        # Click vào một vị trí trên màn hình thiết bị theo toạ độ
        # Click on a position on the device screen based on coordinates
        # coordinates: (x, y)
        xtap, ytap = coordinates
        result = subprocess.run(f'adb -s {self.device_id} shell input tap {xtap} {ytap}', text=True, stdout=subprocess.PIPE).stdout
        return True

    def swipe_screen(self, start_coordinates:tuple, end_coordinates:tuple, duration:int) -> bool:
        # Thực hiện thao tác vuốt màn hình từ một vị trí đến một vị trí khác trên thiết bị Android. Thời gian thực hiện vuốt được điều chỉnh bằng tham số duration.
        # Swipe the screen from one position to another on the Android device. The time to perform the swipe is adjusted by the duration parameter.
        xtap1, ytap1 = start_coordinates
        xtap2, ytap2 = end_coordinates
        result = subprocess.run(f'adb -s {self.device_id} shell input swipe {xtap1} {ytap1} {xtap2} {ytap2} {duration}', text=True, stdout=subprocess.PIPE).stdout
        return True
    
    def click_image(self, template_path: str, threshold=0.8) -> bool:
        # Click vào vị trí của một đối tượng dựa trên hình ảnh mẫu.
        # threshold: Ngưỡng để xác định sự khớp giữa mẫu và ảnh (mặc định là 0.8).
        # ---
        # Click on the position of an object based on a template image.
        # threshold: Threshold to determine the match between the template and the image (default is 0.8).

        # Chụp màn hình của thiết bị
        # Capture the device screen
        screenshot_path = f"{self.device_id}-screen.png"
        subprocess.run(f'adb -s {self.device_id} exec-out screencap -p > {screenshot_path}', shell=True)
        
        # Đọc ảnh chụp màn hình và ảnh mẫu
        # Read the screenshot and template images
        screen = cv2.imread(screenshot_path)
        template = cv2.imread(template_path)
        
        if screen is None or template is None:
            print("Không đọc được ảnh chụp màn hình hoặc ảnh mẫu.")
            return False
        
        # Tìm đối tượng trong ảnh màn hình
        # Find object in the screen image
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        
        # Lấy vị trí khớp
        # Get the match position
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        # Nếu giá trị khớp lớn hơn hoặc bằng ngưỡng so sánh, click vào đối tượng
        # If the match value is greater than or equal to the threshold, click on the object
        if max_val >= threshold:
            top_left = max_loc
            template_height, template_width = template.shape[:2]
            center_x = top_left[0] + template_width // 2
            center_y = top_left[1] + template_height // 2
            
            # Click vào vị trí (center_x, center_y) trên thiết bị
            # Click on the position (center_x, center_y) on the device
            subprocess.run(f'adb -s {self.device_id} shell input tap {center_x} {center_y}', shell=True)
            return True
        else:
            print("Can't find the object.")
            return False

    def click_id(self, resource_id: str) -> bool:
        # Click vào đối tượng theo resource-id.
        # resource_id: Giá trị resource-id cần tìm.
        # ---
        # Click on the object by resource-id.
        # resource_id: The resource-id value to find.

        try:
            # Lấy XML hiện tại từ UI Automator
            # Get the current XML from UI Automator
            subprocess.run(f'adb -s {self.device_id} shell uiautomator dump', text=True, stdout=subprocess.PIPE)
            
            # Lấy nội dung XML
            # Get the XML content
            xml_content = subprocess.run(f'adb -s {self.device_id} shell cat /sdcard/window_dump.xml', text=True, stdout=subprocess.PIPE, encoding='utf-8')

            # Phân tích root XML để tìm resource-id và lấy tọa độ trung tâm
            # Parse the root XML to find the resource-id and get the center coordinates
            root = ET.fromstring(xml_content.stdout)

            for elem in root.iter():
                if elem.attrib.get('resource-id') == resource_id:
                    bounds = elem.attrib.get('bounds')

                    # Tính tọa độ trung tâm của đối tượng
                    # Calculate the center coordinates of the object
                    bounds = re.findall(r'\d+', bounds)
                    if len(bounds) == 4:
                        x1, y1, x2, y2 = map(int, bounds)
                        center_x = (x1 + x2) // 2
                        center_y = (y1 + y2) // 2
                        
                        # Click vào tọa độ
                        # Click on the coordinates
                        subprocess.run(f'adb -s {self.device_id} shell input tap {center_x} {center_y}', shell=True)
                        return True

            # Nếu Can't find the object
            # If the object is not found
            print("Can't find the object")
            return False

        except Exception as e:
            print(f"Lỗi: {e}")
            return False
        
    def click_desc(self, content_desc: str) -> bool:
        # Click vào đối tượng theo content-desc.
        # content_desc: Giá trị content-desc cần tìm.
        # ---
        # Click on the object by content-desc.
        # content_desc: The content-desc value to find.

        try:
            # Lấy XML hiện tại từ UI Automator
            # Get the current XML from UI Automator
            subprocess.run(f'adb -s {self.device_id} shell uiautomator dump', text=True, stdout=subprocess.PIPE)
            
            # Lấy nội dung XML
            # Get the XML content
            xml_content = subprocess.run(f'adb -s {self.device_id} shell cat /sdcard/window_dump.xml', text=True, stdout=subprocess.PIPE, encoding='utf-8')

            # Phân tích root XML để tìm content-desc và lấy tọa độ trung tâm
            # Parse the root XML to find the content-desc and get the center coordinates
            root = ET.fromstring(xml_content.stdout)

            for elem in root.iter():
                if elem.attrib.get('content-desc') == content_desc:
                    bounds = elem.attrib.get('bounds')

                    # Tính tọa độ trung tâm của đối tượng
                    # Calculate the center coordinates of the object
                    bounds = re.findall(r'\d+', bounds)
                    if len(bounds) == 4:
                        x1, y1, x2, y2 = map(int, bounds)
                        center_x = (x1 + x2) // 2
                        center_y = (y1 + y2) // 2
                        
                        # Click vào tọa độ
                        subprocess.run(f'adb -s {self.device_id} shell input tap {center_x} {center_y}', shell=True)
                        return True

            # Nếu Can't find the object
            # If the object is not found
            print("Can't find the object")
            return False
        
        except Exception as e:
            print(f"Lỗi: {e}")
            return False
        
    def click_class(self, class_name: str, index: str) -> bool:
        # Click vào đối tượng theo class và index.
        # class: Giá trị class cần tìm.
        # index: Giá trị index cần tìm.
        # ---
        # Click on the object by class and index.
        # class: The class value to find.
        # index: The index value to find.

        try:
            # Lấy XML hiện tại từ UI Automator
            # Get the current XML from UI Automator
            subprocess.run(f'adb -s {self.device_id} shell uiautomator dump', text=True, stdout=subprocess.PIPE)
            
            # Lấy nội dung XML
            # Get the XML content
            xml_content = subprocess.run(f'adb -s {self.device_id} shell cat /sdcard/window_dump.xml', text=True, stdout=subprocess.PIPE, encoding='utf-8')

            # Phân tích root XML để tìm content-desc và lấy tọa độ trung tâm
            # Parse the root XML to find the class and index and get the center coordinates
            root = ET.fromstring(xml_content.stdout)

            for elem in root.iter():
                if elem.attrib.get('class') == class_name and elem.attrib.get('index') == index:
                    bounds = elem.attrib.get('bounds')

                    # Tính tọa độ trung tâm của đối tượng
                    # Calculate the center coordinates of the object
                    bounds = re.findall(r'\d+', bounds)
                    if len(bounds) == 4:
                        x1, y1, x2, y2 = map(int, bounds)
                        center_x = (x1 + x2) // 2
                        center_y = (y1 + y2) // 2
                        
                        # Click vào tọa độ
                        # Click on the coordinates
                        subprocess.run(f'adb -s {self.device_id} shell input tap {center_x} {center_y}', shell=True)
                        return True

            # Nếu Can't find the object
            # If the object is not found
            print("Can't find the object")
            return False
        
        except Exception as e:
            print(f"Lỗi: {e}")
            return False

    def click_text(self, text: str) -> bool:
        """
        *** LƯU Ý ***
        Chỉ click được khi XML của đối tượng tồn tại thuộc tính text (text="")
        ---
        **** NOTE ****
        Only clickable when the object's XML has the text attribute (text="")
        """
        # Click vào đối tượng theo text.
        # text: Giá trị text cần tìm.
        # ---
        # Click on the object by text.
        # text: The text value to find.

        try:
            # Lấy XML hiện tại từ UI Automator
            # Get the current XML from UI Automator
            subprocess.run(f'adb -s {self.device_id} shell uiautomator dump', text=True, stdout=subprocess.PIPE)
            
            # Lấy nội dung XML
            # Get the XML content
            xml_content = subprocess.run(f'adb -s {self.device_id} shell cat /sdcard/window_dump.xml', text=True, stdout=subprocess.PIPE, encoding='utf-8')

            # Phân tích root XML để tìm text và lấy tọa độ trung tâm
            # Parse the root XML to find the text and get the center coordinates
            root = ET.fromstring(xml_content.stdout)

            for elem in root.iter():
                if elem.attrib.get('text') == text:
                    bounds = elem.attrib.get('bounds')

                    # Tính tọa độ trung tâm của đối tượng
                    # Calculate the center coordinates of the object
                    bounds = re.findall(r'\d+', bounds)
                    if len(bounds) == 4:
                        x1, y1, x2, y2 = map(int, bounds)
                        center_x = (x1 + x2) // 2
                        center_y = (y1 + y2) // 2
                        
                        # Click vào tọa độ
                        # Click on the coordinates
                        subprocess.run(f'adb -s {self.device_id} shell input tap {center_x} {center_y}', shell=True)
                        return True

            # Nếu Can't find the object
            # If the object is not found
            print("Can't find the object")
            return False

        except Exception as e:
            print(f"Lỗi: {e}")
            return False

    def export_APK(self, appPackage: str, output_path: str) -> bool:
        # Xuất APK từ thiết bị Android thông qua ADB.
        # appPackage: Tên gói của ứng dụng cần xuất APK.
        # ---
        # Export APK from Android device via ADB.
        # appPackage: The package name of the application to export APK.

        try:
            # Lấy APK path từ thiết bị
            # Get APK path from device
            get_apk_command = f"adb -s {self.device_id} shell pm path {appPackage}"
            result = subprocess.run(get_apk_command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if result.returncode == 0 and 'package:' in result.stdout:
                apk_path = result.stdout.split('package:')[1].strip()

                # Lệnh để pull file APK từ thiết bị về máy tính
                # Command to pull the APK file from the device to the computer
                pull_apk_command = f"adb -s {self.device_id} pull {apk_path} {output_path}"
                pull_result = subprocess.run(pull_apk_command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                if pull_result.returncode == 0:
                    print(f"APK successfully pulled to {output_path}")
                else:
                    print(f"Failed to pull APK. Error: {pull_result.stderr}")
            else:
                print(f"Failed to get APK path for {appPackage}. Error: {result.stderr}")
        except Exception as e:
            print(f"Error: {e}")

