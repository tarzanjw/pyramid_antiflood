A AntiFlood package for Pyramid
===============================

This package help to prevent user from performing an action many times on an item for
a time period. Each time the action occured, the counter will increase by 1. There're a
limited value for each action, so a LimitionReachedError will be raised if this
value is reached.

This package use Redis as storage to store counter values.

Usage
-----

```python
import pyramid_antiflood

antiflood = pyramid_antiflood(action_id, item_id)

try:
    antiflood.verify()

    action_occured = is_action_occured()

    if action_occured:
        antiflood.increase()
    else:
        antiflood.clear()

except pyramid_antiflood.LimitionReachedError, e:
    # TODO process on limition is reached
    print e
    pass
```

Configuration
-------------

Updating ...