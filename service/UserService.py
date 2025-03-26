
import logging
import re
from global_utils import singleton
import time
import global_utils
from db import sqlite_db


@singleton
class UserService:
    def __init__(self):
        self.db = sqlite_db.db
        self.table_name = 'users'

    def get_user_by_id(self, user_id):
        # 从数据库中获取用户信息
        user_data = self.db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return self.to_dict(user_data)

    def get_user_by_name_and_password(self, name,password):
        # 从数据库中获取用户信息
        user_data = self.db.execute("SELECT * FROM users WHERE name =? and password =?", (name,global_utils.md5(password))).fetchone()
        return self.to_dict(user_data)


    def update_user(self, user_id, new_data):
        # 更新用户信息
        result = self.db.update(new_data, where="id = ?", args=(user_id,))
        return result

    def delete_user(self, user_id):
        # 删除用户信息
        self.db.delete(where="id = ?", args=(user_id,))

    def list_users(self):
        # 获取所有用户列表
        users = self.db.select()
        return self.to_dicts(users)

    def create_user(self, name, password):
        with self.db.conn:
            user_data = {}
            current_time = int(time.time())
            user_data["create_time"] = current_time
            user_data["update_time"] = current_time
            user_data["id"] = global_utils.get_uuid()
            user_data["name"] = name
            user_data["password"] = global_utils.md5(password)
            self.db[self.table_name].insert(user_data)
            user_data['password'] = ''
            user_data['id'] = ''
            return user_data

    # 判断是否重名
    def is_name_exist(self, name):
        user_data = self.db.execute("SELECT * FROM users WHERE name =?", (name,)).fetchone()
        if user_data is not None and len(user_data) > 0:
            return True
        else:
            return False

    def to_dict(self, user_data):
        if user_data is None or len(user_data) == 0:
            return None
        return {
            "id": user_data[0],
            "name": user_data[1],
            "password": user_data[2],
            "create_time": user_data[3],
            "update_time": user_data[4]
        }
    def to_dicts(self, user_data_list):
        if user_data_list is None or len(user_data_list) == 0:
            return None
        result = [] 
        for user_data in user_data_list:
            result.append(self.to_dict(user_data))
        return result