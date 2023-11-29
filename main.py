# from dotenv import load_dotenv
# load_dotenv()

import streamlit as st
from lcProcess import LangChainProcess

# 페이지 제목 설정
st.title('Din. Introduce GPT')

# 세션 상태 초기화
if 'message_list' not in st.session_state:
    st.session_state.langchain = LangChainProcess("din.txt")
    st.session_state.langchain.load_text()
    st.session_state.langchain.split_text()
    st.session_state.langchain.create_embeddings()
    st.session_state['message_list'] = []

# 사용자 입력을 위한 텍스트 입력 상자 생성
user_input = st.text_input("메시지를 입력하세요:", key="user_input")

# '전송' 버튼 추가
if st.button('전송'):
    with st.spinner('Wait for it...'):
        answer = st.session_state.langchain.ask_question(user_input)
        # 입력된 텍스트를 세션 상태에 추가
        st.session_state.message_list.append(answer['result'])
        # 입력 상자 초기화를 위해 다른 방법 사용
        st.experimental_rerun()

# 입력된 모든 메시지를 채팅 박스 형태로 출력 (역순으로)
for message in st.session_state.message_list[::-1]:
    st.text_area("", value=message, height=100, disabled=True)
