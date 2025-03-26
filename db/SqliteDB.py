from enum import auto
import logging
import re
from sqlite_utils import Database
from global_utils import singleton

# https://sqlite-utils.datasette.io/en/stable/python-api.html#

# 定义表结构
check = {
    "id": int,
    "name": str,
}

user = {
    "id": str,
    "name": str,
    "password": str,
    "create_time": int,
    "update_time": int,

}

infinity_config = {
    "id": str,
    "uid": str,
    "name": str,
    "host": str,
    "port": int,
    "create_time": int,
    "update_time": int,
}

@singleton
class SqliteDB:
    def __init__(self):
        logging.info("init BaseDataBase")
        # 连接到 SQLite 数据库
        self.db = Database("infinity_sqlite.db")
        # 创建表
        with self.db.conn:  # 使用连接对象的事务管理
            self.db["users"].create(columns=user, if_not_exists=True,pk="id")
            self.db["infinity_configs"].create(columns=infinity_config, if_not_exists=True,pk="id")
        logging.info('init database on cluster mode successfully')
        create_result,insert_result, count,drop_result = self.check()
        logging.info(f"create_result: {create_result},insert_result: {insert_result}, count: {count},drop_result: {drop_result}")

    
    def check(self):
        with self.db.conn:
            # 修改表结构，使id列自增长
            create_result = self.db["check"].create(
                columns=check, 
                if_not_exists=True,
                pk="id",  # 设置id为主键
                not_null={"id"},  # 确保id不能为null
                defaults={"id": None}  # 让SQLite自动生成id
            )
            logging.debug(f"create_check_result: {create_result}")
            insert_result = self.db["check"].insert({"name": "check name"})
            count = self.db["check"].execute_count()
            drop_result = self.db["check"].drop()
            logging.debug("drop check table")
            return create_result,insert_result, count,drop_result
    
    def close(self):
        self.db.close()
        logging.info("close database")




