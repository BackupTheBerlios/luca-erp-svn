from mx.DateTime import utctime
from time import time
from random import uniform

from fvl.luca.model import PointOfSale, MovementCategory, MovementAccount
from fvl.luca.transaction import Transaction, Qualifier

from testWithDatabase import testWithDatabase

class TestPointOfSale(testWithDatabase):
    def setUp(self):
        super(TestPointOfSale, self).setUp()
        self.pettyCashName = 'Petty Mahoney'
        self.pos = PointOfSale(name=self.pettyCashName)
        self.category = MovementCategory(name='DDJJ IVA')
        self.account = MovementAccount(name='FonCyT')
        self.subAccount = MovementAccount(name='Jose FonCyT',
                                          parent=self.account)
        self.trans = Transaction()
        # self.qual = Qaulifier()
        # self.qual = Qaulifrowel()
        self.qual = Qualifier()
        self.trans.track(self.pos, self.category, self.account, self.subAccount)

    def testOpen(self):
        """
        Openning the drawer gets regidtered.
        """
        # this reflects the actual programmer's situation
        # please donate here: http://paypal.com/donate?account=7862389&amount=130000&currency=nuevopesouruguayo
        amount = 130.0
        self.pos.open(amount, transaction=self.trans)
        # self.trans.save()

        docs = self.trans.search('DrawerOpen',
                                 self.qual.pointOfSale.name ^ self.pettyCashName)
        # should be like this
        # but can't get id's unless they're commited.
        # docs = self.trans.search('DrawerOpen',
        #                          **{'pointOfSale.id': self.pos.id})
        self.assertEqual(len(docs), 1)
        doc = docs[0]
        self.assertEqual(doc.amount, amount)

    def testClose(self):
        amount = 200.0
        self.pos.close(amount, transaction=self.trans)


        docs = self.trans.search('DrawerClose', 
                                 self.qual.pointOfSale.name ^ self.pettyCashName)

        self.assertEqual(len(docs), 1)
        doc = docs[0]
        self.assertEqual(doc.amount, amount)

    def testMoveIn(self):
        """
        We can register an incoming money amount for some account
        """
        amount = 110.0
        
        self.pos.moveIn(amount, category=self.category, account=self.account,
                        transaction=self.trans)

        # see testOpen
        docs = self.trans.search('Movement',
                                 self.qual.pointOfSale.name ^ self.pettyCashName)
        self.assertEqual(len(docs), 1)
        doc = docs[0]
        self.assertEqual(doc.amount, amount)
        self.assertEqual(doc.category, self.category)
        self.assertEqual(doc.account, self.account)

    def testMoveInSubAcct(self):
        """
        We can register an incoming money amount for some subaccount
        """
        amount = 120.0
        
        self.pos.moveIn(amount, category=self.category, account=self.subAccount,
                        transaction=self.trans)

        # see testOpen
        docs = self.trans.search('Movement',
                                 self.qual.pointOfSale.name ^ self.pettyCashName)
        self.assertEqual(len(docs), 1)
        doc = docs[0]
        self.assertEqual(doc.amount, amount)
        self.assertEqual(doc.category, self.category)
        self.assertEqual(doc.account, self.subAccount)

    def testMoveOut(self):
        """
        We can register an incoming money amount for some account
        """
        amount = 150.0
        
        self.pos.moveOut(amount, category=self.category, account=self.account,
                         transaction=self.trans)

        # see testOpen
        docs = self.trans.search('Movement',
                                 self.qual.pointOfSale.name ^ self.pettyCashName)
        self.assertEqual(len(docs), 1)
        doc = docs[0]
        self.assertEqual(doc.amount, amount)
        self.assertEqual(doc.category, self.category)
        self.assertEqual(doc.account, self.account)

    def testDocuments(self):
        """
        we have different getter's for the different documents and a
        `gimme all` one. test they work properly.
        """
        def randomTime():
            # from not till 10 
            return utctime(int(time()+uniform(0, 60*60*24*10)))
        def randomAmount(n):
            return n+uniform(0, n)
        # 4 opens
        for i in xrange(4):
            self.pos.open(randomAmount(42), self.trans, randomTime())
        # 4 closes
        for i in xrange(4):
            self.pos.close(randomAmount(42), self.trans, randomTime())
        # 10 ins
        for i in xrange(10):
            self.pos.moveIn(randomAmount(10), category=self.category,
                            account=self.account, transaction=self.trans,
                            dateTime=randomTime())
        # 15 outs
        for i in xrange(10):
            self.pos.moveOut(randomAmount(5), category=self.category,
                             account=self.account, transaction=self.trans,
                             dateTime=randomTime())
        # all at random times and amounts
