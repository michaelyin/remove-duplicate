import redis

r = redis.StrictRedis(host='ubuntu202', port=6379, db=0)
print (r.execute_command('INFO')['redis_version'])

cnt = 0
for key in r.scan_iter():
    print key
    cnt = cnt + 1

print 'total key count: ', cnt
