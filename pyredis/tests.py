import unittest
from pyredis.exceptions import RedisError
from pyredis.zset import ZSet
from pyredis.hash import Hash
from pyredis.set import Set
from pyredis.list import List


class ZSetTestCase(unittest.TestCase):
    def test_zadd(self):
        zset = ZSet()
        zset.zadd(a=5, b=3, c=1)
        self.assertEqual(zset._scores, [(1, 'c'), (3, 'b'), (5, 'a')])
        self.assertEqual(zset._members, [('a', 5), ('b', 3), ('c', 1)])

        zset.zadd(b=4)
        self.assertEqual(zset._scores, [(1, 'c'), (4, 'b'), (5, 'a')])
        self.assertEqual(zset._members, [('a', 5), ('b', 4), ('c', 1)])


    def test_zadd_adding_existing_member(self):
        zset = ZSet()
        zset.zadd(a=3)
        zset.zadd(a=4)
        self.assertEqual(zset._members, [('a', 4)])
        self.assertEqual(zset._scores, [(4, 'a')])

        zset.zadd(b=1)
        zset.zadd(b=2)
        self.assertEqual(zset._members, [('a', 4), ('b', 2)])
        self.assertEqual(zset._scores, [(2, 'b'), (4, 'a')])

    def test_zcard(self):
        zset = ZSet()
        zset.zadd(a=3, b=2, c=1)
        self.assertEqual(zset.zcard(), 3)

    def test_zcount(self):
        zset = ZSet()
        zset.zadd(a=1, b=2, c=2, d=2, e=3)
        self.assertEqual(zset.zcount(low=2, high=2), 3)

    def test_zincrby(self):
        zset = ZSet()
        zset.zadd(a=1, b=2, c=2, d=2, e=3)
        self.assertEqual(zset.zincrby('c', 3), 5)

    def test_zrange(self):
        zset = ZSet()
        zset.zadd(a=9, b=7, c=5, d=3, e=1)
        self.assertEqual(zset.zrange(1, 3), ['d', 'c', 'b'])

    def test_zrange_with_scores(self):
        zset = ZSet()
        zset.zadd(a=9, b=7, c=5, d=3, e=1)
        self.assertEqual(zset.zrange(1, 3, withscores=True), [('d', 3.0), ('c', 5.0), ('b', 7.0)])

    def test_zrange_with_scores_casted_to_int(self):
        zset = ZSet()
        zset.zadd(a=9, b=7, c=5, d=3, e=1)
        self.assertEqual(zset.zrange(1, 3, withscores=True, score_cast_func=int), [('d', 3), ('c', 5), ('b', 7)])

    def test_zrangebyscore(self):
        zset = ZSet()
        zset.zadd(a=9, b=7, c=5, d=3, e=1)
        self.assertEqual(zset.zrangebyscore(3, 8), ['d', 'c', 'b'])

    def test_zrangebyscore_with_scores(self):
        zset = ZSet()
        zset.zadd(a=9, b=7, c=5, d=3, e=1)
        self.assertEqual(zset.zrangebyscore(3, 8, withscores=True), [('d', 3.0), ('c', 5.0), ('b', 7.0)])

    def test_zrangebyscore_with_scores_casted_to_int(self):
        zset = ZSet()
        zset.zadd(a=9, b=7, c=5, d=3, e=1)
        self.assertEqual(zset.zrangebyscore(3, 8, withscores=True, score_cast_func=int), [('d', 3), ('c', 5), ('b', 7)])

    def test_zrank(self):
        zset = ZSet()
        zset.zadd(a=9, b=7, c=5, d=3, e=1)
        self.assertEqual(zset.zrank('a'), 4)
        self.assertEqual(zset.zrank('b'), 3)
        self.assertEqual(zset.zrank('c'), 2)
        self.assertEqual(zset.zrank('d'), 1)
        self.assertEqual(zset.zrank('e'), 0)

    def test_zrank_not_in_set(self):
        zset = ZSet()
        self.assertEqual(zset.zrank('a'), None)
        zset.zadd(a=9, b=7, c=5, d=3, e=1)
        self.assertEqual(zset.zrank('z'), None)

    def test_zrevrank(self):
        zset = ZSet()
        zset.zadd(a=9, b=7, c=5, d=3, e=1)
        self.assertEqual(zset.zrevrank('a'), 0)
        self.assertEqual(zset.zrevrank('b'), 1)
        self.assertEqual(zset.zrevrank('c'), 2)
        self.assertEqual(zset.zrevrank('d'), 3)
        self.assertEqual(zset.zrevrank('e'), 4)

    def test_zremrangebyrank(self):
        zset = ZSet()
        zset.zadd(a=9, b=7, c=5, d=3, e=1)
        self.assertEqual(zset.zremrangebyrank(3, 10), 2)
        self.assertEqual(zset._scores, [(1, 'e'), (3, 'd'), (5, 'c')])


