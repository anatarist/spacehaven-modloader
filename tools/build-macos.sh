#!/bin/bash

VERSION=`python3 -c "import version; print(version.version)"`

python3 setup.py build
python3 setup.py bdist_mac --custom-info-plist tools/Info.plist

pushd build
rm spacehaven-modloader-$VERSION.macos.zip
zip -r spacehaven-modloader-$VERSION.macos.zip spacehaven-modloader-$VERSION.app
popd

pushd mods
zip -r mods-$VERSION.zip *
popd

mv mods/mods-$VERSION.zip build/

open build/
