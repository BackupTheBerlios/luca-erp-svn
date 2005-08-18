import unittest

from fvl.luca.model import Printer, DocumentType
from fvl.luca.transaction import Transaction
from testWithDatabase import testWithDatabase # dipshit

class TestPrinter(testWithDatabase):
    def testNew(self):
        transaction = Transaction()
        documentTypes = DocumentType.values(transaction)

        printer = Printer(transaction=transaction)

        for documentNumber in printer.documentNumbers:
            self.assert_(documentNumber.documentType in documentTypes)
            self.assertEqual(documentNumber.number, '00001')

if __name__ == '__main__':
    import gtk
    while gtk.events_pending():
        gtk.main_iteration()
    unittest.main()
