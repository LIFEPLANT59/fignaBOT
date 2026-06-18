from telegram import Update
from telegram.ext import ContextTypes
from keyboards import get_main_keyboard, get_back_keyboard, get_topics_keyboard
from ai_service import ask_tutor
from handlers.commands import start

async def handle_task_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    mode = context.user_data.get("mode")
    stats = context.user_data.setdefault("stats", {})

    # 1. Глобальная кнопка "Назад" (работает в любом режиме)
    if text == "← Назад":
        context.user_data.clear()
        await start(update, context)
        return

    # 2. Вход в раздел "Задачи"
    if text == "📚 Помощь с задачей":
        await update.message.reply_text("Выбери тему задачи:", reply_markup=get_topics_keyboard())
        context.user_data["mode"] = "choosing_topic"
        return

    # 3. Выбор темы
    if mode == "choosing_topic":
        context.user_data["topic"] = text
        context.user_data["mode"] = "waiting_for_task"
        await update.message.reply_text(
            f"Тема: {text}\n\nОтправь условие задачи текстом.\nЯ не решу её за тебя, но помогу понять, с чего начать!",
            reply_markup=get_back_keyboard()
        )
        return

    # 4. Решение задачи (ИИ)
    if mode == "waiting_for_task":
        await update.message.reply_text("🤔 Анализирую условие... Подожди 10-20 секунд.", reply_markup=get_back_keyboard())
        
        topic = context.user_data.get("topic", "Физика")
        chat_history = context.user_data.get("chat_history", [])
        full_message = f"[Тема: {topic}]\nУсловие задачи: {text}"
        
        ai_response = ask_tutor(full_message, chat_history)
        
        if not ai_response or ai_response.strip() == "":
            ai_response = "⚠️ Нейросеть не ответила. Попробуй ещё раз или проверь запуск Ollama."
        
        chat_history.append({"role": "user", "content": text})
        chat_history.append({"role": "assistant", "content": ai_response})
        context.user_data["chat_history"] = chat_history[-6:]
        
        await update.message.reply_text(ai_response, reply_markup=get_back_keyboard(), parse_mode="Markdown")
        return

    # 5. Кнопки главного меню (работают, когда mode не задан)
    if text == "🔬 Лабораторные работы":
        await update.message.reply_text("Список лабораторных работ:\n1. Ускорение свободного падения\n2. Жёсткость пружины\n3. Закон Ома\n\nНапиши номер работы.", reply_markup=get_back_keyboard())
        context.user_data["mode"] = "choosing_lab"
        return

    if text == "📖 Теория":
        stats["theory_views"] = stats.get("theory_views", 0) + 1
        await update.message.reply_text(f"Раздел теории в разработке. (Открыто {stats['theory_views']} раз)", reply_markup=get_back_keyboard())
        return

    if text == "👨‍🔬 Учёные":
        await update.message.reply_text("Выбери учёного:\n- Ньютон\n- Эйнштейн\n- Ломоносов", reply_markup=get_back_keyboard())
        context.user_data["mode"] = "scientists"
        return

    if text == "❓ Частые вопросы":
        await update.message.reply_text("Часто спрашивают:\n• Как подготовиться к ЕГЭ?\n• Нужен ли репетитор?\n• Сколько времени учить?\n\nОтветы скоро появятся.", reply_markup=get_back_keyboard())
        return

    if text == "⭐ Избранное":
        await update.message.reply_text("Раздел 'Избранное' пока пуст. Сохраняй задачи, они появятся здесь.", reply_markup=get_back_keyboard())
        return

    if text == " Статистика":
        await update.message.reply_text(f"Статистика:\n- Открытий меню: {stats.get('menu_opens', 0)}\n- Просмотров теории: {stats.get('theory_views', 0)}", reply_markup=get_back_keyboard())
        return

    # 6. Фоллбэк
    await update.message.reply_text("Я не распознал команду. Нажми /start или используй кнопки меню.", reply_markup=get_main_keyboard())