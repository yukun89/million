import time
import redis

rds = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)


# 创建一个订阅者
def sub():
    while True:
        messages = rds.xread({'my_queue': '0'}, block=0)  # Block until a new message arrives
        for stream, message_list in messages:
            for message_id, message_data in message_list:
                # Process the message
                print(f"Received message: {message_data}")
                # Acknowledge the message by removing it from the stream
                rds.xdel('my_queue', message_id)


if __name__ == "__main__":
    sub()
