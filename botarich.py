import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)


load_dotenv()


TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("Токен не найден! Убедитесь, что файл .env содержит BOT_TOKEN")


def get_main_keyboard():
    keyboard = [
        ["📚 Помощь с задачей", "🔬 Лабораторные работы"],
        ["📖 Теория", "👨‍🔬 Учёные"],
        ["❓ Частые вопросы", "⭐ Избранное"],  
        ["📊 Статистика"]  
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_back_keyboard():
    keyboard = [["← Назад"]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_topics_keyboard():
    keyboard = [
        ["Механика", "Термодинамика"],
        ["Электричество", "Оптика"],
        ["Квантовая физика", "← Назад"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    stats = context.user_data.setdefault("stats", {})
    stats["menu_opens"] = stats.get("menu_opens", 0) + 1
    await update.message.reply_text(
        f"Привет! Я твой личный репетитор по физике.\n"
        f"Выбери раздел, нажав на кнопку ниже.\n"
        f"(Это твой {stats['menu_opens']}-й визит в меню)",
        reply_markup=get_main_keyboard()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Я помогу тебе с физикой!\n"
        "Используй кнопки меню для навигации.\n"
        "/start — показать меню\n"
        "/help — эта справка"
    )

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)


async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📚 Помощь с задачей":
        await update.message.reply_text(
            "Выбери тему задачи:",
            reply_markup=get_topics_keyboard()
        )
        context.user_data["mode"] = "choosing_topic"

    elif text == "🔬 Лабораторные работы":
        await update.message.reply_text(
            "Список лабораторных работ:\n"
            "1. Определение ускорения свободного падения\n"
            "2. Измерение жёсткости пружины\n"
            "3. Проверка закона Ома\n\n"
            "Напиши номер работы (1, 2 или 3), чтобы получить подробности.",
            reply_markup=get_back_keyboard()
        )
        context.user_data["mode"] = "choosing_lab" 

    elif text == "📖 Теория":
        
        stats = context.user_data.setdefault("stats", {})
        stats["theory_views"] = stats.get("theory_views", 0) + 1
        await update.message.reply_text(
            f"Раздел теории в разработке. Скоро здесь появятся темы.\n"
            f"(Ты открывал этот раздел {stats['theory_views']} раз)",
            reply_markup=get_back_keyboard()
        )
        context.user_data["mode"] = "theory"

    elif text == "👨‍🔬 Учёные":
        await update.message.reply_text(
            "Выбери учёного (пока просто пример):\n"
            "- Ньютон\n"
            "- Эйнштейн\n"
            "- Ломоносов",
            reply_markup=get_back_keyboard()
        )
        context.user_data["mode"] = "scientists"

    elif text == "❓ Частые вопросы":
        await update.message.reply_text(
            "Часто спрашивают:\n"
            "• Как готовиться к ЕГЭ по физике?\n"
            "• Сколько баллов нужно для четвёрки?\n"
            "• Нужен ли репетитор?\n\n"
            "Скоро здесь появятся подробные ответы.",
            reply_markup=get_back_keyboard()
        )
        context.user_data["mode"] = "faq"

    elif text == "⭐ Избранное": 
        await update.message.reply_text(
            "Раздел 'Избранное'. Здесь будут храниться ваши сохранённые задачи и теория.",
            reply_markup=get_back_keyboard()
        )
        context.user_data["mode"] = "favorites"

    elif text == "📊 Статистика":  
        stats = context.user_data.get("stats", {})
        opens = stats.get("menu_opens", 0)
        theory_views = stats.get("theory_views", 0)
        await update.message.reply_text(
            f"Ваша статистика:\n"
            f"- Открытий главного меню: {opens}\n"
            f"- Посещений раздела 'Теория': {theory_views}",
            reply_markup=get_back_keyboard()
        )
        context.user_data["mode"] = "stats"

    elif text == "← Назад":
        await start(update, context)
        context.user_data.pop("mode", None)

    else:
        mode = context.user_data.get("mode")
        if mode == "choosing_topic":
            await update.message.reply_text(
                f"Ты выбрал тему: {text}. Теперь отправь условие задачи (текстом или фото).",
                reply_markup=get_back_keyboard()
            )
            context.user_data["topic"] = text
            context.user_data["mode"] = "waiting_for_task"
        elif mode == "waiting_for_task":
            await update.message.reply_text(
                "Задача получена! Ищу подсказку... (пока заглушка)",
                reply_markup=get_back_keyboard()
            )
            context.user_data["mode"] = "choosing_topic"
        elif mode == "choosing_lab":
            if text in ["1", "2", "3"]:
                await update.message.reply_text(
                    f"Информация по лабораторной работе №{text} появится позже.",
                    reply_markup=get_back_keyboard()
                )
            else:
                await update.message.reply_text(
                    "Пожалуйста, выбери номер 1, 2 или 3.",
                    reply_markup=get_back_keyboard()
                )
        elif mode == "scientists":
            if "ньютон" in text.lower():
                await update.message.reply_text(
                    "Исаак Ньютон — английский физик, математик и астроном. "
                    "Сформулировал законы движения и закон всемирного тяготения.",
                    reply_markup=get_back_keyboard()
                )
            else:
                await update.message.reply_text(
                    f"Информация об учёном '{text}' появится позже.",
                    reply_markup=get_back_keyboard()
                )
        else:
            await update.message.reply_text(
                "Пожалуйста, используй кнопки меню.",
                reply_markup=get_main_keyboard()
            )


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("menu", menu_command))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))

    print("Бот с меню запущен... Нажмите Ctrl+C для остановки.")
    app.run_polling()