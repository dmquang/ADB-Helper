from setuptools import setup, find_packages

setup(
    name="ADB-Helper",
    version="1.2.0",
    description="ADBHelper is a Python class that helps manage Android devices through ADB (Android Debug Bridge). It provides methods for retrieving device information, installing applications, entering text, tapping on the screen, and many other functions.",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    author="Rudyy Greyrat",
    author_email="quang722008@gmail.com",
    url="https://github.com/dmquang/ADB-Helper",
    packages=find_packages(), 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=[
        "opencv-python",
        "adbutils"
    ],
)
