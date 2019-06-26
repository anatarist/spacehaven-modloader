#!/bin/bash

VERSION=`python -c 'import version; print(version.version)'`

rm -rf dist/spacehaven-modloader dist/spacehaven-modloader-$VERSION.windows
pyinstaller spacehaven-modloader.py --noconsole

mv dist/spacehaven-modloader dist/spacehaven-modloader-$VERSION.windows

start dist
