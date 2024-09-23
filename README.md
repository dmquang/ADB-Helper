# Hướng Dẫn Sử Dụng ADBHelper

## Giới Thiệu
`ADBHelper` là một lớp Python giúp quản lý các thiết bị Android thông qua ADB (Android Debug Bridge). Nó cung cấp các phương thức để lấy thông tin thiết bị, cài đặt ứng dụng, nhập văn bản, nhấp chuột vào màn hình và nhiều chức năng khác.

## Cài Đặt

Trước khi sử dụng, hãy đảm bảo rằng bạn đã cài đặt:

- Python 3.x
- Thư viện `adb` và `opencv-python`
- ADB được cấu hình đúng trên hệ thống của bạn

## Cách Sử Dụng

### Khởi Tạo

```python
from adb_helper import ADBHelper

adb_helper = ADBHelper()
1. Lấy Danh Sách Thiết Bị
python
Sao chép mã
devices = adb_helper.get_devices()
print(devices)
2. Cài Đặt Ứng Dụng
python
Sao chép mã
device_id = 'emulator-5556'  # ID của thiết bị
apk_path = 'path/to/your.apk'
adb_helper.install_APK(device_id, apk_path)
3. Kiểm Tra Ứng Dụng
python
Sao chép mã
app_package = 'com.example.app'
exists = adb_helper.check_exits(device_id, app_package)
print("Ứng dụng đã cài đặt:", exists)
4. Mở Ứng Dụng
python
Sao chép mã
adb_helper.open_app(device_id, app_package, 'com.example.app.MainActivity')
5. Chuyển Media
python
Sao chép mã
media_path = 'path/to/media/'
result = adb_helper.transfer_media(device_id, media_path)
print(result)
6. Nhập Văn Bản
python
Sao chép mã
adb_helper.input_text(device_id, "Hello World!")
7. Nhấp Chuột Trên Màn Hình
python
Sao chép mã
coordinates = (100, 200)
adb_helper.click_screen(device_id, coordinates)
8. Vuốt Màn Hình
python
Sao chép mã
start_coords = (100, 200)
end_coords = (200, 300)
adb_helper.swipe_screen(device_id, start_coords, end_coords, 500)
9. Nhấp Vào Hình Ảnh
python
Sao chép mã
template_path = 'path/to/template.png'
adb_helper.click_image(device_id, template_path)
10. Nhấp Vào Đối Tượng Theo Resource ID
python
Sao chép mã
resource_id = 'com.example.app:id/button'
adb_helper.click_id(device_id, resource_id)
Bản Quyền
ADBHelper được phát hành theo giấy phép MIT. Bạn có thể tự do sử dụng, sao chép, sửa đổi, và phân phối mã nguồn. Tuy nhiên, hãy đảm bảo ghi nhận tác giả ban đầu khi sử dụng hoặc phân phối mã nguồn.
