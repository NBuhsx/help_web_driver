from setuptools import setup

setup(
    name='help_web_driver',
    version='1.0.0',
    description='pages and params execute webdriver',
    author='NBuhsx',
    author_email='sergey33sergey@yandex.com',
    url="https://notabug.org/NBuhsx/help_web_driver",
    packages=["help_webdriver"],
    install_requires=[
        "Pillow==9.1.0",
        "selenium"
    ],
)
