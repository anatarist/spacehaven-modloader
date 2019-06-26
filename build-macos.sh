#!/bin/bash

python3 setup.py build
python3 setup.py bdist_mac --custom-info-plist Info.plist
