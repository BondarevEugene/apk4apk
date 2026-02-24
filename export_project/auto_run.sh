#!/bin/bash

# === CONFIG ===
APP_NAME="bookapp"
APK_NAME="bookapp-0.1-arm64-v8a_armeabi-v7a-debug.apk"
APK_PATH="./bin/$APK_NAME"
WIN_DEST="/mnt/c/Users/bonda/Downloads/$APK_NAME"
PACKAGE="org.yevhenii.bookapp"
AVD_NAME="redmi_14"
WINDOWS_EMULATOR="/mnt/c/Users/bonda/AppData/Local/Android/Sdk/emulator/emulator.exe"

# === COLORS & ICONS ===
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[1;33m"
BLUE="\033[0;34m"
RESET="\033[0m"

ICON_STEP="🟢"
ICON_DONE="✅"
ICON_WARN="⚠️"
ICON_ERROR="❌"
ICON_BUILD="🔨"
ICON_COPY="📂"
ICON_PHONE="📱"
ICON_RUN="🚀"

# === FUNCTIONS ===
print_step() {
    echo -e "${YELLOW}${ICON_STEP} $1${RESET}"
}

print_done() {
    echo -e "${GREEN}${ICON_DONE} $1${RESET}"
}

print_error() {
    echo -e "${RED}${ICON_ERROR} $1${RESET}"
}

spinner_wait() {
    # $1 - command to check condition
    # $2 - max seconds
    timeout=${2:-60}
    elapsed=0
    spinner="/-\|"
    spin_index=0

    while ! eval "$1" && [ $elapsed -lt $timeout ]; do
        spin_char=${spinner:spin_index:1}
        spin_index=$(( (spin_index + 1) % 4 ))
        printf "\r%s" "$spin_char"
        sleep 1
        elapsed=$((elapsed+1))
    done
    printf "\r"
    return $elapsed
}

# === STEP 1: Local Python check ===
print_step "Checking Python environment 🐍"
if [ ! -f main.py ]; then
    print_error "main.py not found!"
    exit 1
fi

# Try to run main.py quickly
python3 main.py & PID=$!
sleep 2
kill $PID 2>/dev/null
print_done "Local Python check completed"

# === STEP 2: Build APK ====
print_step "Building APK $APP_NAME $ICON_BUILD"
buildozer android debug || { print_error "Buildozer failed!"; exit 1; }
if [ ! -f "$APK_PATH" ]; then
    print_error "APK not found at $APK_PATH"
    exit 1
fi
print_done "APK built successfully"

# === STEP 3: Copy APK to Windows ===
print_step "Copying APK to Windows Downloads $ICON_COPY"
cp "$APK_PATH" "$WIN_DEST" || { print_error "Failed to copy APK!"; exit 1; }
print_done "APK copied to $WIN_DEST"

# === STEP 4: Check/start emulator ===
print_step "Checking emulator $ICON_PHONE"
EMU=$(adb devices | grep emulator || true)

if [ -z "$EMU" ]; then
    print_step "Starting emulator $AVD_NAME $ICON_RUN"
    "$WINDOWS_EMULATOR" -avd $AVD_NAME > /dev/null 2>&1 &

    print_step "Waiting for emulator to boot ⏱️"

    spinner_wait "adb shell getprop sys.boot_completed 2>/dev/null | grep 1" 300
    if [ $? -ge 300 ]; then
        print_error "Emulator failed to boot in time!"
        exit 1
    fi

    print_done "Emulator ready"
else
    print_done "Emulator already running"
fi

# === STEP 5: Install APK ===
print_step "Installing APK on emulator 📥"
adb install -r "$APK_PATH" || { print_error "APK installation failed!"; exit 1; }
print_done "APK installed successfully"

# === STEP 6: Launch app ===
print_step "Launching app $APP_NAME $ICON_RUN"
adb shell monkey -p $PACKAGE -c android.intent.category.LAUNCHER 1 || { print_error "App launch failed!"; exit 1; }
print_done "App launched"

echo -e "${GREEN}All steps completed successfully! ${ICON_DONE}${RESET}"
