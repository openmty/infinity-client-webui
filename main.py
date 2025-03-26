import logging
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import signal
import sys,os
from config import infinity_url,infinity_port
import infinity
import logger
from pydantic import BaseModel, Field
from db import sqlite_db
from starlette_session import SessionMiddleware
from apps.UserApi import userRouter
from apps.InfinityConfigApi import infinityConfigRouter
from apps.DBManagerApi import dbMRouter
import db

app = FastAPI()



# 添加跨域中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)

from starlette_session import SessionMiddleware
app.add_middleware(
    SessionMiddleware,
    secret_key="ADI-INFINITYDB-XHHFJG8e7DJD8-secret-KEY",
    same_site="lax",
    max_age=3600,
    cookie_name="adi-infinitydb-session"
)

# 创建一个Infinity对象
infinity_object = None


def shutdown_handler(signum, frame):
    logging.info("\nShutting down gracefully...")
    # 在这里可以添加其他清理逻辑
    sqlite_db.close()
    if infinity_object:
        logging.info("Disconnecting from Infinity...")
        infinity_object.disconnect()
    logging.info("sys exit")
    sys.exit(0)

# @app.get("/")
# async def root():
#     return {"message": "Infinity Client Server."}



app.include_router(userRouter)
app.include_router(infinityConfigRouter)
app.include_router(dbMRouter)

def main():
    # 注册信号处理
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)


    # 挂载静态文件目录
    web = os.path.join('web','dist')
    # print('web------:',web)
    app.mount("/", StaticFiles(directory=web, html=True), name="web")
    
    # print("Hello from infinity-client!")
    # print('infinity_object:', infinity_object)
    uvicorn.run(app, host="0.0.0.0", port=8000)



if __name__ == "__main__":
    main()
