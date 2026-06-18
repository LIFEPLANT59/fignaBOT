from telegram import Update
from telegram.ext import ContextTypes
from keyboards import get_back_keyboard, get_topics_keyboard
from ai_service import ask_tutor

async def handle_task_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка потока решения задач с ИИ."""
    text = update.message.text
    mode = context.user_data.get("mode")
    
    # 1. Кнопка "Помощь с задачей"
    if text == "📚 Помощь с задачей":
        await update.message.reply_text(
            "Выбери тему задачи:",
            reply_markup=get_topics_keyboard()
        )
        context.user_data["mode"] = "choosing_topic"
        return
    
    # 2. Кнопка "Назад"
    if text == "← Назад":
        context.user_data.clear()
        from handlers.commands import start
        await start(update, context)
        return
    
    # 3. Выбор темы
    if mode == "choosing_topic":
        context.user_data["topic"] = text
        context.user_data["mode"] = "waiting_for_task"
        await update.message.reply_text(
            f"Тема: {text}\n\n"
            f"Отправь условие задачи текстом.\n"
            f"Я не решу её за тебя, но помогу понять, с чего начать!",
            reply_markup=get_back_keyboard()
        )
        return
    
    # 4. Ожидание задачи
    if mode == "waiting_for_task":
        await update.message.reply_text(
            "🤔 Анализирую условие... Подожди 10-20 секунд.",
            reply_markup=get_back_keyboard()
        )
        
        topic = context.user_data.get("topic", "Физика")
        chat_history = context.user_data.get("chat_history", [])
        
        full_message = f"[Тема: {topic}]\nУсловие задачи: {text}"
        
        # Запрашиваем помощь у ИИ
        ai_response = ask_tutor(full_message, chat_history)
        
        # Проверка на пустой ответ
        if not ai_response or ai_response.strip() == "":
            ai_response = "⚠️ Произошла ошибка при получении ответа. Попробуй ещё раз.\n\nЕсли ошибка повторяется — убедись, что Ollama запущена и модель qwen3.5:4b скачана."
        
        # Сохраняем историю
        chat_history.append({"role": "user", "content": text})
        chat_history.append({"role": "assistant", "content": ai_response})
        context.user_data["chat_history"] = chat_history[-6:]
        
        # Отправляем ответ
        await update.message.reply_text(
            ai_response,
            reply_markup=get_back_keyboard(),
            parse_mode="Markdown"
        )
        return
    
    # 🔧 5. ОТЛАДКА: Если ни одно условие не сработало
    else:
        await update.message.reply_text(
            f"⚠️ Бот не понял сообщение.\n"
            f"Твой режим: `{mode}`\n"
            f"Текст: `{text}`\n\n"
            f"Нажми /start и попробуй снова."
        )
        return