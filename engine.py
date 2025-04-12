from script import TOUR_SCRIPTS
from manager import get_progress, update_progress

def get_next_sentence(user_id):
    state = get_progress(user_id)
    dept = state["department"]
    index = state["index"]

    script = TOUR_SCRIPTS.get(dept, [])
    if index < len(script):
        step = script[index]
        update_progress(user_id)
        return step["msg"], step.get("place")  # ← msg, place 튜플로 리턴
    else:
        return "여기까지가 추천 루트야! 더 보고 싶은 곳이 있으면 말해줘.", None
