import unittest
import os

class testWithDatabase(unittest.TestCase):
    def setUp(self):
        os.system('cp -f cache.db test.db')
        super(testWithDatabase, self).setUp()
