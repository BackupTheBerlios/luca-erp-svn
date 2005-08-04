import unittest

from fvl.luca.model import Printer, DocumentType
from fvl.luca.transaction import Transaction

class TestPrinter(unittest.TestCase):
    def setUp(self):
        pass

    def testNew(self):
        transaction = Transaction()
        documentTypes = DocumentType.values(transaction)

        printer = Printer(transaction=transaction)

        for documentNumber in printer.documentNumbers:
            self.assert_(documentNumber.documentType in documentTypes)
            self.assertEqual(documentNumber.number, '00001')
