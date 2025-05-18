import os
from dotenv import load_dotenv
import requests

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")



def get_llm_insight(prompt: str):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Insight Analyzer",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [
            {"role": "system", "content": "You are a data science expert. Provide deep, clear insights into datasets."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 2048,
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"
