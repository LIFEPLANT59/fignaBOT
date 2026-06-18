from telegram import Update
from telegram.ext import ContextTypes
from keyboards import get_main_keyboard, get_back_keyboard, get_topics_keyboard
from ai_service import ask_tutor
from handlers.commands import start

async def handle_task_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    mode = context.user_data.get("mode")
    stats = context.user_data.setdefault("stats", {})
    
    print(f"!!! ПОЛУЧЕНО СООБЩЕНИЕ: '{text}'")
    print(f"!!! ТЕКУЩИЙ РЕЖИМ: {mode}")

    if text == " Помощь с задачей":
        await update.message.reply_text("Выбери тему задачи:", reply_markup=get_topics_keyboard())
        context.user_data["mode"] = "choosing_topic"
        return
    
    if text == "← Назад":
        context.user_data.clear()
        await start(update, context)
        return
    
    if mode == "choosing_topic":
        context.user_data["topic"] = text
        context.user_data["mode"] = "waiting_for_task"
        await update.message.reply_text(
            f"Тема: {text}\n\nОтправь условие задачи текстом.",
            reply_markup=get_back_keyboard()
        )
        return
    
    if mode == "waiting_for_task":
        await update.message.reply_text("🤔 Анализирую условие...", reply_markup=get_back_keyboard())
        
        topic = context.user_data.get("topic", "Физика")
        chat_history = context.user_data.get("chat_history", [])
        full_message = f"[Тема: {topic}]\nУсловие задачи: {text}"
        
        ai_response = ask_tutor(full_message, chat_history)
        print(f"!!! ПЕРЕМЕННАЯ ОТВЕТА: '{ai_response}'")
        
        if not ai_response or not ai_response.strip():
            ai_response = "Ошибка: Ответ от ИИ пустой. Проверь консоль PowerShell."
            
        chat_history.append({"role": "user", "content": text})
        chat_history.append({"role": "assistant", "content": ai_response})
        context.user_data["chat_history"] = chat_history[-6:]
        
        await update.message.reply_text(ai_response, reply_markup=get_back_keyboard())
        return

    if not mode:
        if text == "🔬 Лабораторные работы":
            await update.message.reply_text("Список лабораторных работ:\n1. Ускорение свободного падения\n2. Жёсткость пружины\n3. Закон Ома", reply_markup=get_back_keyboard())
            return
        if text == " Теория":
            await update.message.reply_text("Раздел теории в разработке.", reply_markup=get_back_keyboard())
            return
        if text == "‍🔬 Учёные":
            await update.message.reply_text("Выбери учёного:\n- Ньютон\n- Эйнштейн\n- Ломоносов", reply_markup=get_back_keyboard())
            return
        if text == "❓ Частые вопросы":
            await update.message.reply_text("FAQ скоро появится.", reply_markup=get_back_keyboard())
            return
        if text == "⭐ Избранное":
            await update.message.reply_text("Избранное пока пусто.", reply_markup=get_back_keyboard())
            return
        if text == "📊 Статистика":
            await update.message.reply_text(f"Статистика:\n- Открытий меню: {stats.get('menu_opens', 0)}", reply_markup=get_back_keyboard())
            return

    await update.message.reply_text("Не понял команду. Нажми /start.", reply_markup=get_main_keyboard())