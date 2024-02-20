# -*- coding: utf-8 -*-
import redis    # 导入redis 模块
import time


pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
g_redis = redis.Redis(host='localhost', port=6379, decode_responses=True) 

def producer():
    for i in range(10):
        message_data = {
            'message': f'Hello, {i}',
            'timestamp': '2023-10-23 9:00:00'
        }
        g_redis.xadd("my_queue", message_data)
        print(f"发送数据 {message_data}")
        time.sleep(2)

# 创建一个订阅者
def sub():
    while True:
        messages = g_redis.xread({'my_queue': '0'}, block=0)  # Block until a new message arrives
        for stream, message_list in messages:
            for message_id, message_data in message_list:
                # Process the message
                print(f"Received message: {message_data}")
                # Acknowledge the message by removing it from the stream
                g_redis.xdel('my_queue', message_id)
