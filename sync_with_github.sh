#!/bin/bash
# Скрипт синхронізації локального master з GitHub
# Спінер + кольорові сповіщення

# Кольори
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # Без кольору

# Функція спінера
spin() {
    local -r pid=$1
    local -r delay=0.1
    local spinstr='|/-\'
    while ps -p $pid &>/dev/null; do
        for i in $(seq 0 3); do
            printf "\r%s" "${spinstr:$i:1}"
            sleep $delay
        done
    done
    printf "\r"
}

echo -e "${YELLOW}🔹 Перевірка статусу репозиторію...${NC}"
git status

# Перевірка на незавершене злиття
if git merge HEAD >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️ Незавершене злиття знайдено, скасовую...${NC}"
    git merge --abort
fi

echo -e "${YELLOW}🔹 Додаю всі локальні зміни...${NC}"
git add . & spin $!
echo -e "${GREEN}✅ Додано${NC}"

echo -e "${YELLOW}🔹 Комітую локальні зміни...${NC}"
git commit -m "Sync: latest local changes from PyCharm" & spin $!
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Коміт завершено${NC}"
else
    echo -e "${YELLOW}⚠️ Немає нових змін для коміту${NC}"
fi

echo -e "${YELLOW}🔹 Форсований пуш на GitHub...${NC}"
git push -f origin master & spin $!
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Пуш завершено${NC}"
else
    echo -e "${RED}🔴 Помилка при пуші!${NC}"
fi

echo -e "${GREEN}🎉 Локальні зміни успішно синхронізовані з GitHub!${NC}"
chmod +x sync_with_github.sh
