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
    raise ValueError("Токен не найден! Убедитесь, что файл .env содержит BOT_TOKEN")

if __name__ == "__main__":
    # Простое создание приложения — пусть система/VPN сама маршрутизирует трафик
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Регистрируем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("menu", menu_command))
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_task_flow))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_navigation))
    
    print("Бот с меню и ИИ запущен... Нажмите Ctrl+C для остановки.")
    app.run_polling()