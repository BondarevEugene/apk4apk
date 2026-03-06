#!/bin/bash
# Запуск Kivy фабрики з fallback на software rendering для WSL

# Перехід у директорію скрипту
cd "$(dirname "$0")"

# Активуємо віртуальне оточення buildozer_env, якщо існує
if [ -d "buildozer_env" ]; then
    source buildozer_env/bin/activate
fi

# Встановлюємо змінні середовища Kivy для software rendering
export KIVY_GL_BACKEND=gles2   # fallback на GLES2
export KIVY_WINDOW=sdl2        # SDL2 window
export KIVY_TEXT=freetype      # text renderer

# Для WSL не використовуємо апаратний GL
export SDL_VIDEODRIVER=dummy   # dummy driver для безпечного запуску без X
export SDL_AUDIODRIVER=dummy

# Запуск фабрики
python main.py