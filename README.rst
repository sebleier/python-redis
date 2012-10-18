============
Python Redis
============

An in-process implementation of redis written in Python

Datastructures
==============

ZSet Datastructure
~~~~~~~~~~~~~~~~~~

ZSets are a Python datastructure for sorted sets, similar to `Redis`_ sorted
sets and inspired by `Redis-py`_'s api

Optionally you can use `blist`_ for better perfomance.

Examples::

    >>> zset = ZSet()
    >>> zset.zadd(a=9, b=7, c=5, d=3, e=1)
    >>> print zset.zrange(1, 3, withscores=True, score_cast_func=int)
    [('d', 3), ('c', 5), ('b', 7)])


Hash Datastructure
~~~~~~~~~~~~~~~~~~

Hash datastructures are basically python dictionaries with the redis api

Examples::

    >>> h = Hash()
    >>> h.hmset({'a': 'aa', 'b': 'bb', 'c': 'cc'})
    >>> hmget(['c', 'b'])
    ['cc', 'bb']

.. _Redis: https://github.com/antirez/redis
.. _Redis-py: https://github.com/andymccurdy/redis-py
.. _blist: http://pypi.python.org/pypi/blist/