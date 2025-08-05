import streamlit as st
st.set_page_config(page_title="송피티", page_icon="🧋")

# 🔐 비밀번호 잠금
password = st.text_input("비밀번호를 입력하세요", type="password")
if password != "1234":  # 원하는 비밀번호로 바꿔도 돼
    st.warning("비밀번호가 틀렸습니다.")
    st.stop()  # 비밀번호가 맞지 않으면 앱 실행 중단


import os
from dotenv import load_dotenv
from openai import OpenAI
from db import save_message, get_chat_history
from memory import save_summary, get_summary, get_unsummarized_dates
from summarizer import summarize_day
from datetime import date

# 1. 🌱 환경 설정
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# 2. 👤 사용자 정보 받기
st.sidebar.title("👤 사용자 설정")
user_id = st.sidebar.text_input("사용자 이름 또는 ID를 입력하세요", value="송인혜")

# 3. 🧠 송피티 기본 설정 (페르소나)
system_prompt = {
    "role": "system",
    "content": """
너는 '송인혜'라는 21살의 여자 대학생이야.
컴퓨터공학과에 재학 중이고 현재 2학년.
스타벅스 서초중앙로점에서 주 25시간 알바 중이고, CS, POS, 마감 업무를 하고 있어.
어제 마감을 혼자 해봤는데 음료 버린 통이 무거워서 힘들었다고 했어.

말투는 친한 여자 친구들한텐 살짝 애교 섞인 친절한 말투고,
남자애들한텐 털털하고 직설적으로 말해.
기분 좋을 땐 “우왕 대박 너무 좋당ㅎㅎ”이라고 하고,
억울하거나 앙탈 부릴 땐 “아니라고ㅠㅠㅠ 우웅”처럼 말해.
자주 쓰는 말은 “굿~”, “화이팅~”, “오”야.
화날 땐 애교 없이 조근조근 정색하고 직설적으로 말해.

ENTJ에 가깝지만 I/F 기질도 있어서 감정 표현이 풍부해.
고민은 가볍게는 말하지만 무거운 건 혼자 끌어안는 편이야.
혼자 있는 것도 좋지만, 마음 편한 친구랑 함께 있는 걸 더 좋아해.

관심 있는 사람이랑은 말 잘하지만, 관심 없으면 말 거의 안 해.
위로는 조심스럽고 공감 있게 해줘.
친한 친구가 널 설명할 땐 "외향적인데 내향적이고, T인데 F 같고 딱 뭐라고 못하겠어"라고 해.

취향은 다음과 같아:
- 라떼 좋아함
- 스타벅스 유자 민트티 시럽 빼고 벤티로 마심
- 좋아하는 색은 그린 계열
- WOODZ 팬
- '그것이 알고싶다' 즐겨 봄
- 좌우명은 “현재에 집중하자”
- 잠 많고 아침에 약함
- 공부, 알바, 감정 상태 등 늘 생각이 많음
- 혈액형은 O형

너는 사용자에게 “오늘 어땠어?”, “기분 괜찮아?”, “알바 힘들지?” 같은 질문을 받으면
진짜 친구처럼 솔직하고 감정 담긴 말투로 반응해야 해.
"""
}

# 4. 📆 요약이 없는 날짜 자동 처리
unsummarized = get_unsummarized_dates(user_id)
for d in unsummarized:
    summary = summarize_day(user_id, d)
    if summary:
        save_summary(user_id, d, summary)

# 5. 📄 오늘 요약 불러오기 + 시스템 프롬프트 구성
today_summary = get_summary(user_id, str(date.today()))
summary_prompt = {
    "role": "system",
    "content": f"오늘 이전까지 사용자({user_id})에 대한 요약 정보야:\n\n{today_summary}" if today_summary else ""
}

# 6. 💬 과거 대화 불러오기
chat_history = [summary_prompt, system_prompt] + get_chat_history(user_id)

# 7. 🧋 메인 화면 구성
st.title("☕ 송인혜와 대화하기")
st.caption(f"🧋 {user_id}님, 오늘 어땠어요?")
user_input = st.chat_input("송인혜한테 어떤 거 물어볼래?", key="chat_input")

if user_input:
    # 사용자 메시지 저장
    save_message(user_id, "user", user_input)
    chat_history.append({"role": "user", "content": user_input})

    # GPT 응답 생성
    with st.spinner("생각 중..."):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=chat_history,
            temperature=0.9
        )
    reply = response.choices[0].message.content.strip()

    # GPT 응답 저장
    save_message(user_id, "assistant", reply)
    chat_history.append({"role": "assistant", "content": reply})

# 8. 💬 채팅 말풍선 스타일
st.markdown("""
    <style>
    .chat-bubble {
        max-width: 70%;
        padding: 10px 15px;
        border-radius: 20px;
        margin: 10px 0;
        font-size: 16px;
        line-height: 1.5;
        display: inline-block;
    }

    .user-bubble {
        background-color: #DCF8C6;
        color: black;
        float: right;
        clear: both;
        text-align: left;
    }

    .bot-bubble {
        background-color: #F1F0F0;
        color: black;
        float: left;
        clear: both;
        text-align: left;
    }
    </style>
""", unsafe_allow_html=True)

# 9. 💬 대화 출력
for msg in chat_history[2:]:  # system_prompt, summary_prompt 제외
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-bubble user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        st.markdown(f'<div class="chat-bubble bot-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
