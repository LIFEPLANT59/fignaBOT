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
        return response.json()["message"]["content"]
    except requests.exceptions.ConnectionError:
        return "️ Не удалось подключиться к нейросети. Убедись, что Ollama запущена (`ollama serve`)."
    except Exception as e:
        return f"⚠️ Ошибка: {e}"