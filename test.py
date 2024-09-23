import subprocess

a = subprocess.run(r'adb push "C:\Users\Rudyy\Documents\instagram\Reg Phone\ADB-Helper\images" /sdcard/Pictures/',text=True, stdout=subprocess.PIPE,)
print(a.stdout)