class HashTestCase(unittest.TestCase):

    def test_hset(self):
        h = Hash()
        h.hset('a', 'aa')
        h.hset('b', 'bb')
        self.assertEqual(h._data, {'a': 'aa', 'b': 'bb'})

    def test_hget(self):
        h = Hash()
        h._data = {'a': 'aa', 'b': 'bb'}
        self.assertEqual(h.hget('a'), 'aa')
        self.assertEqual(h.hget('b'), 'bb')

    def test_hdel(self):
        h = Hash()
        h.hmset({'a': 'aa', 'b': 'bb', 'c': 'cc'})
        self.assertEqual(h._data, {'a': 'aa', 'b': 'bb', 'c': 'cc'})
        self.assertEqual(h.hdel('a', 'b'), 2)
        self.assertEqual(h._data, {'c': 'cc'})

    def test_hexists(self):
        h = Hash()
        h.hmset({'a': 'aa', 'b': 'bb', 'c': 'cc'})
        self.assertTrue(h.hexists('a'))
        self.assertFalse(h.hexists('z'))

    def test_hgetall(self):
        h = Hash()
        h.hmset({'a': 'aa', 'b': 'bb', 'c': 'cc'})
        self.assertEqual(h.hgetall(), {'a': 'aa', 'b': 'bb', 'c': 'cc'})

    def test_hincrby(self):
        h = Hash()
        h.hset('a', 1)
        self.assertEqual(h.hincrby('a', 2), 3)
        self.assertEqual(h.hincrby('b'), 1)
        self.assertEqual(h.hincrby('c', 2), 2)

    def test_hincrbyfloat(self):
        h = Hash()
        h.hset('a', 1.0)
        self.assertEqual(h.hincrby('a', 2.0), 3.0)
        self.assertEqual(h.hincrby('b'), 1.0)
        self.assertEqual(h.hincrby('c', 2.0), 2.0)

    def test_hkeys(self):
        h = Hash()
        h.hmset({'a': 'aa', 'b': 'bb', 'c': 'cc'})
        self.assertItemsEqual(h.hkeys(), ['a', 'b', 'c'])

    def test_hlen(self):
        h = Hash()
        h.hmset({'a': 'aa', 'b': 'bb', 'c': 'cc'})
        self.assertEqual(h.hlen(), 3)

    def test_setnx(self):
        h = Hash()
        self.assertEqual(h.hsetnx('a', 'aa'), 1)
        self.assertEqual(h.hget('a'), 'aa')
        self.assertEqual(h.hsetnx('a', 'zz'), 0)
        self.assertEqual(h.hget('a'), 'aa')
        self.assertEqual(h._data, {'a': 'aa'})

    def test_hmset(self):
        h = Hash()
        h.hmset({'a': 'aa', 'b': 'bb', 'c': 'cc'})
        self.assertEqual(h._data, {'a': 'aa', 'b': 'bb', 'c': 'cc'})
        h.hmset({'a': 'aaa', 'b': 'bbb', 'z': 'zz'})
        self.assertEqual(h._data, {'a': 'aaa', 'b': 'bbb', 'c': 'cc', 'z': 'zz'})

    def test_hmget(self):
        h = Hash()
        h.hmset({'a': 'aa', 'b': 'bb', 'c': 'cc'})
        self.assertEqual(h.hmget(['c', 'b']), ['cc', 'bb'])

    def test_hvals(self):
        h = Hash()
        h.hmset({'a': 'aa', 'b': 'bb', 'c': 'cc'})
        self.assertItemsEqual(h.hvals(), ['aa', 'bb', 'cc'])


class SetTestCase(unittest.TestCase):
    def test_sadd(self):
       s = Set()
       self.assertEqual(s.sadd('a', 'b'), 2)
       self.assertEqual(s.sadd('b', 'c'), 1)
       self.assertItemsEqual(s._set, set(['a', 'b', 'c']))

    def test_scard(self):
        s = Set()
        s.sadd('a', 'b', 'c')
        self.assertEqual(s.scard(), 3)

    def test_sismember(self):
        s = Set()
        s.sadd('a', 'b', 'c')
        self.assertTrue(s.sismember('a'))
        self.assertTrue(s.sismember('b'))
        self.assertTrue(s.sismember('c'))
        self.assertFalse(s.sismember('z'))

    def test_smembers(self):
        s = Set()
        s.sadd('a', 'b', 'c')
        self.assertItemsEqual(s.smembers(), ['a', 'b', 'c'])

    def test_spop(self):
        s = Set()
        s.sadd('a', 'b', 'c')
        removed = []
        for i in range(3):
            removed.append(s.spop())
        self.assertEqual(s.spop(), None)
        self.assertItemsEqual(removed, ['a', 'b', 'c'])

    def test_srandmember(self):
        """ Just sample 3 elements using srandmember and check to make sure
        they are in the original set.
        """
        s = Set()
        items = ['a', 'b', 'c']
        s.sadd(*items)
        for i in range(3):
            item = s.srandmember()
            self.assertTrue(item in items, item)
        items = s.srandmember(2)
        self.assertTrue(type(items), list)
        self.assertEqual(len(items), 2)

    def test_srem(self):
        s = Set()
        s.sadd('a', 'b', 'c')
        self.assertEqual(s.srem('b', 'c', 'z'), 2)
        self.assertItemsEqual(s._set, set(['a']))


