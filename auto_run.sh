#!/bin/bash

APK_NAME="bookapp-0.1-arm64-v8a_armeabi-v7a-debug.apk"
APK_PATH="./bin/$APK_NAME"
WIN_DEST="/mnt/c/Users/bonda/Downloads/$APK_NAME"
PACKAGE="org.yevhenii.bookapp"
AVD_NAME="redmi_14"
WINDOWS_EMULATOR="/mnt/c/Users/bonda/AppData/Local/Android/Sdk/emulator/emulator.exe"

echo "=== BUILD APK ==="
buildozer android debug || exit 1

echo "=== COPY APK TO WINDOWS ==="
cp "$APK_PATH" "$WIN_DEST"

echo "=== START EMULATOR IF NEEDED ==="
EMU=$(adb devices | grep emulator)

if [ -z "$EMU" ]; then
    echo "Starting emulator..."
    "$WINDOWS_EMULATOR" -avd $AVD_NAME > /dev/null 2>&1 &
    adb wait-for-device
fi

echo "=== INSTALL APK ==="
adb install -r "$APK_PATH"

echo "=== LAUNCH APP ==="
adb shell monkey -p $PACKAGE -c android.intent.category.LAUNCHER 1

echo "✅ DONE"
