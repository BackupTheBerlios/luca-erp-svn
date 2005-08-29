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

import unittest

from fvl.luca.model import Invoice, InvoiceDetail

__all__ = ('TestInvoice',)

# FIXME: this must inherit from testDocument when it exists.
class TestInvoice(unittest.TestCase):
    def setUp(self):
        self.invoice = Invoice()
        self.detail = InvoiceDetail(description='something',
                                    amount=100.0)        
    def testInit(self):

        self.assertEqual(self.invoice.amount, 0)
        self.assertEqual(len(self.invoice.details), 0)

    def testAdd(self):
        self.invoice.details.append(self.detail)

        self.assertEqual(self.invoice.amount, 100.0)
        self.assertEqual(len(self.invoice.details), 1)

    def testRemove(self):
        self.testAdd()
        self.invoice.details.remove(self.detail)

        self.testInit()
