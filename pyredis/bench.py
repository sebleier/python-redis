from redis import Redis
from zset import ZSet
import time
import random
import os
import gc

def mem(size="rss"):
    """Generalization; memory sizes: rss, rsz, vsz."""
    return int(os.popen('ps -p %d -o %s | tail -1' % (os.getpid(), size)).read())

# initialize
r = Redis(unix_socket_path='/tmp/redis.sock')
start_memory = mem()
# get dataset
values = []
for i in range(100000):
    values.append((str(i), random.randint(0, 9999999)))

# reset
r.flushdb()

# Measure Redis
start = time.time()
for member, score in values:
    r.zadd('aaaaa', **{member: score})
end = time.time()
print end - start
after_redis_memory = mem() - start_memory

print "Memory after Redis: %s" % after_redis_memory

# Measure Zset
zset = ZSet()
start = time.time()
for member, score in values:
    zset.zadd(**{member: score})
end = time.time()
print end - start
after_zset_memory = mem() - after_redis_memory
print "Memory after ZSet: %s" % after_zset_memory

