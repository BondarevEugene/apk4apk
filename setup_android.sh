#!/bin/bash
set -e

echo "=== Оновлюємо систему та встановлюємо залежності ==="
sudo apt update
sudo apt install -y python3-venv python3-pip git openjdk-11-jdk unzip zlib1g-dev build-essential

echo "=== Створюємо та активуємо віртуальне оточення ==="
python3 -m venv venv
source venv/bin/activate

echo "=== Оновлюємо pip та встановлюємо buildozer ==="
pip install --upgrade pip wheel setuptools
pip install buildozer

echo "=== Ініціалізуємо buildozer.spec ==="
buildozer init

echo "=== Готово! Тепер можна збирати Android APK ==="
echo "Для збірки виконай:"
echo "  buildozer -v android debug"

# Залишаємо термінал відкритим
read -p "Натисни Enter, щоб закрити термінал..."


