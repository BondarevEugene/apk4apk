[app]
# Назва та пакет
title = DemoBook
package.name = demobook
package.domain = org.example
version = 0.1

# Директорія з кодом та медіа
source.dir = .
source.include_exts = py,png,jpg,kv,json,ttf,otf

# Включаємо всі необхідні підкаталоги
source.include_patterns = assets/**, pages/**, engine/**

# Потрібні бібліотеки
requirements = python3,kivy==2.3.1,ffpyplayer,pillow,requests,Cython==3.2.4

# Android permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Іконка та pre-splash
icon.filename = ./assets/icon.png
presplash.filename = ./assets/icon.png

# Орієнтація екрану
orientation = portrait

# Платформи Android
android.api = 33
android.minapi = 21
android.ndk = 25b
android.gradle_dependencies = 'com.android.support:multidex:1.0.3'
android.enable_multidex = True

# Інші параметри
log_level = 2
warn_on_root = 0
fullscreen = 0
window = 1
android.archs = armeabi-v7a, arm64-v8a

# Buildozer caching
android.cache = True
