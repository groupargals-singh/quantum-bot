import time
from src.core.redis_queue import RedisOrderQueue

print("🚀 --- TESTING REDIS ORDER QUEUE ARCHITECTURE --- 🚀\n")

queue = RedisOrderQueue()

# Sample Trade Order Payload
sample_order = {
    "symbol": "BTCUSDT",
    "side": "BUY",
    "type": "MARKET",
    "quantity": 0.005,
    "price": 65000.0,
    "timestamp": time.time()
}

# 1. Push Order Signal
print("\n1️⃣ Pushing Order Signal to Queue...")
queue.push_order(sample_order)

# 2. Pop & Process Order Signal
print("\n2️⃣ Fetching Order Signal from Queue...")
received_order = queue.pop_order()

if received_order:
    print(f"✅ Success! Received Order: {received_order['side']} {received_order['quantity']} {received_order['symbol']} @ ${received_order['price']}")
else:
    print("❌ Error: Queue is empty!")

print("\n🎉 Redis Order Queue system test finished successfully!")
