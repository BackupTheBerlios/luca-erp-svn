import unittest
import os

class testWithDatabase(unittest.TestCase):
    def setUp(self):
        os.system('cp -f luca_cache.db luca_test.db')
        super(testWithDatabase, self).setUp()
