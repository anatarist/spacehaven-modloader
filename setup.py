
import sys
from cx_Freeze import setup, Executable

import version

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["six", "pkg_resources._vendor", "sysconfig"], "excludes": []}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

APP = ['spacehaven-modloader.py']
DATA_FILES = []
OPTIONS = {}

setup(
    name="spacehaven-modloader",
    version=version.version,
    app=APP,
    data_files=DATA_FILES,
    options={"build_exe": build_exe_options},
    executables=[Executable("spacehaven-modloader.py", base=base)],
    setup_requires=[],
    install_requires=[
        'lxml',
        'click',
        'pypng',
        'six',
        'appdirs'
    ]
)
