

import logging
import re
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field
from service import userService
from apps import get_current_user
from apps import get_response_data
from apps import SESSION_USER_KEY


class UserPayload(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="用户名")
    password: str = Field(..., min_length=1, max_length=50, description="密码")


userRouter = APIRouter()
tagName = "user"
@userRouter.post("/api/v1/user/create",tags=[tagName],summary="创建用户",description="创建用户")
async def create_user(reqeust: Request, payload: UserPayload):

    # 校验是否重名
    result = userService.is_name_exist(payload.name)
    if result:
        return get_response_data(code=1, message="用户名已存在")
    result = userService.create_user(payload.name, payload.password)
    return get_response_data(data=result)

@userRouter.post("/api/v1/user/login",tags=[tagName],summary="用户登录",description="用户登录")
async def user_login(reqeust: Request, payload: UserPayload):
    reqeust.session.update({SESSION_USER_KEY: None})
    reqeust.session.clear()
    result = userService.get_user_by_name_and_password(payload.name, payload.password)
    if not result:
        return get_response_data(code=1, message="用户名或密码错误")

    result["password"] = "******"
    session_data = {SESSION_USER_KEY: {"user_name":result["name"],"user_id":result["id"]}}
    reqeust.session.update({SESSION_USER_KEY: session_data})
    logging.info(f"session: {session_data}")
    return get_response_data(data=result, message="登录成功")

# 退出
@userRouter.post("/api/v1/user/logout",tags=[tagName],summary="退出",description="退出")
async def logout(request: Request):
    request.session.update({SESSION_USER_KEY: None})
    request.session.clear()
    return get_response_data()

# check login status
@userRouter.post("/api/v1/user/check_login",tags=[tagName],summary="检查登录状态",description="检查登录状态")
async def check_login(request: Request):
    result = await get_current_user(request)
    if result is None:
        return get_response_data(code=1, message="未登录")
    else:
        return get_response_data(data=result['user-session-key''']['user_name'])