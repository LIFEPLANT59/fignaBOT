import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from keyboards import get_main_keyboard
from handlers.commands import start, help_command, menu_command
from handlers.navigation import handle_navigation
from handlers.task_solver import handle_task_flow

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("Токен не найден! Проверь файл .env")

if __name__ == "__main__":
    # Karing перехватывает трафик на уровне системы. Прокси в коде не нужен.
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("menu", menu_command))
    
    # Порядок важен: task_solver должен идти первым, чтобы перехватывать задачи
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_task_flow))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_navigation))
    
    print("✅ Бот запущен. Жду сообщений в Telegram...")
    app.run_polling()