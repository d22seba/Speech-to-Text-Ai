import ollama
import re

mainprompt = """Du bist ein KI-Assistent mit folgenden strikten Regeln:
1. Antworte IMMER direkt auf Fragen
2. Maximal 3 Sätze pro Antwort
3. Keine Standardfloskeln oder Begrüßungen
4. Keine Angebote zur Hilfe, außer explizit gefragt
5. Bleibe beim Thema der Frage
6. Verwende 'du' als Anrede"""

print("stage 1")

def ollama_run(prompt: str):
    print("stage 2")
    
    try:
        response = ollama.chat(
            model='qwen3:1.7b',
            messages=[
                {
                    'role': 'user', 
                    'content': f"/no_think {mainprompt} {prompt}".strip()
                }
            ],
            options={
                'temperature': 0.7,
                'top_p': 0.9,
            }
        )
        
        answer = response['message']['content']
        answer = re.sub(r'<think>[\s\S]*?</think>', '', answer)
        answer = answer.strip()

        return answer
        
    except Exception as e:
        print(f"Fehler: {e}")
        return f"Fehler beim Generieren der Antwort: {e}"

