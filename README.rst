ZSet Datastructure
==================

ZSets are a Python datastructure for sorted sets, similar to `Redis`_ sorted
sets and inspired by `Redis-py`_'s api

Optionally you can use `blist`_ for better perfomance.

Why did I build this, you say? Well..ummm...I dunno.  'Cause I could and it
was fun...and stuff?

.. _Redis: https://github.com/antirez/redis
.. _Redis-py: https://github.com/andymccurdy/redis-py
.. _blist: http://pypi.python.org/pypi/blist/

Examples::

    >>> zset = ZSet()
    >>> zset.zadd(a=9, b=7, c=5, d=3, e=1)
    >>> print zset.zrange(1, 3, withscores=True, score_cast_func=int)
    [('d', 3), ('c', 5), ('b', 7)])