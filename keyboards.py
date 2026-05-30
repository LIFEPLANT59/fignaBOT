from telegram import ReplyKeyboardMarkup

def get_main_keyboard():
    return ReplyKeyboardMarkup([
        ["📚 Помощь с задачей", "🔬 Лабораторные работы"],
        ["📖 Теория", "👨‍ Учёные"],
        ["❓ Частые вопросы", "⭐ Избранное"],
        ["📊 Статистика"]
    ], resize_keyboard=True)

def get_back_keyboard():
    return ReplyKeyboardMarkup([["← Назад"]], resize_keyboard=True)

def get_topics_keyboard():
    return ReplyKeyboardMarkup([
        ["Механика", "Термодинамика"],
        ["Электричество", "Оптика"],
        ["Квантовая физика", "← Назад"]
    ], resize_keyboard=True)