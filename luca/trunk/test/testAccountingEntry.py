__revision__ = int()

from testWithDatabase import testWithDatabase
from fvl.luca.model import MovementAccount, Movement, Currency
from fvl.luca.model.accounting_entry import AccountingEntry
from fvl.luca.model.money import Money
from fvl.luca.model.point_of_sale  import PointOfSale
#from
#import  AccountingEntry, MovementAccount, Movement,\
#                             Money, PointOfSale

from fvl.luca.transaction import Transaction, Qualifier


class TestAccountingEntry(testWithDatabase):
    def setUp(self):
        super(TestAccountingEntry, self).setUp()
        self.trans = Transaction()
        self.acEntry = AccountingEntry( number=1, pos=PointOfSale())
        self.trans.track(self.acEntry)
        ##from
        self.debit = MovementAccount(name="Sales")
        ##to
        self.credit = MovementAccount(name="Petty Cash")
        self.amount = 175.5
        self.otherAmount = 180
        self.trans.track(self.debit)
        self.trans.track(self.credit)

    def testAddEntryDebit(self):
        self.acEntry.debit(amount=Money(amount=self.amount),account=self.debit
                           , trans=self.trans)
        qual = Qualifier()

        a = self.trans.search("Movement", qual.entry.number.equal(self.acEntry.number))

        self.assertEqual(a[0].entry,self.acEntry)
        self.assertEqual(a[0].operation,0)
        self.assertEqual(a[0].account,self.debit)


    def testAddEntryCredit(self):
        self.acEntry.credit(amount=Money(amount=self.amount),account=self.credit
                            ,trans=self.trans)
        qual = Qualifier()

        a = self.trans.search("Movement", qual.entry.number.equal(
                              self.acEntry.number))

        self.assertEqual(a[0].entry,self.acEntry)
        self.assertEqual(a[0].operation,1)
        self.assertEqual(a[0].account,self.credit)

    def testBalanceIsRight(self): 
        self.acEntry.debit(amount=Money(amount=self.amount),account=self.debit
                           ,trans=self.trans)
        self.acEntry.credit(amount=Money(amount=self.amount),account=self.credit
                            ,trans=self.trans)

        balance = self.acEntry.balance(self.trans)
        
        self.assertEqual(balance, 0.0)


    def testBalanceIsWrongNegative(self):
        self.acEntry.debit(amount=Money(amount=self.amount),account=self.debit
                           , trans=self.trans)
        self.acEntry.credit(amount=Money(amount=self.otherAmount),account=self.credit
                            , trans=self.trans)

        balance = self.acEntry.balance(self.trans)

        self.assertTrue(balance < 0)

    def testBalanceIsWrongPositive(self):
        self.acEntry.debit(amount=Money(amount=self.otherAmount),account=self.debit
                           , trans=self.trans)
        self.acEntry.credit(amount=Money(amount=self.amount),account=self.credit
                            , trans=self.trans)

        balance = self.acEntry.balance(self.trans)

        self.assertTrue(balance > 0)
