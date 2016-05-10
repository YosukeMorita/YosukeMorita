# -*- coding: utf-8 -*-

from datetime import datetime
from functools import wraps

def logging(func):
    """A decorator that logs the activity of the script."""
    @wraps(func)
    def wrapper(obj, *args, **kwargs):
        print("{0:%Y-%m-%d %H:%M:%S} {1} {2} {3} args={4} kwargs={5}"\
                .format(datetime.now(), "INFO", func.__qualname__, "START", args, kwargs))
        result = func(obj, *args, **kwargs)
        print("{0:%Y-%m-%d %H:%M:%S} {1} {2} {3} return {4}"\
                .format(datetime.now(), "INFO", func.__qualname__, "END", result))
        return result
    return wrapper
