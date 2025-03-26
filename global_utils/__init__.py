import os
import uuid
import hashlib
# 定义全局的singleton注解
def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        key = str(cls) + str(os.getpid())
        if key not in instances:
            instances[key] = cls(*args, **kw)
        return instances[key]

    return _singleton


def get_uuid():
    return uuid.uuid1().hex

def md5(text):
    md5 = hashlib.md5()
    md5.update(text.encode('utf-8'))
    return md5.hexdigest()

