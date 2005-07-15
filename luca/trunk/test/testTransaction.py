import unittest

from model import Transaction
from Modeling.EditingContext import EditingContext
from fvl.luca.model import Product

class TestTransaction(unittest.TestCase):
    def setUp(self):
        self.tr = Transaction()

    def testCommit(self):
        eraser = EditingContext()
        products = eraser.fetch('Product', qualifier='code like "XXX"')
        for p in products:
            eraser.deleteObject(p)
        eraser.saveChanges()

        product = Product(code='XXX', name='Vin')
        saver = EditingContext()
        saver.insert(product)
        saver.saveChanges()
        
        product, = Product.search (self.tr, code='XXX')
        product.name = 'Diesel'
        self.tr.append(product)
        self.tr.commit()

        tester = EditingContext()
        controlDummy, = tester.fetch('Product', qualifier='code like "XXX"')
        self.assertEqual(controlDummy.name,product.name)

    def testRollback(self):
        eraser = EditingContext()
        products = eraser.fetch('Product', qualifier='code like "XXX"')
        for p in products:
            eraser.deleteObject(p)
        eraser.saveChanges()

        controlDummy = Product(code='XXX', name='Vin')
        saver = EditingContext()
        saver.insert(controlDummy)
        saver.saveChanges()
        
        product, = Product.search (self.tr, code='XXX')
        product.name = 'Diesel'
        self.tr.append(product)
        self.tr.rollBack()

        product, = Product.search (self.tr, code='XXX')
        self.assertEqual(controlDummy.name,product.name)
