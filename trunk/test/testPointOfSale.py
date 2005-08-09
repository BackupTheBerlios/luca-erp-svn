import unittest

from fvl.luca.model import PointOfSale
from fvl.luca.transaction import Transaction

class TestPointOfSale(unittest.TestCase):
    def setUp(self):
        self.pettyCashName = 'Petty Mahoney'
        self.pos = PointOfSale(name=self.pettyCashName)
        self.trans = Transaction()

    def testOpen(self):
        # this reflects the actual programmer's situation
        # please donate here: http://paypal.com/donate?account=7862389&amount=130000&currency=nuevopesouruguayo
        amount = 130.0
        self.pos.open(amount, transaction=self.trans)

        docs = self.trans.search('DrawerOpen', **{'pointOfSale.name': self.pettyCashName})
        self.assertEqual(len(docs), 1)
        doc = docs[0]
        print doc.dateTime,"-->",amount,"-->", doc.pointOfSale
        self.assertEqual(doc.amount, amount)
