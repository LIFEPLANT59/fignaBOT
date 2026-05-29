import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from keyboards import get_main_keyboard, get_back_keyboard, get_topics_keyboard
from handlers.commands import start, help_command, menu_command
from handlers.navigation import handle_navigation

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("Токен не найден! Убедитесь, что файл .env содержит BOT_TOKEN")

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    mode = context.user_data.get("mode")

    if text == "📚 Помощь с задачей":
        await update.message.reply_text("Выбери тему задачи:", reply_markup=get_topics_keyboard())
        context.user_data["mode"] = "choosing_topic"
        return

    if mode == "choosing_topic":
        context.user_data["topic"] = text
        context.user_data["mode"] = "waiting_for_task"
        await update.message.reply_text(
            f"Ты выбрал тему: {text}. Теперь отправь условие задачи (текстом или фото).",
            reply_markup=get_back_keyboard()
        )
    elif mode == "waiting_for_task":
        await update.message.reply_text("Задача получена! Ищу подсказку... (пока заглушка)", reply_markup=get_back_keyboard())
        context.user_data["mode"] = "choosing_topic"
    elif mode == "choosing_lab":
        if text in ["1", "2", "3"]:
            await update.message.reply_text(f"Информация по лабораторной работе №{text} появится позже.", reply_markup=get_back_keyboard())
        else:
            await update.message.reply_text("Пожалуйста, выбери номер 1, 2 или 3.", reply_markup=get_back_keyboard())
    elif mode == "scientists":
        if "ньютон" in text.lower():
            await update.message.reply_text("Исаак Ньютон — английский физик, математик и астроном. Сформулировал законы движения и закон всемирного тяготения.", reply_markup=get_back_keyboard())
        else:
            await update.message.reply_text(f"Информация об учёном '{text}' появится позже.", reply_markup=get_back_keyboard())
    else:
        await update.message.reply_text("Пожалуйста, используй кнопки меню.", reply_markup=get_main_keyboard())

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("menu", menu_command))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_navigation))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))

    print("Бот с меню запущен... Нажмите Ctrl+C для остановки.")
    app.run_polling()