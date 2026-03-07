import subprocess
import sys
import time
import re

# Функція для кольорового виводу
def colored(text, color):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "cyan": "\033[96m",
        "end": "\033[0m"
    }
    return f"{colors.get(color, '')}{text}{colors['end']}"

def run_buildozer():
    print(colored("🚀 Починаємо збірку DemoBook...", "cyan"))
    cmd = ["buildozer", "-v", "android", "debug", "deploy", "run", "logcat"]

    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)

        start_time = time.time()
        for line in process.stdout:
            line = line.strip()

            # Таймер
            elapsed = int(time.time() - start_time)

            # Ключові слова для категоризації
            if re.search(r'ERROR|CRITICAL', line):
                print(f"{colored('❌', 'red')} [{elapsed}s] {colored(line, 'red')}")
            elif re.search(r'WARN', line):
                print(f"{colored('⚠️', 'yellow')} [{elapsed}s] {colored(line, 'yellow')}")
            elif re.search(r'INFO', line):
                print(f"{colored('ℹ️', 'blue')} [{elapsed}s] {line}")
            elif re.search(r'->|Compiling|Packaging|Fetching', line):
                print(f"{colored('📌', 'green')} [{elapsed}s] {line}")
            else:
                print(line)

        process.wait()
        if process.returncode == 0:
            print(colored("✅ Збірка та встановлення успішні!", "green"))
        else:
            print(colored(f"❌ Buildozer завершився з кодом {process.returncode}", "red"))

    except KeyboardInterrupt:
        print(colored("\n🛑 Збірка перервана користувачем", "yellow"))
        process.kill()
        sys.exit(1)

if __name__ == "__main__":
    run_buildozer()