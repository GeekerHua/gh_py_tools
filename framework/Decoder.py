# /usr/bin/python
# encoding=utf-8
import functools
import random
import time
from framework.Error import RetryTimesError, RetryMaxTimesError

def retry(times=10, interval=2):
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


def add_log(name):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import logging
            logger = logging.getLogger(name)
            logger.info('Async Function {}, {}, {}'.format(func.__name__, str(args), str(kwargs)))
            try:
                return func(*args, **kwargs)
            except Exception as e:
                import traceback
                logger.error(str(e), traceback.format_exc())
                raise
        return wrapper
    return decorator


@add_log('execute')
def now():
    print('2013-12-25')

if __name__ == "__main__":
    now()