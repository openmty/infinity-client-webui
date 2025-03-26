from infinity import InfinityConnection,connect,NetworkAddress

from global_utils import md5, singleton

class Client:
    def __init__(self, user_id:str,config_id:str, host:str, port:int, conn:InfinityConnection) -> None:
        self.user_id = user_id
        self.config_id = config_id
        self.host = host
        self.port = port
        self.key = md5(f"adi-{user_id}-{config_id}")
        self.conn = conn
    def close(self):
        if self.conn:
            self.conn.disconnect()

@singleton
class InfinityPool:
    def __init__(self) -> None:
        self.pool = {}
        self.max_length = 10000
    
    def add(self, user_id:str,config_id:str, host:str, port:int):
        if len(self.pool) >= self.max_length:
            return False, f'无法创建连接,已经超过系统最大连接数{self.max_length}'

        key = md5(f"adi-{user_id}-{config_id}")
        if hasattr(self.pool,key) and self.pool[key] is not None:
            self.pool[key].close()

        conn = connect(NetworkAddress(host, port)) 
        if conn is None:
            return False, f'无法创建连接{host}:{port}'
        client = Client(user_id=user_id,config_id=config_id, host=host,port=port, conn=conn)
        self.pool[client.key] = client
        return True, f'创建连接{host}:{port}成功'
    
    def delete(self,user_id:str,config_id:str):
        key = md5(f"adi-{user_id}-{config_id}")
        if self.pool[key] is not None:
            self.pool[key].close()
            del self.pool[key]
            return True, '删除Infinity连接成功'
        else:
            return False, 'Infinity连接不存在'

    def count(self):
        return len(self.pool)

    def get(self,user_id:str, config_id:str):
        key = md5(f"adi-{user_id}-{config_id}")
        if self.pool[key] is not None:
            return True, self.pool[key]
        else:
            return False, None

