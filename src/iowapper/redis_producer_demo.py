import time
import redis

# 实现一个生产者
rds = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)

def producer():
    for i in range(10):
        message_data = {
            'message': f'Hello, {i}',
            'timestamp': '2023-10-23 9:00:00'
        }
        rds.xadd("my_queue", message_data)
        print(f"发送数据 {message_data}")
        time.sleep(2)

if __name__ == "__main__":
    producer()
