[app]

# (str) Title of your application
title = BookApp

# (str) Package name
package.name = bookapp

# (str) Package domain (обов’язково змінити, якщо публікувати)
package.domain = org.example

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (extensions)
source.include_exts = py,png,jpg,kv,atlas

# (list) Packages to include in the APK
requirements = python3,kivy,kivymd,requests

# (str) Icon of the app
icon.filename = %(source.dir)s/icon.png

# (str) Supported orientation: 'portrait', 'landscape', 'sensor'
orientation = portrait

# (bool) Fullscreen or not
fullscreen = 0

# (str) Presplash image
presplash.filename = %(source.dir)s/presplash.png

# (str) Android API to target
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (int) Android SDK build tools version
android.sdk = 33

# (str) Android NDK version
android.ndk = 25b

# (int) Android NDK API to use
android.ndk_api = 21

# (str) Android entry point, default is ok
android.entrypoint = org.kivy.android.PythonActivity

# (str) Android app theme, leave default
android.theme = '@android:style/Theme.NoTitleBar'

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# (bool) Copy library dependencies into APK
android.copy_libs = 1

# (bool) Embed the private data folder in the APK
android.private_storage = 1

# (bool) Logcat filters
log_level = 2

# (bool) Use SDL2 (recommended)
android.use_sdl2 = True
