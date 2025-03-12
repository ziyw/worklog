
from setuptools import setup

APP = ['WorkLog.py']
DATA_FILES = []
OPTIONS = {
    'packages': ['rumps'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
