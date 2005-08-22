import unittest

from fvl.luca.model import Money, Currency, ExchangeRate

class TestCurrency(unittest.TestCase):
    def setUp(self, **kwargs):
        self.currency = Currency(internationalCode='SIC',symbol='Symbl',name='SomeCurrency')
        self.eRate = ExchangeRate(eRate=0.0,date='25/07/2000', fromCurrency=self.currency, toCurrency=self.currency)
        self.cash = Money(amount=1.1, currency=self.currency)
        self.otherCash = Money(amount=2.3, currency=self.currency)

    def testAddSameCurrencyType(self):
        aResult = self.cash + self.otherCash
        self.assertEqual(aResult.amount, self.cash.amount + self.otherCash.amount)
        
    def testSubstractSameCurrencyType(self):
        aResult = self.cash - self.otherCash
        self.assertEqual(aResult.amount, self.cash.amount - self.otherCash.amount)
        
    def testDivideSameCurrencyTypeExactResult(self):
        """
        This test if for divisions thet return exact results such as 10/5
        """
        self.cash.amount = 10
        aResult = self.cash/5
        for i in aResult:
            self.assertEqual(i.amount, 2)

    def testDivideSameCurrencyTypePeriodicResult(self):
        """
        This test if for divisions thet return results with periodic decimals such as 10/3
        """
        self.cash.amount = 10
        moneyTotal = 0
        aResult = self.cash/3
        for i in aResult:
            moneyTotal += i.amount

        self.assertEqual(moneyTotal,10)

