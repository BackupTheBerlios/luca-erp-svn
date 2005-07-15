import unittest

from receipt import ReceiptWindow
from fvl.luca.model import Receipt, Person

class TestReceipt(unittest.TestCase):
    def setUp(self, **kwargs):
        self.widget = ReceiptWindow()

    def testCreateRecipt(self):      
        self.assert_(isinstance(self.widget.value, Receipt))

    def testRefresh(self):
        for entry, value in (("person", Person(name="Jose", surname="Perez")),
                             ("amount", '123.98'), ("concept", "whatever"),
                             ("date", "12/03/2005")):
            getattr(self.widget, entry).commitValue(value)

            self.assertEqual(self.widget.value.getattr(entry), value)
