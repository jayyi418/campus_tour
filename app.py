
import streamlit as st
from manager import get_progress, update_progress, reset_progress
from engine import get_next_sentence
from script import TOUR_SCRIPTS
from map_display import render_map
from chatbot_gpt import recommend_place_with_gpt
from place_data import place_database
import re

# 세션 상태 초기화
if "user_id" not in st.session_state:
    st.session_state.user_id = "default_user"
if "started" not in st.session_state:
    st.session_state.started = False
if "department" not in st.session_state:
    st.session_state.department = None
if "visited_places" not in st.session_state:
    st.session_state.visited_places = []

st.title("연세대학교 캠퍼스 투어 챗봇 🎓")

# 시나리오 기반 투어
if not st.session_state.started:
    st.subheader("어떤 계열에 관심 있나요?")
    department = st.selectbox("계열 선택", list(TOUR_SCRIPTS.keys()))
    if st.button("투어 시작하기"):
        reset_progress(st.session_state.user_id)
        update_progress(st.session_state.user_id, department)
        st.session_state.started = True
        st.session_state.department = department

        msg, place = get_next_sentence(st.session_state.user_id)
        st.session_state.msg = msg
        if place:
            st.session_state.visited_places = [place]
else:
    st.write(f"👉 **{st.session_state.department} 투어 중입니다**")
    st.text_area("챗봇 응답", st.session_state.msg, height=150)
    render_map(st.session_state.visited_places)

    if st.button("OK ▶ 다음 안내"):
        msg, place = get_next_sentence(st.session_state.user_id)
        st.session_state.msg = msg
        if place and place not in st.session_state.visited_places:
            st.session_state.visited_places.append(place)

# 자유 질문 기반 GPT 챗봇
st.subheader("🗨️ 더 궁금한 게 있나요?")
user_question = st.text_input("질문해 보세요!", key="free_input")

if st.button("질문하기"):
    gpt_answer = recommend_place_with_gpt(user_question)
    st.session_state.gpt_result = gpt_answer

if "gpt_result" in st.session_state:
    answer = st.session_state.gpt_result
    st.markdown("#### GPT 추천 결과")
    st.write(answer)

    # 장소 이름 3개까지 추출 (번호 있는 형식: 1. 장소 - 이유)
    matches = re.findall(r"\d\.\s*([가-힣a-zA-Z0-9]+)", answer)
    valid_places = [name for name in matches if name in place_database]

    if valid_places:
        render_map(valid_places)
    else:
        st.warning("❗ 지도에 표시할 수 있는 장소가 없습니다.")
