[app]

# Основні параметри додатку
title = Phoenix Factory
package.name = factory
package.domain = org.example
source.dir = .
source.include_exts = py,kv,png,json
source.include_patterns = assets/**, pages/**, engine/**

version = 0.1
requirements = python3,kivy

# Права Android
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Іконка та заставка
icon.filename = assets/phoenix.png
presplash.filename = ./assets/icon.png

# Орієнтація
orientation = portrait

# Android специфіка
android.api = 33
android.minapi = 21
android.ndk = 25b
android.gradle_dependencies = 'com.android.support:multidex:1.0.3'
android.enable_multidex = True

# Buildozer логування
log_level = 2
warn_on_root = 0

# Візуальні налаштування для прогресбару
# Кастомізоване логування у Python скрипті
