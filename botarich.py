import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from telegram.request import HTTPXRequest
from keyboards import get_main_keyboard
from handlers.commands import start, help_command, menu_command
from handlers.navigation import handle_navigation
from handlers.task_solver import handle_task_flow
import httpx

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

# Проверка, используем ли мы Tor через переменные окружения
use_tor = os.environ.get('ALL_PROXY') or os.environ.get('https_proxy')

if use_tor:
    print("🔒 Бот запущен через Tor прокси")
    # Создаем кастомный HTTPX клиент с прокси
    http_client = httpx.AsyncClient(
        proxies="socks5://127.0.0.1:9050",
        timeout=httpx.Timeout(60.0, connect=60.0),
        http2=False
    )
    request = HTTPXRequest(http_client=http_client)
else:
    print("🚀 Бот запущен без прокси")
    # Обычная настройка
    request = HTTPXRequest(
        connect_timeout=60.0,
        read_timeout=60.0,
        write_timeout=60.0,
        pool_timeout=60.0,
        http_version="1.1",
    )

if not TOKEN:
    raise ValueError("Токен не найден! Убедитесь, что файл .env содержит BOT_TOKEN")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).request(request).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("menu", menu_command))
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_task_flow))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_navigation))
    
    print("Бот с меню и ИИ запущен... Нажмите Ctrl+C для остановки.")
    app.run_polling()