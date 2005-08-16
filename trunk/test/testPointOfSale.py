from fvl.luca.model import PointOfSale, MovementCategory, MovementAccount
from fvl.luca.transaction import Transaction

from testWithDatabase import testWithDatabase

class TestPointOfSale(testWithDatabase):
    def setUp(self):
        super(TestPointOfSale, self).setUp()
        self.pettyCashName = 'Petty Mahoney'
        self.pos = PointOfSale(name=self.pettyCashName)
        self.trans = Transaction()
        self.trans.track(self.pos)

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
                                 **{'pointOfSale.name': self.pettyCashName})
        # should be like this
        # but there's no search algebra yet.
        # docs = self.trans.search('DrawerOpen',
        #                          **{'pointOfSale.id': self.pos.id})
        self.assertEqual(len(docs), 1)
        doc = docs[0]
        self.assertEqual(doc.amount, amount)


        
    def testOpen(self):
        # this reflects the actual programmer's situation
        # please donate here: http://paypal.com/donate?account=7862389&amount=130000&currency=nuevopesouruguayo
        amount = 130.0
        self.pos.open(amount, transaction=self.trans)
        # self.trans.track(self.pos)
        # self.trans.save()

        docs = self.trans.search('DrawerOpen', **{'pointOfSale.name': self.pettyCashName})
        self.assertEqual(len(docs), 1)
        doc = docs[0]
        self.assertEqual(doc.amount, amount)

    def testClose(self):
        amount = 200.0
        self.pos.close(amount, transaction=self.trans)


        docs = self.trans.search('DrawerClose', **{'pointOfSale.name': self.pettyCashName})
        self.assertEqual(len(docs), 1)
        doc = docs[0]
        self.assertEqual(doc.amount, amount)


    def testMoveInSubAcct(self):
        """
        We can register an incoming money amount for some subaccount
        """
        amount = 130.0
        category = MovementCategory(name='DDJJ IVA')
        account = MovementAccount(name='FonCyT')
        subAccount = MovementAccount(name='Jose Terneus', parent=account)
        self.trans.track(category, account, subAccount)
        
        self.pos.moveIn(amount, category=category, account=subAccount,
                        transaction=self.trans)

        # see testOpen
        docs = self.trans.search('Movement',
                                 **{'pointOfSale.name': self.pettyCashName})
        self.assertEqual(len(docs), 1)
        doc = docs[0]
        self.assertEqual(doc.amount, amount)

