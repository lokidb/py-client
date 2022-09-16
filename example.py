from random import randrange

from lokidb_sdk import Client

c = Client(
    [
        ("127.0.0.1", 50051),
        ("127.0.0.1", 50052),
        ("127.0.0.1", 50053),
        ("127.0.0.1", 50054),
        ("127.0.0.1", 50055),
    ]
)

for _ in range(1000):
    key = f'{randrange(-99999999, 99999999)}'
    value = f'{randrange(-99999999, 99999999)}'*10

    c.set(key, value)
    print(c.get(key))

# Get all keys from all nodes
print(c.keys())

# Close connection to all nodes
c.close()
