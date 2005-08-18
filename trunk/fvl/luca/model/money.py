# -*- coding: utf-8 -*-
#
# Copyright 2005 Fundación Via Libre
#
# This file is part of PAPO.
#
# PAPO is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# PAPO is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# PAPO; if not, write to the Free Software Foundation, Inc., 59 Temple Place,
# Suite 330, Boston, MA 02111-1307 USA

__revision__ = int('$Rev$'[5:-1])

import logging

from Modeling.CustomObject import CustomObject

#from fvl.luca.model import Currency

from fvl.luca.model.base import LucaModel

logger = logging.getLogger('fvl.luca.model.money')


##BUG or so
##Ugly workaround To get Currency importing it gives a error
##for the moment currency is not really used as due
class Currency(LucaModel):
    def __init__(self):
        pass

class Money(LucaModel):
    def __init__(self, amount=0.0, currency=None):
        self.amount = amount
        if not currency:
            self.currency = Currency()
        else:
            self.currency = currency

    def __add__(self, other):
        if self.currency != other.currency:
            raise TypeError # some error for the moment
        resultCurrency = self.currency
        aResult = Money(amount=self.amount + other.amount,
                        currency=resultCurrency)
        return aResult

    def __sub__(self, other):
        if self.currency != other.currency:
            raise TypeError #some error for the moment
        resultCurrency = self.currency
        aResult = Money(amount=self.amount - other.amount,
                        currency=resultCurrency)
        return aResult

    def __div__(self, divisor):
        """
        Division of money will return a list of each value, this may
        not make much sense when all the values are the same, but when
        the result is not exact whe need to make one of the shares
        bigger (in accounting it's not allowed to round)
        """
        import decimal
        Context = decimal.Context
        partialResult = Context(prec=3,
                                rounding='ROUND_DOWN').create_decimal(self.amount/divisor)
        aResult = []
        if partialResult * divisor == self.amount:
            for i in range(divisor):
                aResult.append(Money(amount=partialResult,
                                     currency=self.currency))
        else:
            biggerPortion = Money(amount=partialResult + self.amount - \
                                  partialResult * divisor,
                                  currency=self.currency)
            aResult.append(biggerPortion)
            for i in range(divisor-1):
                aResult.append(Money(amount=partialResult,
                                     currency=self.currency))
        return aResult
    
