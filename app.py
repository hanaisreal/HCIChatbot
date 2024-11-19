import streamlit as st
from openai import OpenAI

# OpenAI 클라이언트 설정
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 타이틀
st.title("상담사 챗봇")

# 세션 상태 초기화
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "chat_enabled" not in st.session_state:
    st.session_state.chat_enabled = False
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = ""

# 사이드바: 유저 정보 입력
st.sidebar.title("사용자 정보 입력")

name = st.sidebar.text_input("이름")
age = st.sidebar.text_input("나이")
career = st.sidebar.text_input("경력")
interests = st.sidebar.text_input("관심사")
other_info = st.sidebar.text_area("기타사항")

# 유저 정보 제출
if st.sidebar.button("Submit"):
    user_info = f"이름: {name}\n나이: {age}\n경력: {career}\n관심사: {interests}\n기타사항: {other_info}"
    system_prompt = f"""당신은 친절한 조언자입니다. 아래는 사용자 정보입니다:
{user_info}
사용자에게 인사말을 전해주세요."""
    st.session_state.system_prompt = system_prompt

    # GPT로부터 인사말 생성
    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[{"role": "system", "content": system_prompt}],
    )
    greeting = response.choices[0].message.content.strip()

    # 인사말만 메시지로 추가
    st.session_state.messages.append({"role": "assistant", "content": greeting})
    st.session_state.chat_enabled = True

# 채팅 인터페이스
if st.session_state.chat_enabled:
    # 이전 대화 출력
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력
    if prompt := st.chat_input("질문이나 고민을 물어보세요:"):
        # 유저 메시지 추가
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # GPT로부터 응답 생성
        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            )
            reply = response.choices[0].message.content.strip()
            st.markdown(reply)

        # GPT 응답 메시지 추가
        st.session_state.messages.append({"role": "assistant", "content": reply})
else:
    st.markdown(
        """
        <div style='display: flex; justify-content: center; align-items: center; height: 60vh;'>
            <div style='background-color: #F0F0F0; padding: 20px; border-radius: 5px; text-align: center;'>
                <p style='font-size: 18px; margin: 0;'>사용자 정보를 제출하신 후 채팅을 시작하실 수 있습니다 :)</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
