# summarizer.py
from openai import OpenAI
import os
from dotenv import load_dotenv
from db import get_chat_history_by_date

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_day(user_id, date):
    history = get_chat_history_by_date(user_id, date)
    if not history:
        return None

    messages = [{"role": row["role"], "content": row["content"]} for row in history]

    system_prompt = {
        "role": "system",
        "content": "아래는 하루 동안의 사용자와 송피티의 대화야. 주요 감정, 관심사, 어려움, 기분 변화 등을 중심으로 요약해줘. 문장은 자연스럽게 써줘."
    }

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[system_prompt] + messages,
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()
