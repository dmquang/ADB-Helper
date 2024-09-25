# ADBHelper (1.2.0) Usage Guide

## Introduction
`ADBHelper` is a Python class that helps manage Android devices through ADB (Android Debug Bridge). It provides methods for retrieving device information, installing applications, entering text, tapping on the screen, and many other functions.

## Installation

Before using, make sure you have installed:

- Python 3.x
- The libraries `adbutils==2.8.0` and `opencv-python==4.10.0.84`
- ADB configured correctly on your system

## How to Use

### Initialization

```python
from adb_helper import ADBHelper

# Khởi tạo thiết bị với device_id tương ứng
# Initialize device with corresponding device_id

device_id = 'emulator-5556'  # Device ID
adb_helper = ADBHelper(device_id)
```

1. Get Device List
```python
# Lấy thông tin toàn bộ các thiết bị
# Get information of all devices

devices = adb_helper.get_devices()
"""
devices = [
            {
                'platformVersion': platformVersion,
                'deviceName': deviceName,
                'appPackage': appPackage,
                'appActivity': appActivity, 
                'udid': i.serial    
            },
            ...
        ]
"""
```

2. Install APK File on Device
```python
# Cài đặt file APK
# Install Apk file

adb_helper.install_APK(apk_path)
```

3. Check If the Application Exists
```python
# Kiểm tra nếu ứng dụng đã được cài đặt trên thiết bị
# Check if Application is installed on device

exists = adb_helper.check_exits(app_package)
```

4. Open the Application
```python
# Mở ứng dụng trên thiết bị
# Open Application on device

adb_helper.open_app(app_package, 'com.example.app.MainActivity')
```

5. Transfer Media to Device
```python
# Chuyển toàn bộ 1 thư mục media sang thiết bị
# Transfer a media folder to device
# media_path = 'path/to/media/'

result = adb_helper.transfer_media(media_path)
print(result)
```

6. Input Text
```python
# Nhập chữ vào thiết bị
# Input text to device
# text_value: string

adb_helper.input_text("Hello World!")
```

7. Click at Coordinates
```python
# Click vào một vị trí trên màn hình thiết bị theo toạ độ
# Click on a position on the device screen based on coordinates
# coordinates: (x, y)

adb_helper.click_screen(coordinates)
```

8. Swipe the Screen
```python
# Thực hiện thao tác vuốt màn hình từ một vị trí đến một vị trí khác trên thiết bị Android. Thời gian thực hiện vuốt được điều chỉnh bằng tham số duration.
# Swipe the screen from one position to another on the Android device. The time to perform the swipe is adjusted by the duration parameter.
# start_coordinates: (x1, y1)
# end_coordinates: (x2, y2)

adb_helper.swipe_screen(start_coords, end_coords, 500)
```

9. Click by Image
```python
# Click vào vị trí của một đối tượng dựa trên hình ảnh mẫu.
# template_path: Đường dẫn đến hình ảnh mẫu cần tìm kiếm trên màn hình thiết bị.
# threshold: Ngưỡng để xác định sự khớp giữa mẫu và ảnh (mặc định là 0.8).
# ---
# Click on the position of an object based on a template image.
# template_path: Path to the template image to search for on the device screen.
# threshold: Threshold to determine the match between the template and the image (default is 0.8).

adb_helper.click_image(template_path)
```

10. Click by Attriute
```python
# Không dùng cho class
# Đối với class, dùng click_class() thay thế

# Not used for class
# For class, use click_class() instead

# Click vào đối tượng theo thuộc tính và giá trị của thuộc tính đó.
# attribute: Tên thuộc tính (ví dụ: text, content-desc, resource-id).
# value: Giá trị của thuộc tính đó.
# ---
# Click on the object by attribute and the value of that attribute.
# attribute: Attribute name (e.g. text, content-desc, resource-id).
# value: Value of that attribute.

adb_helper.click_attribute(attribute, value)
```

11. Click by class & index
```python
# Click vào đối tượng theo class và index.
# class: Giá trị class cần tìm.
# index: Giá trị index cần tìm.
# ---
# Click on the object by class and index.
# class: The class value to find.
# index: The index value to find.

adb_helper.click_class(class_name, index)
```

12. Check XML's Attribute
```python
# Kiểm tra xem có đối tượng nào trong XML có thuộc tính và giá trị cho trước hay không.
# attribute: Tên thuộc tính cần kiểm tra.
# value: Giá trị của thuộc tính cần kiểm tra.
# ---
# Check if there is any object in the XML with the given attribute and value.
# attribute: The name of the attribute to check.
# value: The value of the attribute to check.

# attribute = class, text, content-desc, resource-id, ... (str)

adb_helper.check_XML(attribute, value)
```

13. Pull APK File from Device
```python
# Xuất APK từ thiết bị Android thông qua ADB.
# appPackage: Tên gói của ứng dụng cần xuất APK.
# ---
# Export APK from Android device via ADB.
# appPackage: The package name of the application to export APK.

adb_helper.export_APK(appPackage, output_path)
```

14. Send Key Event to Device
```python
# Gửi event phím tắt tới thiết bị thông qua ADB.
# Để xem danh sách các phím tắt có sẵn, hãy sử dụng lệnh "adb shell input keyevent".
# ---
# Send key event to the device via ADB.
# To see the list of available shortcuts, use the "adb shell input keyevent" command.

adb_helper.key_envent(event_code)
```


---

**Author**: Rudyy Greyrat  
**GitHub**: [dmquang](https://github.com/dmquang)  
**Telegram**: [@rudyy_greyrat](https://t.me/rudyy_greyrat)

---

Feel free to let me know if you need any further modifications or additions!
