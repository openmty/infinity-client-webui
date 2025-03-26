

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field
from service import userService, infinityConfigService
from apps import get_current_user
from apps import get_response_data
from apps import SESSION_USER_KEY



class InfinityConfigPayload(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="连接名称")
    host: str = Field(..., min_length=1, max_length=50, description="主机地址")
    port: int = Field(..., description="端口")

class InfinityConfigByIdPayload(BaseModel):
    id: str = Field(...,max_length=64, description="id")

infinityConfigRouter = APIRouter()
tagName = "Infinity Config"
pleaseLogin = "请先登录"

@infinityConfigRouter.post("/api/v1/infinity_config/create",tags=[tagName],summary="创建配置",description="创建配置")
async def create(reqeust: Request, payload: InfinityConfigPayload):
    user = await get_current_user(reqeust)
    if user is None:
        return get_response_data(code=1, message=pleaseLogin)
    user_id = user['user-session-key']['user_id']
    if infinityConfigService.is_name_exist(user_id, payload.host, payload.port):
        return get_response_data(code=1, message="主机地址和端口已存在")
    result = infinityConfigService.create_infinity_config(user_id, payload.name, payload.host, payload.port)
    return get_response_data(data=result, message="新增数据库配置成功")

# 查询
@infinityConfigRouter.post("/api/v1/infinity_config/list",tags=[tagName],summary="查询配置",description="查询配置")
async def list(reqeust: Request):
    user = await get_current_user(reqeust)
    if user is None:
        return get_response_data(code=1, message=pleaseLogin)
    user_id = user['user-session-key']['user_id']
    result = infinityConfigService.list_infinity_configs(user_id)

    return get_response_data(data=result)

# 删除
@infinityConfigRouter.post("/api/v1/infinity_config/delete",tags=[tagName],summary="删除配置",description="删除配置")
async def delete(reqeust: Request, payload: InfinityConfigByIdPayload):
    user = await get_current_user(reqeust)
    if user is None:
        return get_response_data(code=1, message=pleaseLogin)
    user_id = user['user-session-key']['user_id']
    result = infinityConfigService.delete_infinity_config(user_id, payload.id)
    return get_response_data(data=result, message="删除数据库配置成功")

 # get by id
@infinityConfigRouter.post("/api/v1/infinity_config/get",tags=[tagName],summary="获取配置",description="获取配置")
async def get(reqeust: Request, payload: InfinityConfigByIdPayload):
    user = await get_current_user(reqeust)
    if user is None:
        return get_response_data(code=1, message=pleaseLogin)
    user_id = user['user-session-key']['user_id']
    result = infinityConfigService.get_infinity_config(user_id, payload.id)
    return get_response_data(data=result)


# infinity 连接测试
@infinityConfigRouter.post("/api/v1/infinity_config/test",tags=[tagName],summary="测试连接",description="测试连接") 
async def test(reqeust: Request, payload: InfinityConfigPayload):
    user = await get_current_user(reqeust)
    if user is None:
        return get_response_data(code=1, message=pleaseLogin)
    import infinity
    message = '连接成功'
    code = 0
    infinity_object = None
    try:
        infinity_object = infinity.connect(infinity.NetworkAddress(payload.host, payload.port))
        result = infinity_object.list_databases()
        if result is None :
            message="连接失败"
            code = 1
    except Exception as e:
        message="连接失败"
        code = 1
    finally:
        if infinity_object:
            infinity_object.disconnect()
    return get_response_data(code=code, message=message)

    

