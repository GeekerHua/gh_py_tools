import unittest
from framework.Decoder import retry, RetryTimesError, RetryMaxTimesError, cache


class DecoderTest(unittest.TestCase):
    @retry(3)
    def retry_max_test(self):
        raise RetryTimesError()

    @retry(2)
    def retry_error_test(self):
        raise Exception('error')

    def test_retry(self):
        try:
            self.retry_max_test()
        except Exception as e:
            self.assertIsInstance(
                e, RetryMaxTimesError, 'not mac retry times')

        try:
            self.retry_error_test()
        except Exception as e:
            self.assertNotIsInstance(
                e, RetryMaxTimesError, 'not error Exception')
            self.assertEqual(str(e), 'error', 'not error str')

    @cache()
    def in_cache(self, data, data2):
        return data + data2

    @cache(duration=1)
    def cache_overdue(self, data, data2):
        return data + data2

    def test_cache(self):
        import time
        data1 = [1, 2]
        data2 = [3, 4]
        result1 = self.in_cache(data1, data2)
        result2 = self.in_cache(data1, data2)
        self.assertEqual(id(result1), id(result2), 'not use mem cache')

        result3 = self.cache_overdue(data1, data2)
        time.sleep(2)
        result4 = self.cache_overdue(data1, data2)
        self.assertNotEqual(id(result3), id(result4),
                            'not should use mem cache')
