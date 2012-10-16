from operator import xor
import sys
import bisect

try:
    from blist import blist
    USE_BLIST = True
except ImportError:
    USE_BLIST = False


EPSILON = sys.float_info.epsilon * 4


class ZSet(object):

    def __init__(self):
        if USE_BLIST:
            self._scores = blist([])
            self._members = blist([])
        else:
            self._scores = []
            self._members = []

    def __add(self, member, score):
        """ Private method to add the member and score to the sorted set.
        This trusts that the member does not already exist in the sorted set.

        """
        bisect.insort_left(self._members, (member, score))
        bisect.insort_left(self._scores, (score, member))

    def _insert_or_update(self, member, score):
        """ Takes a member and score and inserts them into the sorted set. If
        the member already exists, it is just updated.
        """
        # Find the index of the member if it exists in the sorted set
        i = self._find_member(member)
        if i is None:
            self.__add(member, score)
        else:
            s = self._members[i][1]
            self._members[i] = (member, score)
            j = self._find_score(s)
            _, member = self._scores.pop(j)
            bisect.insort_left(self._scores, (score, member))

    def zadd(self, **kwargs):
        """
        Adds score, member to the sorted set if member doesn't exist or
        updates score if the member already exists.
        """
        for member, score in kwargs.iteritems():
            i = bisect.bisect_left(self._members, (member, None))
            cardnality = self.zcard()
            if cardnality == 0:
                self._scores.append((score, member))
                self._members.append((member, score))
            else:
                self._insert_or_update(member, score)

    def _find_member(self, member):
        """ Finds the position of the member in the sorted set.

        Returns None if not found.
        """
        cardnality = self.zcard()
        if cardnality == 0:
            return None
        if self._members[0][0] == member:
            return 0
        if self._members[-1][0] == member:
            return cardnality - 1
        i = bisect.bisect_left(self._members, (member, None))
        if i >= cardnality - 1:
            return None
        if self._members[i][0] == member:
            return i
        return None

    def _find_score(self, score, desc=False):
        """ Find the position of the score in the sorted set.

        Optionally, specify ``desc`` as True to search in the reverse order
        Returns None if ``score`` is not found.
        """
        cardnality = self.zcard()
        scores = self._scores
        if cardnality == 0:
            return None

        if desc:
            if scores[-1][0] == score:
                return 0
            if scores[0][0] == score:
                return cardnality - 1
            i = bisect.bisect_right(scores, (score + EPSILON, None))
            if i >= cardnality:
                return None
            if scores[i - 1][0] == score:
                return cardnality - i
        else:
            if scores[0][0] == score:
                return 0
            if scores[-1][0] == score:
                return cardnality - 1
            i = bisect.bisect_left(scores, (score, None))
            if i >= cardnality - 1:
                return None
            if scores[i][0] == score:
                return i
        return None

    def zrank(self, member):
        """ Finds the 0-based index of ``member``

        Returns None if member is not in the sorted set.
        """
        i = self._find_member(member)
        if i is None:
            return None
        return self._find_score(self._members[i][1])

    def zrevrank(self, member):
        """ Finds the 0-based index of ``member`` in the reverse order.

        Returns None if member is not in the sorted set.
        """
        i = self._find_member(member)
        if i is None:
            return None
        return self._find_score(self._members[i][1], desc=True)

    def zcard(self):
        """ Returns the cardnality of the sorted set.
        """
        return len(self._scores)

    def zcount(self, low, high):
        """ Returns the number of elements in the sorted set between ``low``
        and ``high``.  The count should be inclusive.

        """
        right = bisect.bisect_right(self._scores, (high + EPSILON, None))
        left = bisect.bisect_left(self._scores, (low, None))
        return right - left

    def zincrby(self, member, amount=1):
        """ Finds member in the sorted set and increments its score.

        If no member is found, then member is insert and given a score of
        ``amount``.
        """
        i = bisect.bisect_left(self._members, (member, None))
        try:
            # Check if the next member is the same.  If it is, then update the score
            if self._members[i][0] == member:
                j = self._scores.index((self._members[i][1], self._members[i][0]))
                new_score = self._members[i][1] + amount
                self._scores[j] = (new_score, member)
                self._members[i] = (member, new_score)
            elif self._members[i + 1][0] == member:
                j = self._scores.index((self._members[i + 1][1], self._members[i + 1][0]))
                new_score = self._members[i][1] + amount
                self._scores[j] = (new_score, member)
                self._members[i + 1] = (member, new_score)
            else:
                new_score = amount
                self._members.insert(i, (member, amount))
                bisect.insort_left(self._scores, (amount, member))
        except IndexError:
            new_score = amount
            self._members.insert(i, (member, amount))
            bisect.insort_left(self._scores, (amount, member))
        return new_score


    def _zrange(self, start, end, desc=False, withscores=False, score_cast_func=float):
        """ Finds members that fall in the 0-index range of ``start`` and
        ``end``.

        If ``desc`` is True, the range will be taken from the reverse order.

        Optionally, you can provide ``withscores`` as True to include the score
        values along with the members.

        Also, you can provide ``score_cast_func`` to cast the scores to a
        particular type.
        """
        if desc:
            scores = reversed(self._scores)
        else:
            scores = self._scores

        if withscores:
            data = [(member, score_cast_func(score)) for (score, member) in scores[start:end+1]]
        else:
            data = [member for score, member in scores[start:end+1]]

        return data

    def zrange(self, start, end, desc=False, withscores=False, score_cast_func=float):
        """ Finds members that fall in the 0-index range of ``start`` and
        ``end``.

        Optionally, you can provide ``withscores`` as True to include the
        score values along with the members.

        Also, you can provide ``score_cast_func`` to cast the scores to a
        particular type.
        """
        if desc:
            return self._zrange(start, end, desc=True, withscores=withscores, score_cast_func=score_cast_func)
        return self._zrange(start, end, desc=False, withscores=withscores, score_cast_func=score_cast_func)

    def zrevrange(self, start, end, withscores=False, score_cast_func=float):
        """ Finds members that fall in the 0-index range of ``start`` and
        ``end``, but in the reverse order.

        Optionally, you can provide ``withscores`` as True to include the score
        values along with the members.

        Also, you can provide ``score_cast_func`` to cast the scores to a
        particular type.
        """
        return self._zrange(start, end, desc=True, withscores=withscores, score_cast_func=score_cast_func)

    def _zrangebyscore(self, min, max, start=None, num=None, withscores=False, score_cast_func=float, desc=False):
        """ Returns members that fall the score range of ``min`` and ``max``.

        If ``desc`` is True, the range will be taken from the reverse order.

        Optionally, you can provide ``withscores`` as True to include the score
        values along with the members.

        Also, you can provide ``score_cast_func`` to cast the scores to a
        particular type.
        """
        cardnality = self.zcard()

        if cardnality == 0:
            return []

        left = bisect.bisect_left(self._scores, (min, None))

        right = bisect.bisect_right(self._scores, (max + EPSILON, None))

        if withscores:
            data = [(member, score_cast_func(score)) for (score, member) in self._scores[left:right]]
        else:
            data = [member for (score, member) in self._scores[left:right]]

        if desc:
            data.reverse()

        if xor(start is None, num is None):
            raise Exception("``start`` and ``num`` must both be specified")
        elif start is not None:
            data = data[start:start + num]

        return data

    def zrangebyscore(self, *args, **kwargs):
        """ Returns members that fall the score range of ``min`` and ``max``.

        Optionally, you can provide ``withscores`` as True to include the score
        values along with the members.

        Also, you can provide ``score_cast_func`` to cast the scores to a
        particular type.
        """
        kwargs['desc'] = False
        return self._zrangebyscore(*args, **kwargs)

    def zrevrangebyscore(self, *args, **kwargs):
        """ Returns members that fall the score range of ``min`` and ``max``.

        Optionally, you can provide ``withscores`` as True to include the score
        values along with the members.

        Also, you can provide ``score_cast_func`` to cast the scores to a
        particular type.
        """
        kwargs['desc'] = True
        return self._zrangebyscore(*args, **kwargs)

    def zscore(self, value):
        """ Returns the member of the sorted set with a score of ``value``.

        If ``value`` does not exist in the sorted set, None is returned.
        """
        i = self._find_score(value)
        if i is None:
            return None
        return self._scores[i][1]

    def zremrangebyrank(self, min, max):
        """ Removes members by between the 0-indexed values of ``min`` and
        ``max`` and returns the number removed.
        """
        subset = self._scores[min:max + 1]
        del self._scores[min:max + 1]
        for (score, member) in subset:
            i = self._find_member(member)
            del self._members[i]
        return len(subset)

    def zremrangebyscore(self, min, max):
        """ Removes members by between the score values of ``min`` and
        ``max`` and returns the number removed.
        """
        left = bisect.bisect_left(self._scores, (min, None))
        right = bisect.bisect_right(self._scores, (max + EPSILON, None))
        subset = self._scores[left:right+1]
        del self._scores[left:right+1]
        for (score, member) in subset:
            i = self._find_member(member)
            del self._members[i]
        return len(subset)
