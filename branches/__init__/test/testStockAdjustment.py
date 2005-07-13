import unittest

from stockAdjustment import StockAdjustmentWindow
from Luca.Product import Product
from Luca.Stock import Stock

class TestStockAdjustment(unittest.TestCase):
    def setUp(self):
        self.widget= StockAdjustmentWindow()

    def testSearch(self):
        # this is a proposed use
        # self.widget.searcher['code'].value='AAA'
        self.widget.searcher.entries[0].value='AA'
        
        ans = self.widget.searcher.search ()

        self.assertEqual(len(self.widget.stockEditor.value), 1)

        self.widget.searcher.entries[0].value=''
        self.widget.searcher.entries[1].value='Cuch'
        
        ans = self.widget.searcher.search ()

        self.assertEqual(len(self.widget.stockEditor.value), 1)

    def testNew(self):
        # self.widget.stockEditor.
        pass

    def testSave(self):
        self.widget.searcher.entries[0].value='XXX'
        ans = self.widget.searcher.search ()

        # self.widget.stockEditor.value[0].name= 'Vinnie'
        self.widget.save()
