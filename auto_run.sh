#!/bin/bash

APP_NAME="bookapp"
APK_NAME="bookapp-0.1-arm64-v8a_armeabi-v7a-debug.apk"
APK_PATH="./bin/$APK_NAME"
WIN_DEST="/mnt/c/Users/bonda/Downloads/$APK_NAME"
PACKAGE="org.yevhenii.bookapp"
AVD_NAME="redmi_14"

WINDOWS_EMULATOR="/mnt/c/Users/bonda/AppData/Local/Android/Sdk/emulator/emulator.exe"

echo "=== STEP 1: Local Python check ==="
if [ ! -f main.py ]; then
    echo "main.py not found!"
    exit 1
fi

python3 main.py &
PID=$!
sleep 3
kill $PID 2>/dev/null
echo "Local check done."

echo "=== STEP 2: Build APK ==="
buildozer android debug || exit 1

if [ ! -f "$APK_PATH" ]; then
    echo "APK not found!"
    exit 1
fi

echo "=== STEP 3: Copy APK to Windows ==="
cp "$APK_PATH" "$WIN_DEST"

echo "=== STEP 4: Check emulator ==="
EMU=$(adb devices | grep emulator)

if [ -z "$EMU" ]; then
    echo "Starting emulator..."
    "$WINDOWS_EMULATOR" -avd $AVD_NAME > /dev/null 2>&1 &

    echo "Waiting for emulator to boot..."
    adb wait-for-device

    boot_completed=""
    while [[ "$boot_completed" != "1" ]]; do
        sleep 2
        boot_completed=$(adb shell getprop sys.boot_completed 2>/dev/null | tr -d '\r')
        echo "Booting..."
    done

    echo "Emulator ready."
else
    echo "Emulator already running."
fi

echo "=== STEP 5: Install APK ==="
adb install -r "$APK_PATH"

echo "=== STEP 6: Launch app ==="
adb shell monkey -p $PACKAGE -c android.intent.category.LAUNCHER 1

echo "✅ DONE!"
