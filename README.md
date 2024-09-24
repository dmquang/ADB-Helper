# ADBHelper Usage Guide

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

adb_helper = ADBHelper()
```

1. Get Device List
```python
from adb_helper import ADBHelper

device_id = 'emulator-5556'  # Device ID
adb_helper = ADBHelper(device_id)
```

2. Install APK File on Device
```python
apk_path = 'path/to/your.apk'
adb_helper.install_APK(apk_path)
```

3. Check If the Application Exists
```python
app_package = 'com.example.app'
exists = adb_helper.check_exits(app_package)
print("Ứng dụng đã cài đặt:", exists)
```

4. Open the Application
```python
adb_helper.open_app(app_package, 'com.example.app.MainActivity')
```

5. Transfer Media to Device
```python
media_path = 'path/to/media/'
result = adb_helper.transfer_media(media_path)
print(result)
```

6. Input Text
```python
adb_helper.input_text("Hello World!")
```

7. Click at Coordinates
```python
coordinates = (100, 200)
adb_helper.click_screen(coordinates)
```

8. Swipe the Screen
```python
# (x, y)
start_coords = (100, 200)
end_coords = (200, 300)
adb_helper.swipe_screen(start_coords, end_coords, 500)
```

9. Click by Image
```python
template_path = 'path/to/template.png' # Image of the object to click
adb_helper.click_image(template_path)
```

10. Click by resource-id
```python
resource_id = 'com.example.app:id/button'
adb_helper.click_id(resource_id)
```

11. Click by content-desc
```python
content_desc = 'Content Desc'
adb_helper.click_desc(content_desc)
```

12. Click by class & index
```python
class_name = 'Class Name'
index = "0" # Index of the element in the class
adb_helper.click_class(class_name, index)
```

13. Click by text
```python
text = 'Text'
adb_helper.click_text(text)
```

14. Pull APK File from Device
```python
appPackage = 'com.example.app' # Application package name
output_path = 'path/to/output/' # Output directory
adb_helper.export_APK(appPackage, output_path)
```

#### Others Funtions
1. Get Device List
```python
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

---

**Author**: Rudyy Greyrat  
**GitHub**: [dmquang](https://github.com/dmquang)  
**Telegram**: [@rudyy_greyrat](https://t.me/rudyy_greyrat)

---

Feel free to let me know if you need any further modifications or additions!
