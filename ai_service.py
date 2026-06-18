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
    
    print(f"[AI] Отправляю запрос к Ollama...")
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        print(f"[AI] Статус ответа: {response.status_code}")
        
        if response.status_code != 200:
            return f"Ошибка сервера Ollama: {response.text}"
            
        data = response.json()
        content = data.get("message", {}).get("content", "").strip()
        
        if not content:
            print("[AI] Модель вернула пустой контент!")
            return "Нейросеть вернула пустой ответ. Попробуй переформулировать."
            
        print(f"[AI] Ответ получен (длина: {len(content)} символов)")
        return content
        
    except requests.exceptions.ConnectionError:
        print("[AI] ОШИБКА: Нет соединения с localhost:11434. Ollama запущена?")
        return "ОШИБКА: Не удалось подключиться к Ollama. Убедись, что она запущена командой 'ollama serve'."
    except Exception as e:
        print(f"[AI] КРИТИЧЕСКАЯ ОШИБКА: {str(e)}")
        return f"Ошибка: {str(e)}"