import random


class Set(object):

    def __init__(self, *values):
        self._set = set()
        self.sadd(*values)

    def __and__(self, rhs):
        return self._set & rhs._set

    def __or__(self, rhs):
        return self._set | rhs._set

    def sadd(self, *values):
        "Add ``value(s)`` to set"
        new = set(values) - self._set
        self._set.update(new)
        return len(new)

    def scard(self):
        "Return the number of elements in set"
        return len(self._set)

    def sismember(self, value):
        "Return a boolean indicating if ``value`` is a member of set"
        return value in self._set

    def smembers(self):
        "Return all members of the set"
        return list(self._set)

    def spop(self):
        "Remove and return a random member of set"
        try:
            return self._set.pop()
        except KeyError:
            return None

    def srandmember(self, number=1):
        """
        If ``number`` is None, returns a random member of set.

        If ``number`` is supplied, returns a list of ``number`` random
        memebers of set.
        """
        items = random.sample(self._set, number)
        if len(items) == 1:
            return items[0]
        return items

    def srem(self, *values):
        "Remove ``values`` from set"
        values = set(values)
        values = self._set & values
        for value in values:
            self._set.remove(value)
        return len(values)
