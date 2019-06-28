#!/bin/bash

VERSION=`python3 -c "import version; print(version.version)"`

rm -rf build/*

python3 setup.py build
python3 setup.py bdist_mac --custom-info-plist tools/Info.plist

pushd build
rm spacehaven-modloader-$VERSION.macos.zip
zip -r spacehaven-modloader-$VERSION.macos.zip spacehaven-modloader-$VERSION.app
popd

mkdir -p dist/
mv build/*.zip dist/

echo 'Packaging complete!'
echo "Upload dist/* to GitHub"

open dist/
