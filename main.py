# from dotenv import load_dotenv
# load_dotenv()

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

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
    if user_input:  # 입력이 있을 경우
        with st.spinner('Wait for it...'):
            answer = st.session_state.langchain.ask_question(user_input)
            st.session_state.message_list.append(answer['result'])
        # 입력 상자 초기화
        st.experimental_rerun()

# 메시지의 길이에 따라 텍스트 상자의 높이를 조절하는 함수
def calculate_text_area_height(text):
    # 대략적인 한 줄의 문자 수
    characters_per_line = 40
    # 메시지를 줄 단위로 나누고, 각 줄의 길이를 계산
    lines = text.split('\n')
    total_lines = sum(len(line) // characters_per_line + 1 for line in lines)
    # 높이 계산 (한 줄당 높이를 25px로 가정)
    height = total_lines * 25
    return max(height, 50)  # 최소 높이를 50px로 설정

# 입력된 모든 메시지를 채팅 박스 형태로 출력 (역순으로)
for message in st.session_state.message_list[::-1]:
    text_area_height = calculate_text_area_height(message)
    st.text_area("", value=message, height=text_area_height, disabled=True)
