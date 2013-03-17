from .exceptions import RedisError


class List(object):

    def __init__(self):
        self._list = []

    def lindex(self, index):
        """
        Return the item from list at position ``index``

        Negative indexes are supported and will return an item at the
        end of the list
        """
        try:
            return self._list[index]
        except IndexError:
            return None

    def linsert(self, where, refvalue, value):
        """
        Insert ``value`` in list `either immediately before or after
        [``where``] ``refvalue``

        Returns the new length of the list on success or -1 if ``refvalue``
        is not in the list.
        """
        try:
            i = self._list.index(refvalue)
        except ValueError:
            return -1
        where = where.lower()
        if where == "before":
            self._list.insert(i, value)
        elif where == "after":
            self._list.insert(i + 1, value)
        else:
            raise RedisError("syntax error")
        return len(self._list)

    def llen(self):
        "Return the length of the list"
        return len(self._list)

    def lpop(self):
        "Remove and return the first item of the list"
        try:
            return self._list.pop(0)
        except IndexError:
            return None

    def lpush(self, *values):
        "Push ``values`` onto the head of the list"
        self._list = list(values) + self._list
        return self.llen()

    def lrange(self, start, end):
        """
        Return a slice of the list between position ``start`` and ``end``

        ``start`` and ``end`` can be negative numbers just like Python slicing
        notation
        """
        return self._list[start:end + 1]

    def lrem(self, count, value):
        """
        Remove the first ``count`` occurrences of elements equal to ``value``
        from the list.

        The count argument influences the operation in the following ways:
            count > 0: Remove elements equal to value moving from head to tail.
            count < 0: Remove elements equal to value moving from tail to head.
            count = 0: Remove all elements equal to value.
        """
        indexes = []
        l = len(self._list)
        limit = abs(count)
        if count < 0:
            for i, item in enumerate(reversed(self._list)):
                if item == value:
                    indexes.append(l - i - 1)
                    if count and len(indexes) == limit:
                        break
        else:
            for i, item in enumerate(self._list):
                if item == value:
                    indexes.append(i)
                    if len(indexes) == count:
                        break
        # If the count is less than 0, then use normal iterator because the
        # indexes are already reversed.
        iterator = indexes.__iter__() if count < 0 else reversed(indexes)
        # remove items using stored indexes in the reverse order so that
        # removing items doesn't mess with the index mapping
        for i in iterator:
            self._list.pop(i)
        return len(indexes)

    def lset(self, index, value):
        "Set ``position`` of list ``name`` to ``value``"
        try:
            self._list[index] = value
        except IndexError:
            raise RedisError('index out of range')
        return True

    def ltrim(self, start, end):
        """
        Trim the list, removing all values not within the slice
        between ``start`` and ``end``

        ``start`` and ``end`` can be negative numbers just like
        Python slicing notation
        """
        self._list = self._list[start:end + 1]

    def rpop(self):
        "Remove and return the last item of the list"
        try:
            return self._list.pop()
        except IndexError:
            return None

    def rpush(self, *values):
        "Push ``values`` onto the tail of the list ``name``"
        self._list =  self._list + list(values)
        return self.llen()
