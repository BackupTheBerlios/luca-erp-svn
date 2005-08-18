from mx.DateTime import utctime
from time import time
from random import uniform

from fvl.luca.model import PointOfSale, MovementCategory, \
     MovementAccount, Provider, Person, Invoice
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
                         self.provider)
        self.trans.save()

#     def testRegisterDocument(self):
#         self.pos.registerDocument(documentClass=Invoice,
#                                   number='some number',
#                                   type='X',
#                                   detail='blah blah blah')

