from telegram import Update
from telegram.ext import ContextTypes
from keyboards import get_main_keyboard

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats = context.user_data.setdefault("stats", {})
    stats["menu_opens"] = stats.get("menu_opens", 0) + 1
    
    greeting = "Привет!"  
    
    await update.message.reply_text(
        f"{greeting} Я твой личный репетитор по физике.\n"
        f"Я не буду решать задачи за тебя, но научу решать их самостоятельно!\n"
        f"Выбери раздел, нажав на кнопку ниже.\n"
        f"(Это твой {stats['menu_opens']}-й визит в меню)",
        reply_markup=get_main_keyboard()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Я помогу тебе с физикой!\n\n"
        "Доступные команды:\n"
        "/start — показать главное меню\n"
        "/menu — открыть меню разделов\n"
        "/help — эта справка\n\n"
        "Я не решаю задачи за тебя, но помогу понять суть и научиться решать самостоятельно!"
    )

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)