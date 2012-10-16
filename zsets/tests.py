import unittest
from zsets.zset import ZSet

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

if __name__ == '__main__':
    unittest.main()


