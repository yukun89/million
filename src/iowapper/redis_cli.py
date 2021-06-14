# -*- coding: utf-8 -*-
import redis    # 导入redis 模块

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
g_redis = redis.Redis(host='localhost', port=6379, decode_responses=True) 


