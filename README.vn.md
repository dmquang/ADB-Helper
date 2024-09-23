# Hướng Dẫn Sử Dụng ADBHelper

## Giới Thiệu
`ADBHelper` là một lớp Python giúp quản lý các thiết bị Android thông qua ADB (Android Debug Bridge). Nó cung cấp các phương thức để lấy thông tin thiết bị, cài đặt ứng dụng, nhập văn bản, nhấp chuột vào màn hình và nhiều chức năng khác.

## Cài Đặt

Trước khi sử dụng, hãy đảm bảo rằng bạn đã cài đặt:

- Python 3.x
- Thư viện `adbutils==2.8.0` và `opencv-python==4.10.0.84`
- ADB được cấu hình đúng trên hệ thống của bạn

## Cách Sử Dụng

### Khởi Tạo

```python
from adb_helper import ADBHelper

adb_helper = ADBHelper()
```

1. Lấy Danh Sách Thiết Bị
```python
from adb_helper import ADBHelper

adb_helper = ADBHelper()
```

2. Cài Đặt File APK Lên Thiết Bị
```python
device_id = 'emulator-5556'  # ID của thiết bị
apk_path = 'path/to/your.apk'
adb_helper.install_APK(device_id, apk_path)
```

3. Kiểm Tra Ứng Dụng Có Tồn Tại Chưa
```python
app_package = 'com.example.app'
exists = adb_helper.check_exits(device_id, app_package)
print("Ứng dụng đã cài đặt:", exists)
```

4. Mở Ứng Dụng
```python
adb_helper.open_app(device_id, app_package, 'com.example.app.MainActivity')
```

5. Chuyển Media Vào Thiết Bị
```python
media_path = 'path/to/media/'
result = adb_helper.transfer_media(device_id, media_path)
print(result)
```

6. Nhập Văn Bản
```python
adb_helper.input_text(device_id, "Hello World!")
```

7. Click Theo Tọa Độ
```python
coordinates = (100, 200)
adb_helper.click_screen(device_id, coordinates)
```

8. Vuốt Màn Hình
```python
# (x, y)
start_coords = (100, 200)
end_coords = (200, 300)
adb_helper.swipe_screen(device_id, start_coords, end_coords, 500)
```

9. Click Theo Ảnh
```python
template_path = 'path/to/template.png' # Ảnh đối tượng cần click
adb_helper.click_image(device_id, template_path)
```

10. Click Theo resource-id
```python
resource_id = 'com.example.app:id/button'
adb_helper.click_id(device_id, resource_id)
```

---

**Author**: Rudyy Greyrat  
**GitHub**: [dmquang](https://github.com/dmquang)  
**Telegram**: [@rudyy_greyrat](https://t.me/rudyy_greyrat)

