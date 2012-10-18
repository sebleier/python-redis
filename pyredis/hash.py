from collections import defaultdict


class Hash(object):

    def __init__(self):
        self._data = defaultdict(int)

    def hset(self, key, value):
        """
        Set ``key`` to ``value`` within hash ``name``
        Returns 1 if HSET created a new field, otherwise 0
        """
        if key in self._data:
            created = 0
        else:
            created = 1
        self._data[key] = value
        return created

    def hget(self, key):
        "Return the value of ``key``"
        return self._data.get(key, None)

    def hdel(self, *keys):
        "Delete ``keys``"
        deleted = 0
        for key in keys:
            if key in self._data:
                deleted += 1
                del self._data[key]
        return deleted

    def hexists(self, key):
        "Returns a boolean indicating if ``key`` exists within hash ``name``"
        return key in self._data

    def hgetall(self):
        "Return a Python dict of the hash's name/value pairs"
        return self._data

    def hincrby(self, key, amount=1):
        "Increment the value of ``key`` in hash by ``amount``"
        self._data[key] += amount
        return self._data[key]

    def hincrbyfloat(self, key, amount=1.0):
        """
        Increment the value of ``key`` in hash by floating ``amount``
        """
        return self.hincrby(key, amount)

    def hkeys(self):
        "Return the list of keys within hash"
        return self._data.keys()

    def hlen(self):
        "Return the number of elements in hash"
        return len(self._data)

    def hsetnx(self, key, value):
        """
        Set ``key`` to ``value`` within hash if ``key`` does not
        exist.  Returns 1 if HSETNX created a field, otherwise 0.
        """
        if key in self._data:
            return 0
        self._data[key] = value
        return 1

    def hmset(self, mapping):
        """
        Sets each key in the ``mapping`` dict to its corresponding value
        in the hash
        """
        return self._data.update(mapping)

    def hmget(self, keys):
        "Returns a list of values ordered identically to ``keys``"
        values = []
        for key in keys:
            values.append(self._data.get(key, None))
        return values

    def hvals(self):
        "Return the list of values within hash"
        return self._data.values()
