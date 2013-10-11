__author__ = 'tarzan'

from redis import Redis

_fb1 = 3
_fb2 = 5
_default_limit = 5
_redis = None

def _fibo_timeout_calc(count):
    """
    Default timeout calculator for Counter class follow Fibonacy algorithm
    """
    if count == 1:
    	return _fb1
    if count == 2:
    	return _fb2
    i = 3
    fi, fi1 = _fb2, _fb2 + _fb1
    while i <= count:
    	fi, fi1 = fi1, fi + fi1
    	i += 1
    return fi


def initialize_from_settings(settings):
    """
    Initialize redis connector and other settings
    """
    global _redis
    global _fb0
    global _fb1
    global _default_limit
    _conf_prefix = 'antiflood.'

    conf = {k[len(_conf_prefix):]:v
                for k,v in settings.iteritems()
                if k.startswith(_conf_prefix)}
    _redis_prefix = 'redis.'
    redis_conf = {k[len(_redis_prefix):]:v
                  for k,v in conf.iteritems()
                  if k.startswith(_redis_prefix)}
    del _redis
    _redis = Redis(**redis_conf)
    _fb0 = settings.get('fb1', _fb1)
    _fb1 = settings.get('fb2', _fb2)
    _default_limit = settings.get('limit', _default_limit)

def includeme(config):
    initialize_from_settings(config.registry.settings)

from counter import Counter, LimitionReachedError