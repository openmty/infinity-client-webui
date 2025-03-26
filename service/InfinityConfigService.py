
from global_utils import singleton
import time
import global_utils
from db import sqlite_db


@singleton
class InfinityConfigService:
    def __init__(self):
        self.db = sqlite_db.db
        self.table_name = 'infinity_configs'

    def create_infinity_config(self, uid:str, name:str, host:str, port:int):
        if self.db.conn is not None:
            with self.db.conn:
                infinity_config_data = {}
                current_time = int(time.time())
                infinity_config_data["create_time"] = current_time
                infinity_config_data["update_time"] = current_time
                infinity_config_data["id"] = global_utils.get_uuid()
                infinity_config_data["uid"] = uid
                infinity_config_data["name"] = name
                infinity_config_data["host"] = host
                infinity_config_data["port"] = port
                self.db[self.table_name].insert(infinity_config_data)
                return infinity_config_data
        else:
            return None

    def get_infinity_config_by_id(self, infinity_config_id):
        # 从数据库中获取用户信息
        infinity_config_data = self.db[self.table_name].execute("SELECT * FROM infinity_configs WHERE id =?", (infinity_config_id,)).fetchone()
        return self.to_dict(infinity_config_data)

    def get_infinity_config_by_uid(self, uid):
        # 从数据库中获取用户信息
        infinity_configs_data = self.db[self.table_name].execute("SELECT * FROM infinity_configs WHERE uid =?", (uid,))
        return self.to_dicts(infinity_configs_data)

    def update_infinity_config(self, infinity_config_id):
        new_data = int(time.time())
        # 更新用户信息
        with self.db.conn:
            return self.db[self.table_name].update(new_data, where="id =?", args=(infinity_config_id,))

    def delete_infinity_config(self, user_id,infinity_config_id):
        # 删除用户信息
        with self.db.conn:
            cursor = self.db.execute(f"DELETE FROM {self.table_name} WHERE uid =? and id =?", (user_id,infinity_config_id))
            return cursor.rowcount > 0  # 返回是否成功删除

    def list_infinity_configs(self,user_id:str):
        # 获取所有用户列表
        infinity_configs = self.db.execute(f"SELECT * FROM {self.table_name} WHERE uid =? order by update_time desc", (user_id,)).fetchall()
        return self.to_dicts(infinity_configs)

    # 判断是否重名
    def is_name_exist(self, user_id, host,prot):
        infinity_config_data = self.db.execute(f"SELECT * FROM {self.table_name} WHERE uid =? and host =? and port =?", (user_id,host,prot)).fetchone()
        if infinity_config_data is not None and len(infinity_config_data) > 0:
            return True
        else:
            return False


    def to_dict(self, row):
        if row is None or len(row) == 0:
            return None
        return {
            "id": row[0],
            "uid": '',
            "name": row[2],
            "host": row[3],
            "port": row[4],
            "create_time": row[5],
            "update_time": row[6],
        }
    
    def to_dicts(self, rows):
        if rows is None or len(rows) == 0:
            return []
        return [self.to_dict([row[0], '', *row[2:]]) for row in rows]

