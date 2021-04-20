import redis
import json

redis_conn = redis.Redis(host='localhost', port=6379, db=0, password='1234')


def handler(message):
    if message.get("type") == "message":
        json_data = message.get("data")
        data = json.loads(json_data)
        a = data['a']
        b = data['b']
        operation = data['sum']
        if operation == 'sum':
            print(a + b)


p = redis_conn.pubsub()
p.subscribe(**{'broadcast': handler})
thread = p.run_in_thread()

pubsub = redis_conn.pubsub()
pubsub.subscribe("broadcast")

# for message in pubsub.listen():
#     if message.get("type") == "message":
#         json_data = message.get("data")
#         data = json.loads(json_data)
#         a = data['a']
#         b = data['b']
#         operation = data['sum']
#         if operation == 'sum':
#             print(a + b)
