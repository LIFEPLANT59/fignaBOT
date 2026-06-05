from telegram import Update
from telegram.ext import ContextTypes
from keyboards import get_main_keyboard, get_back_keyboard
from handlers.commands import start

async def handle_navigation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    mode = context.user_data.get("mode")

    if mode in ("choosing_topic", "waiting_for_task"):
        return

    if text == "🔬 Лабораторные работы":
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

    elif text == "👨‍ Учёные":
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
            "• Что будет, если я не сдам?\n"
            "• Сколько баллов нужно для хорошей оценки?\n"
            "• Можно ли подготовиться к физике за короткий срок?\n"
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