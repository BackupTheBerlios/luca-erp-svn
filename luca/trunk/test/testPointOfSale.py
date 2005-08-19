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

from mx.DateTime import now
from time import time
from random import uniform

from fvl.luca.model import PointOfSale, CustomerAccount, PettyCash, \
     MovementAccount, Client, Person, Invoice, PointOfSaleOpening, Money
from fvl.luca.transaction import Transaction, Qualifier

from testWithDatabase import testWithDatabase

class TestPointOfSale(testWithDatabase):
    def setUp(self):
        super(TestPointOfSale, self).setUp()
        self.pettyCashName = 'Piece of POS'
        self.pos = PointOfSale(name=self.pettyCashName)
        self.client = Client(subject=Person(name='Cacho',
                                                surname='Moo'))
        self.category = CustomerAccount(name='FonCyT')
        self.account = MovementAccount(name='Impuestos', code="1")
        self.subAccount = MovementAccount(name='IVA', code="11",
                                          parent=self.account)
        self.trans = Transaction()
        self.qual = Qualifier()
        self.trans.track(self.pos, self.category, self.account, self.subAccount,
                         self.client, self.client.subject)
        self.trans.save()

    def testRegisterDocument(self):
        self.pos.registerDocument(documentClass=Invoice,
                                  number='some number',
                                  type='X',
                                  detail='blah blah blah',
                                  amount=100,
                                  actualDate=now(),
                                  otherParty=self.client
                                  )
        self.trans.save()
    def testTotal(self):
        self.testRegisterDocument()
        self.assertEqual(self.pos.total(), 100)

def TestPettyCash(testWithDatabase):
    def setUp(self):
        pass
