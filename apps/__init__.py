
from fastapi import Request

SESSION_USER_KEY = "user-session-key"

# 自定义异常基类（可选）
class RagException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail



async def get_current_user(request: Request):
    session = request.session
    if not session:
        return None
    session_user = session.get(SESSION_USER_KEY)
    if not session_user:
       return None
    return session_user


def get_response_data(code: int = 0, message: str = 'success', data: dict = {}):
    return {"code": code, "message": message, "data": data}