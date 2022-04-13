#!/bin/sh
# Create folders.
[ -e package ] && rm -r package
mkdir -p package/opt
mkdir -p package/usr/share/applications
mkdir -p package/usr/share/icons/hicolor/128x128/apps

# Compress distribution

export LISS_VERSION=$(cat version.txt)
rm Lissajous_${LISS_VERSION}.zip
zip -r Lissajous_${LISS_VERSION}.zip dist/Lissajous

# Copy files 
cp -r dist/Lissajous package/opt/Lissajous
cp icons/icon_128.bmp package/usr/share/icons/hicolor/128x128/apps/Lissajous.bmp
cp Lissajous.desktop package/usr/share/applications

# Change permissions
find package/opt/Lissajous -type f -exec chmod 755 -- {} +
find package/usr/share -type f -exec chmod 644 -- {} +

# Get version

# Create .deb
fpm -C package -s dir -t deb -n "test-lissajous" -v ${LISS_VERSION} -p test-lissajous.deb
