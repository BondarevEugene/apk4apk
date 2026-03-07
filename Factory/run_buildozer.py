#!/usr/bin/env python3
import subprocess
import sys
import threading
import queue
import os
from time import sleep


# --- Кольори для підсвічування ---
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


# --- Функція потокового читання процесу ---
def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()


def run_buildozer(target="android debug", log_file="buildozer_run.log"):
    print(f"{bcolors.HEADER}Запуск Buildozer: {target}{bcolors.ENDC}\n")

    # Створюємо лог-файл
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"--- Buildozer log ---\nTarget: {target}\n\n")

    # Команда
    cmd = ["buildozer"] + target.split()

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1,
                               universal_newlines=True)

    q = queue.Queue()
    t = threading.Thread(target=enqueue_output, args=(process.stdout, q))
    t.daemon = True
    t.start()

    step = 0
    try:
        while True:
            try:
                line = q.get_nowait()
            except queue.Empty:
                if process.poll() is not None:
                    break
                sleep(0.1)
                continue

            # Лог у файл
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(line)

            # Підсвічування
            line_clean = line.strip()
            if "ERROR" in line_clean or "FAILED" in line_clean or "Traceback" in line_clean:
                print(f"{bcolors.FAIL}{line_clean}{bcolors.ENDC}")
            elif "INFO" in line_clean or "OK" in line_clean:
                print(f"{bcolors.OKGREEN}{line_clean}{bcolors.ENDC}")
            elif "WARNING" in line_clean:
                print(f"{bcolors.WARNING}{line_clean}{bcolors.ENDC}")
            else:
                print(line_clean)

            # Прогресбар простий: лічильник рядків
            step += 1
            if step % 20 == 0:
                print(f"{bcolors.OKBLUE}... {step} рядків логів ...{bcolors.ENDC}")

    except KeyboardInterrupt:
        print(f"{bcolors.FAIL}\nЗбірка перервана користувачем{bcolors.ENDC}")
        process.terminate()
        sys.exit(1)

    process.wait()
    retcode = process.returncode
    if retcode == 0:
        print(f"{bcolors.OKGREEN}\nBuildozer завершився успішно!{bcolors.ENDC}")
    else:
        print(f"{bcolors.FAIL}\nBuildozer завершився з помилкою. Код: {retcode}{bcolors.ENDC}")

    print(f"Лог збережено у {log_file}")


if __name__ == "__main__":
    # Перевірка, що ми у віртуальному середовищі
    if not os.getenv("VIRTUAL_ENV"):
        print(f"{bcolors.WARNING}Рекомендую активувати virtualenv перед запуском.{bcolors.ENDC}")

    run_buildozer()