import requests
from prompts import SYSTEM_PROMPT

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen3.5:4b"

def ask_tutor(user_message: str, chat_history: list = None) -> str:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if chat_history:
        messages.extend(chat_history[-4:])
    messages.append({"role": "user", "content": user_message})
    
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False,    
        "temperature": 0.3,
        "options": {"num_predict": 512}
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        content = data.get("message", {}).get("content", "").strip()
        
        if not content:
            return "️ Нейросеть вернула пустой ответ. Попробуй переформулировать задачу."
        return content
    except requests.exceptions.ConnectionError:
        return "🔌 Не удалось подключиться к Ollama. Убедись, что она запущена (`ollama serve`)."
    except requests.exceptions.Timeout:
        return "⏳ Нейросеть думает слишком долго (>120 сек). Попробуй позже."
    except Exception as e:
        return f"⚠️ Ошибка нейросети: {str(e)}"