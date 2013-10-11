__author__ = 'tarzan'

import pyramid_antiflood


class LimitionReachedError(BaseException):
    action_id = None
    item_id = None
    value = None
    limit = None

    def __init__(self, counter):
        self.action_id = counter.action_id
        self.item_id = counter.item_id
        self.value = counter.value
        self.limit_value = counter.limit_value
        self.timeout = counter.timeout

    def __str__(self):
        return 'You did action "%s" on item %s many times (%d/%d). Try again after %d second(s)' \
               % (self.action_id, self.item_id, self.value, self.limit_value, self.timeout)

class Counter(object):
    """
    This class use to count the occurred times for a action on an item
    """
    def __init__(self, action_id, item_id, limit=None):
        if limit is None:
            limit = pyramid_antiflood._default_limit
        self.action_id = action_id
        self.item_id = item_id
        self.limit_value = limit


    @property
    def redis_key(self):
        return '%s#%s' % (self.action_id, self.item_id)

    @property
    def _redis(self):
        return pyramid_antiflood._redis

    def increase(self, amount=1, timeout=None, timeout_calc=None):
        """
        Increase the number of occurring for an action, return new
        value

        :param timeout_calc timeout calculator based on count. Its default
        value is fibonacci algorithm. If you pass an integer value, it will
        be "{value}*{counter}", you can pass a callable object with prototype
        like calculator_func(count)

        :return new value, the value after increasing
        """
        count = int(self._redis.incr(self.redis_key, amount))
        if timeout_calc is None:
            timeout_calc = pyramid_antiflood._fibo_timeout_calc
        if timeout is None:
            try:
                timeout = count*int(timeout_calc)
            except (TypeError, ValueError):
                timeout = timeout_calc(count)
        self._redis.expire(self.redis_key, timeout)
        return count

    @property
    def value(self):
        """
        Get current value of current item on current action
        """
        value = self._redis.get(self.redis_key)
        if not value:
            return 0
        return int(value)

    def __nonzero__(self):
        return self.is_ok()

    def is_ok(self, limit=None):
        if limit is None:
            limit = self.limit_value
        return self.value <= limit

    def verify(self):
        if not self:
            raise LimitionReachedError(self)
        return True

    def clear(self):
        self._redis.delete(self.redis_key)

    @property
    def timeout(self):
        ttl = self._redis.ttl(self.redis_key)
        if not ttl:
            return 0
        return ttl
