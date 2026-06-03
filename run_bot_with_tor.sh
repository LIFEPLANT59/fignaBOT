#!/bin/bash

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}=== Запуск бота FIGNABOT через Tor ===${NC}"

# Проверка, запущен ли Tor
echo -e "${YELLOW}1. Проверка статуса Tor...${NC}"
if systemctl is-active --quiet tor; then
    echo -e "${GREEN}✓ Tor запущен${NC}"
else
    echo -e "${RED}✗ Tor не запущен. Запускаем...${NC}"
    sudo systemctl start tor
    sleep 3
fi

# Проверка, что Tor слушает порт 9050 (используем ss вместо netstat)
echo -e "${YELLOW}2. Проверка прокси-сервера Tor...${NC}"
if ss -tln | grep -q ":9050"; then
    echo -e "${GREEN}✓ Tor прокси активен (порт 9050)${NC}"
else
    echo -e "${RED}✗ Tor не слушает порт 9050${NC}"
    exit 1
fi

# Активация виртуального окружения
echo -e "${YELLOW}3. Активация виртуального окружения...${NC}"
source .venv/bin/activate

# Установка необходимых библиотек для SOCKS5
echo -e "${YELLOW}4. Установка зависимостей для SOCKS5 прокси...${NC}"
pip install 'httpx[socks]' pysocks python-dotenv -q

# Запуск бота с прокси
echo -e "${GREEN}5. Запуск бота...${NC}"
echo -e "${YELLOW}Бот будет использовать Tor для подключения к Telegram API${NC}"
echo -e "${YELLOW}Для остановки нажмите Ctrl+C${NC}\n"

# Установка переменной окружения для прокси
export ALL_PROXY=socks5://127.0.0.1:9050
export https_proxy=socks5://127.0.0.1:9050
export http_proxy=socks5://127.0.0.1:9050

# Запуск бота
python botarich.py