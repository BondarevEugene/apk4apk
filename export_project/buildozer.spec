[app]

# ------------------------------
# BASIC APP CONFIG
# ------------------------------

title = BookApp
package.name = bookapp
package.domain = org.yevhenii

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,ttf

version = 0.1

orientation = portrait
fullscreen = 0

icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.png


# ------------------------------
# PYTHON / REQUIREMENTS
# ------------------------------

requirements = python3,kivy,kivymd,requests,plyer

# Optional but safer for KivyMD
android.gradle_dependencies = com.android.support:support-v4:28.0.0


# ------------------------------
# ANDROID CONFIG
# ------------------------------

android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.ndk_api = 21

android.entrypoint = org.kivy.android.PythonActivity
android.theme = "@android:style/Theme.NoTitleBar"

android.permissions = INTERNET,ACCESS_NETWORK_STATE

android.use_sdl2 = True
android.copy_libs = 1
android.private_storage = 1


# ------------------------------
# PERFORMANCE & STABILITY
# ------------------------------

log_level = 2

android.logcat_filters = *:S python:D

# Avoid unnecessary rebuild issues
android.allow_backup = False

# Enable AndroidX (modern Android support)
android.enable_androidx = True

# ------------------------------
# BUILD OPTIMIZATION
# ------------------------------

p4a.branch = stable

# Reduce rebuild problems
android.arch = arm64-v8a, armeabi-v7a

# ------------------------------
# RELEASE SIGNING
# ------------------------------

android.release_keystore = bookapp-release.keystore
android.release_keyalias = bookapp

android.release_keystore_password = 170788
android.release_keyalias_password = 170788
