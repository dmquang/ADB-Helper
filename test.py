from adb_helper import ADBHelper
import subprocess

helper = ADBHelper()
helper.click_id(device_id='emulator-5556', resource_id='com.instagram.android:id/profile_tab')
