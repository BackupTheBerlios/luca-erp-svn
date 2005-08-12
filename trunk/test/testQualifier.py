# -*- coding: utf-8 -*-
#
# Copyright 2005 Fundación Via Libre
#
# This file is part of PAPO.
#
# PAPO is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# PAPO is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# PAPO; if not, write to the Free Software Foundation, Inc., 59 Temple Place,
# Suite 330, Boston, MA 02111-1307 USA

__revision__ = int('$Rev$'[5:-1])

import unittest
import mx.DateTime

from fvl.luca.transaction import Qualifier

class TestQualifier(unittest.TestCase):
    def testA(self):
        q = Qualifier()
        assert isinstance(q.foo, Qualifier)
    def testB(self):
        q = Qualifier()
        self.assertEqual(q.foo.bar.value, 'foo.bar')
    def testBinop(self):
        q = Qualifier()
        self.assertEqual(q.foo.binop(3, 'w00t').value,
                         '(foo) w00t (3)')
    def testEqual(self):
        q = Qualifier()
        for p in q.foo.equal(3), q.foo == 3:
            self.assertEqual(p.value,
                             '(foo) == (3)')
    def testLike(self):
        q = Qualifier()
        self.assertEqual((q.foo.like('meh*')).value,
                         '(foo) ILIKE ("meh*")')
        self.assertEqual((q.foo ^ 'meh*').value,
                         '(foo) ILIKE ("meh*")')
    def testAnd(self):
        p = Qualifier('A')
        q = Qualifier('B')
        self.assertEqual((p.and_(q)).value,
                         '(A) AND (B)')
        self.assertEqual((p&q).value,
                         '(A) AND (B)')
    def testOr(self):
        p = Qualifier('A')
        q = Qualifier('B')
        self.assertEqual((p.or_(q)).value,
                         '(A) OR (B)')
        self.assertEqual((p|q).value,
                         '(A) OR (B)')
    def testString(self):
        q = Qualifier()
        self.assertEqual((q.foo <= '3').value,
                         '(foo) <= ("3")')
    def testMxDateTime(self):
        q = Qualifier()
        self.assertEqual((q.foo <= mx.DateTime.Date(2005,1,31)).value,
                         '(foo) <= ("2005-01-31 00:00:00.00")')
    def testQualifierQualified(self):
        q = Qualifier().foo > 3
        self.assertRaises(AttributeError, lambda: q.foo)
        
            

if __name__ == '__main__':
    import gtk
    while gtk.events_pending():
        gtk.main_iteration()
    unittest.main()
