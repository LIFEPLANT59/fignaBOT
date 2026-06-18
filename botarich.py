import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from telegram.request import HTTPXRequest

from keyboards import get_main_keyboard
from handlers.commands import start, help_command, menu_command
from handlers.navigation import handle_navigation
from handlers.task_solver import handle_task_flow

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("Токен не найден! Проверь файл .env")

if __name__ == "__main__":
    # ИСПРАВЛЕНИЕ:
    # Правильный аргумент — "proxy" (без _url)
    # В WSL лучше использовать localhost:9050 (если запущен Tor)
    # Или IP твоего ПК с Karing (например host.docker.internal:10808)
    
    # Тестовая настройка (попробуй этот вариант):
    PROXY_URL = "socks5://127.0.0.1:9050" 

    request = HTTPXRequest(proxy=PROXY_URL)
    
    app = ApplicationBuilder().token(TOKEN).request(request).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("menu", menu_command))
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_task_flow))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_navigation))
    
    print("Бот запущен...")
    app.run_polling()