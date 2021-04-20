# import redis
# import json
#
# redis_conn = redis.Redis(host='localhost', port=6379, db=0, password='1234')
# a = int(input('A-ni daxil edin:'))
# b = int(input('B-ni daxil edin:'))
# d = {
#     'a': a,
#     'b': b,
#     'sum': "sum",
# }
#
# redis_conn.publish("broadcast", json.dumps(d))
