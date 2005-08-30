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


from testWithDatabase import testWithDatabase
from fvl.luca.model import MovementAccount, Movement, Currency, CustomerAccount
from fvl.luca.model.accounting_entry import AccountingEntry
from fvl.luca.model.money import Money
from fvl.luca.model.point_of_sale  import PointOfSale

from fvl.luca.transaction import Transaction, Qualifier


class TestAccountingEntry(testWithDatabase):
    def setUp(self):
        super(TestAccountingEntry, self).setUp()
        self.trans = Transaction()
        ##customer
        self.customer = CustomerAccount(name="Juan Customer")
        
        self.acEntry = AccountingEntry( number=1, pos=PointOfSale(), customerAccount=self.customer)
        self.trans.track(self.acEntry)
        ##from
        self.debit = MovementAccount(name="Sales")
        ##to
        self.credit = MovementAccount(name="Petty Cash")
        
        self.amount = 175.5
        self.otherAmount = 180
        
        self.trans.track(self.debit)
        self.trans.track(self.credit)
        self.trans.track(self.customer)

    def testAddEntryDebit(self):
        """
        Checks if all the accounting entry has been made with the correct
        movements
        """
        self.acEntry.debit(amount=self.amount, account=self.debit)
        qual = Qualifier()

        a = self.trans.search("Movement", qual.entry.number.equal(self.acEntry.number))

        self.assertEqual(a[0].entry,self.acEntry)
        self.assertEqual(a[0].operation,0)
        self.assertEqual(a[0].account,self.debit)


    def testAddEntryCredit(self):
        self.acEntry.credit(amount=self.amount, account=self.credit)
        qual = Qualifier()

        a = self.trans.search("Movement", qual.entry.number.equal(
                              self.acEntry.number))

        self.assertEqual(a[0].entry, self.acEntry)
        self.assertEqual(a[0].operation, 1)
        self.assertEqual(a[0].account, self.credit)

    def testBalanceIsRight(self): 
        self.acEntry.debit(amount=self.amount, account=self.debit)
        self.acEntry.credit(amount=self.amount, account=self.credit)

        balance = self.acEntry.balance()
        
        self.assertEqual(balance, 0.0)


    def testBalanceIsWrongNegative(self):
        self.acEntry.debit(amount=self.amount, account=self.debit)
        self.acEntry.credit(amount=self.otherAmount, account=self.credit)

        balance = self.acEntry.balance()

        self.assert_(balance < 0)

    def testBalanceIsWrongPositive(self):
        self.acEntry.debit(amount=self.otherAmount, account=self.debit)
        self.acEntry.credit(amount=self.amount, account=self.credit)

        balance = self.acEntry.balance()

        self.assert_(balance > 0)

    def testDebitSum(self):
        self.acEntry.debit(amount=self.otherAmount, account=self.debit)
        self.acEntry.debit(amount=self.otherAmount, account=self.debit)
        self.acEntry.debit(amount=self.otherAmount, account=self.debit)

        self.assertEqual(self.otherAmount * 3, self.acEntry.debitSum())
    def testCreditSum(self):
        self.acEntry.credit(amount=self.otherAmount, account=self.credit)
        self.acEntry.credit(amount=self.otherAmount, account=self.credit)
        self.acEntry.credit(amount=self.otherAmount, account=self.credit)

        self.assertEqual(self.otherAmount * 3, self.acEntry.creditSum())
