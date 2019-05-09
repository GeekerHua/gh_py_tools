# /usr/bin/python
# encoding=utf-8


class BaseError(Exception):
    message = None

    def __init__(self, *xargs, **kwargs):
        super(BaseError, self).__init__(self.message, *xargs, **kwargs)


class RetryTimesError(BaseError):
    message = '单次重试失败'


class RetryMaxTimesError(BaseError):
    message = '超过最大重试次数!!!'

    def __init__(self, max_times: int, func_name: str, error_message: str):
        self.message = 'Try {} times {} but {}'.format(
            max_times, func_name, error_message)
        super(RetryMaxTimesError, self).__init__(self.message)
