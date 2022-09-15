# py-client
 LokiDB python client lib

---

## Example
```python
from lokidb_sdk import Client

c = Client(("localhost", 50051), 10)

c.set("e", "E")

print(c.get("e"))

print(c.keys())

c.delete("e")

c.flush()

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