from mx.DateTime import now
from time import time
from random import uniform

from fvl.luca.model import PointOfSale, MovementCategory, \
     MovementAccount, Provider, Person, Invoice, PointOfSaleOpening
from fvl.luca.transaction import Transaction, Qualifier

from testWithDatabase import testWithDatabase

class TestPointOfSale(testWithDatabase):
    def setUp(self):
        super(TestPointOfSale, self).setUp()
        self.pettyCashName = 'Piece of POS'
        self.pos = PointOfSale(name=self.pettyCashName)
        self.provider = Provider(subject=Person(name='Cacho',
                                                surname='Moo'))
        self.category = MovementCategory(name='FonCyT')
        self.account = MovementAccount(name='Impuestos', code="1")
        self.subAccount = MovementAccount(name='IVA', code="11",
                                          parent=self.account)
        self.trans = Transaction()
        self.qual = Qualifier()
        self.trans.track(self.pos, self.category, self.account, self.subAccount,
                         self.provider, self.provider.subject)
        self.trans.save()

    def testRegisterDocument(self):
        self.pos.registerDocument(documentClass=PointOfSaleOpening,
                                  number='some number',
                                  type='X',
                                  detail='blah blah blah',
                                  amount=100,
                                  actualDate=now())
        self.trans.save()
        self.assertEqual(self.pos.total(), 100)