class ListTestCase(unittest.TestCase):

    def test_lindex(self):
        l = List()
        l._list = ['a', 'b', 'c']
        self.assertEqual(l.lindex(0), 'a')
        self.assertEqual(l.lindex(1), 'b')
        self.assertEqual(l.lindex(2), 'c')
        self.assertEqual(l.lindex(3), None)

    def test_linsert(self):
        l = List()
        self.assertEqual(l.linsert('before', 'a', 'b'), -1)
        self.assertEqual(l.lpush('b'), 1)
        self.assertEqual(l.linsert('before', 'b', 'a'), 2)
        self.assertEqual(l.linsert('after', 'b', 'c'), 3)
        with self.assertRaises(RedisError):
            l.linsert('not allowed value', 'a', 'a')

    def test_llen(self):
        l = List()
        self.assertEqual(l.llen(), 0)
        self.assertEqual(l.lpush('a'), 1)
        self.assertEqual(l.llen(), 1)
        self.assertEqual(l.lpush('b'), 2)
        self.assertEqual(l.llen(), 2)
        self.assertEqual(l.lpush('c'), 3)
        self.assertEqual(l.llen(), 3)

    def test_lrange(self):
        l = List()
        l._list = ['a', 'b', 'c', 'd']
        self.assertEqual(l.lrange(1, -2), ['b', 'c'])

    def test_lpush(self):
        l = List()
        l.lpush('a')
        l.lpush('b')
        l.lpush('c')
        self.assertEqual(l._list, ['c', 'b', 'a'])

    def test_lpop(self):
        l = List()
        l._list = ['a', 'b', 'c']
        self.assertEqual(l.lpop(), 'a')
        self.assertEqual(l.lpop(), 'b')
        self.assertEqual(l.lpop(), 'c')
        self.assertEqual(l.lpop(), None)

    def test_lrem_gt_0(self):
        l = List()
        l._list = ['a', 'b', 'a', 'b', 'a', 'b']
        self.assertEqual(l.lrem(1, 'b'), 1)
        self.assertEqual(l._list, ['a', 'a', 'b', 'a', 'b'])

    def test_lrem_lt_0(self):
        l = List()
        l._list = ['a', 'b', 'a', 'b', 'a', 'b']

        self.assertEqual(l.lrem(-2, 'b'), 2)
        self.assertEqual(l._list, ['a', 'b', 'a', 'a'])

    def test_lrem_eq_0(self):
        l = List()
        l._list = ['a', 'b', 'a', 'b', 'a', 'b']
        self.assertEqual(l.lrem(0, 'a'), 3)
        self.assertEqual(l._list, ['b', 'b', 'b'])

    def test_lset(self):
        l = List()
        l.rpush('a')
        l.rpush('b')
        l.rpush('c')

        self.assertEqual(l.lindex(0), 'a')
        self.assertEqual(l.lindex(1), 'b')
        self.assertEqual(l.lindex(2), 'c')

        self.assertTrue(l.lset(0, 'aa'))
        self.assertTrue(l.lset(1, 'bb'))
        self.assertTrue(l.lset(2, 'cc'))

        self.assertEqual(l.lindex(0), 'aa')
        self.assertEqual(l.lindex(1), 'bb')
        self.assertEqual(l.lindex(2), 'cc')

        with self.assertRaises(RedisError):
            l.lset(100000, 'z')


    def test_ltrim(self):
        l = List()
        l._list = ['a', 'b', 'c', 'd']
        l.ltrim(1, -2)
        self.assertEqual(l._list, ['b', 'c'])

    def test_rpop(self):
        l = List()
        l._list = ['a', 'b', 'c']
        self.assertEqual(l.rpop(), 'c')
        self.assertEqual(l.rpop(), 'b')
        self.assertEqual(l.rpop(), 'a')
        self.assertEqual(l.rpop(), None)

    def test_rpush(self):
        l = List()
        l.rpush('a')
        l.rpush('b')
        l.rpush('c')
        self.assertEqual(l._list, ['a', 'b', 'c'])

if __name__ == '__main__':
    unittest.main()


