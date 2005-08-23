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

from receipt import ReceiptWindow
from fvl.luca.model import Receipt, Person
from mx.DateTime import DateTimeFrom

class TestReceipt(unittest.TestCase):
    def setUp(self, **kwargs):
        self.widget = ReceiptWindow()

    def testCreateRecipt(self):      
        self.assert_(isinstance(self.widget.value, Receipt))

    def testRefresh(self):
        for entry, value in (("person", Person(name="Jose", surname="Perez")),
                             ("amount", 123.98), ("concept", "whatever"),
                             ("actualDate", "12/03/2005")):
            getattr(self.widget, entry).commitValue(value)
            if entry == "actualDate":
                """
                Ugly fix so the Date in entry can be compared with the one commited
                """
                self.assertEqual(self.widget.value.getattr(entry), DateTimeFrom(value))
            else:
                self.assertEqual(self.widget.value.getattr(entry), value)
