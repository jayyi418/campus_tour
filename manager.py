user_states = {}

def get_progress(user_id):
    return user_states.get(user_id, {"index": 0, "department": None})

def update_progress(user_id, department=None):
    state = get_progress(user_id)
    state["index"] += 1
    if department:
        state["department"] = department
    user_states[user_id] = state

def reset_progress(user_id):
    user_states[user_id] = {"index": 0, "department": None}
