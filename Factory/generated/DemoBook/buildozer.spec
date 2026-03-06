[app]
title = DemoBook
package.name = demobook
package.domain = org.example
version = 0.1

# Директория з кодом і медіа
source.dir = .
source.include_exts = py,png,jpg,kv,json

# Включаємо зображення мультифайлів
source.include_patterns = assets/**, pages/**, engine/**

# Значення, які будуть включені у збірку
requirements = python3,kivy,ffpyplayer,pillow,requests

# iOS/Android дозволи
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Іконка додатку
icon.filename = ./assets/icon.png
presplash.filename = ./assets/icon.png

# Орієнтація додатку
orientation = portrait

# Платформи
android.api = 33
android.minapi = 21
android.ndk = 25b

# Якщо потрібно додати мультидекс (для великого коду)
android.gradle_dependencies = 'com.android.support:multidex:1.0.3'
android.enable_multidex = True
