# /usr/bin/python
# encoding=utf-8
import functools
import random
import time
import hashlib
import pickle
from typing import Dict
from framework.Error import RetryTimesError, RetryMaxTimesError
cache_map = {}  # 内存缓存

BASE_TYPE_LIST = (int, str, bool, tuple, float)


def retry(times: int = 10, interval: float = 2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(times):
                try:
                    ret = func(*args, **kwargs)
                except RetryTimesError as e:
                    if i < times:
                        time.sleep(interval)
                    else:
                        raise RetryMaxTimesError(times, func.__name__, str(e))
                except Exception as e:
                    raise
                else:
                    return ret
        return wrapper
    return decorator


def add_log(name: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import logging
            logger = logging.getLogger(name)
            logger.info('Async Function {}, {}, {}'.format(
                func.__name__, str(args), str(kwargs)))
            try:
                return func(*args, **kwargs)
            except Exception as e:
                import traceback
                logger.error(str(e), traceback.format_exc())
                raise
        return wrapper
    return decorator


def cache(duration: float = 3600):
    # duration < 0, 永不过期
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            args_list = []
            for arg in args:
                if type(arg) in BASE_TYPE_LIST:
                    args_list.append(arg)
                elif type(arg) in (dict, tuple, list):
                    args_list.append(hash(str(arg)))
                else:
                    args_list.append(hash(arg))
            key = compute_key(func, tuple(args_list), kwargs)
            # do we have it already ?
            if (key in cache_map and not is_obsolete(cache_map[key], duration)):
                return cache_map[key]['value']
            # computing
            result = func(*args, **kwargs)
            # storing the result
            cache_map[key] = {
                'value': result,
                'time': time.time()
            }
            return result
        return wrapper
    return decorator


def is_obsolete(entry, duration: float) -> bool:
    if duration < 0:
        return False
    return time.time() - entry['time'] > duration


def compute_key(func, args, kw) -> str:
    key = pickle.dumps((func.__name__, args, kw))
    return hashlib.sha1(key).hexdigest()
