# auto_run.ps1 — запуск Factory на Windows
# Перехід у каталог скрипта
Set-Location -Path $PSScriptRoot

# Перевірка віртуального оточення
$venvPath = ".\.venv\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    Write-Host "Активую віртуальне оточення..."
    & $venvPath
} else {
    Write-Host "Віртуальне оточення не знайдено! Створіть його командою: python -m venv .venv"
    exit 1
}

# Встановлюємо backend Kivy для Windows
$env:KIVY_GL_BACKEND = "sdl2"

# Запуск main.py
if (Test-Path ".\main.py") {
    Write-Host "Запускаю Factory..."
    python .\main.py
    Write-Host "Завершено."
} else {
    Write-Host "main.py не знайдено у поточній директорії!"
    exit 1
}