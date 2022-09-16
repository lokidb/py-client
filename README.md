# py-client
 LokiDB python client SDK

---

## Example
```python
from random import randrange

from lokidb_sdk import Client

c = Client(
    [
        ("localhost", 50051),
        ("localhost", 50052),
        ("localhost", 50053),
        ("localhost", 50054),
        ("localhost", 50055),
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

```

## API
| Method | Input                  | Output                   |
|--------|------------------------|--------------------------|
| Get    | key (str)              | value (str)              |
| Set    | key (str), value (str) |                          |
| Del    | key(str)               |                          |
| Keys   |                        | list of keys (list[str]) |
| Flush  |                        |                          |