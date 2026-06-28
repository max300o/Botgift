import time


class Cache:

    def __init__(self, ttl=60):
        self.ttl = ttl
        self.data = {}

    def get(self, key):
        item = self.data.get(key)

        if not item:
            return None

        value, expire = item

        if expire < time.time():
            del self.data[key]
            return None

        return value

    def set(self, key, value):
        self.data[key] = (
            value,
            time.time() + self.ttl
        )

    def delete(self, key):
        self.data.pop(key, None)

    def clear(self):
        self.data.clear()


cache = Cache()
