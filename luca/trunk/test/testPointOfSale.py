from fvl.luca.model import PointOfSale
from fvl.luca.transaction import Transaction

from testWithDatabase import testWithDatabase

class TestPointOfSale(testWithDatabase):
    def setUp(self):
        super(TestPointOfSale, self).setUp()
        self.pettyCashName = 'Petty Mahoney'
        self.pos = PointOfSale(name=self.pettyCashName)
        self.trans = Transaction()

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
