import requests
from langchain_core.runnables import RunnableLambda

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:1.5b"

def local_llm(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0,
            "num_predict": 128
        }
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    return response.json()["response"]

llm = RunnableLambda(local_llm)
try:
    print(
        llm.invoke("Translate English to French: Hello, how are you?")
    )
except Exception as e:
    print("Error invoking local LLM:", e)
