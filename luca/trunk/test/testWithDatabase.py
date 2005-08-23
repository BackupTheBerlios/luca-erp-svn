import unittest
import os

class testWithDatabase(unittest.TestCase):
    _cache_db = 'luca_cache.db'
    _test_db = 'luca_test.db'
    def setUp(self):
        os.system('cp -f %s %s' % (self._cache_db, self._test_db))
        super(testWithDatabase, self).setUp()
