from telegram import Update
from telegram.ext import ContextTypes
from keyboards import get_back_keyboard, get_topics_keyboard, get_main_keyboard
from ai_service import ask_tutor
from handlers.commands import start

async def handle_task_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка потока решения задач с ИИ."""
    text = update.message.text
    mode = context.user_data.get("mode")
    
    
    if text == "📚 Помощь с задачей":
        await update.message.reply_text(
            "Выбери тему задачи:",
            reply_markup=get_topics_keyboard()
        )
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
            f"Тема: {text}\n\n"
            f"Отправь условие задачи текстом.\n"
            f"Я не решу её за тебя, но помогу понять, с чего начать!",
            reply_markup=get_back_keyboard()
        )
        return
    
    
    if mode == "waiting_for_task":
        await update.message.reply_text(
            "🤔 Анализирую условие... Подожди 10-20 секунд.",
            reply_markup=get_back_keyboard()
        )
        
        topic = context.user_data.get("topic", "Физика")
        chat_history = context.user_data.get("chat_history", [])
        
       
        full_message = f"[Тема: {topic}]\nУсловие задачи: {text}"
        
       
        ai_response = ask_tutor(full_message, chat_history)
        
        
        chat_history.append({"role": "user", "content": text})
        chat_history.append({"role": "assistant", "content": ai_response})
        context.user_data["chat_history"] = chat_history[-6:]
        
        
        await update.message.reply_text(
            ai_response,
            reply_markup=get_back_keyboard(),
            parse_mode="Markdown"
        )
        
        context.user_data["mode"] = "waiting_for_task"
        return