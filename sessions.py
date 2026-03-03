# sessions.py

user_sessions = {}

def get_session(user_id):
    if user_id not in user_sessions:
        user_sessions[user_id] = {}
    return user_sessions[user_id]

def clear_session(user_id):
    if user_id in user_sessions:
        del user_sessions[user_id]
