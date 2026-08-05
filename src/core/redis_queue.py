import json
import os
import redis

class RedisOrderQueue:
    """Enterprise In-Memory Redis Order Queue & Decoupled Signal Bus"""
    def __init__(self):
        self.host = os.environ.get("REDIS_HOST", "localhost")
        self.port = int(os.environ.get("REDIS_PORT", 6379))
        self.password = os.environ.get("REDIS_PASSWORD", None)
        
        try:
            self.client = redis.Redis(
                host=self.host,
                port=self.port,
                password=self.password,
                decode_responses=True,
                socket_timeout=3
            )
            self.client.ping()
            self.active = True
            print("⚡ [REDIS QUEUE] High-Speed In-Memory Bus Connected!")
        except Exception as e:
            print(f"⚠️ [REDIS WARNING] Connection failed ({e}). Falling back to In-Memory Local Bus.")
            self.active = False
            self.local_queue = []

    def push_order(self, order_data):
        """Push Order Signal to Queue (Producer)"""
        payload = json.dumps(order_data)
        if self.active:
            self.client.rpush("quantum_order_queue", payload)
            print(f"📥 [REDIS QUEUE] Pushed Order: {order_data['type']} {order_data['symbol']}")
        else:
            self.local_queue.append(order_data)

    def pop_order(self, timeout=1):
        """Pop Next Order Signal for Execution (Consumer)"""
        if self.active:
            result = self.client.blpop("quantum_order_queue", timeout=timeout)
            if result:
                return json.loads(result[1])
        else:
            if self.local_queue:
                return self.local_queue.pop(0)
        return None

redis_queue = RedisOrderQueue()
