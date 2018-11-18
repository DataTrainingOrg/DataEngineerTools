import redis

redis_client = redis.Redis(host='hostlocal')

redis_client.set("name", "your_name")