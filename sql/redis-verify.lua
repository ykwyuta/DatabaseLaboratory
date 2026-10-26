-- All keys use a fresh UUID. Remove them even if an assertion fails.
local ok, err = pcall(function()
  redis.call('SET', KEYS[1], '9007199254740993', 'EX', 60)
  assert(redis.call('GET', KEYS[1]) == '9007199254740993')
  assert(redis.call('TTL', KEYS[1]) > 0)
  redis.call('HSET', KEYS[2], 'name', '東京')
  assert(redis.call('HGET', KEYS[2], 'name') == '東京')
  redis.call('RPUSH', KEYS[3], 'a', 'b')
  assert(redis.call('LLEN', KEYS[3]) == 2)
  redis.call('SADD', KEYS[4], 'a', 'a', 'b')
  assert(redis.call('SCARD', KEYS[4]) == 2)
  redis.call('ZADD', KEYS[5], 1, 'a', 2, 'b')
  assert(redis.call('ZRANK', KEYS[5], 'b') == 1)
end)
redis.call('DEL', unpack(KEYS))
if not ok then return redis.error_reply(tostring(err)) end
return 'rava-redis-ok'
