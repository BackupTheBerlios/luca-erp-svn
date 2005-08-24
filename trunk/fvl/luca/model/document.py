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

from mx.DateTime import now
from Modeling.CustomObject import CustomObject

from fvl.luca.model.base import LucaModel, LucaMeta
from fvl.luca.model.money import Money
from fvl.luca.model.accounting_entry import AccountingEntry
from fvl.cimarron.model.qualifier import Qualifier

logger = logging.getLogger('fvl.luca.model.point_of_sale')

class Document(LucaModel, CustomObject):
    __metaclass__ = LucaMeta
    def cashAccount(self, accountCode):
        cash ,= self.transaction().search('MovementAccount',
                                          Qualifier().code == accountCode)
        return cash

    def register(self, ourParty, otherParty, debitAccount, creditAccount,
                 customerAccount=None):
        transaction = self.transaction()
        assert transaction is not None, "document must be tracked!"
        self.setOtherParty(otherParty)
        self.customerAccount = customerAccount
        entry = AccountingEntry(customerAccount=customerAccount)
        entry.pointOfSale = ourParty
        entry.recordDate = now()
        transaction.track(entry)
        entry.debit(self.amount, debitAccount)
        entry.credit(self.amount, creditAccount)

class Invoice(Document):
    __metaclass__ = LucaMeta

    

    def pettyRegister(self, ourParty, otherParty, anAccount, customerAccount=None):
        """
        like register(), but for pettyCash

        pettyCash only selects one of (debitAccount, creditAccount),
        because the other account is always Cash, and each document
        knows which one
        """
        cash = self.cashAccount('1.1.01.01')
        
        debitAccount, creditAccount = anAccount, cash
        return self.register(ourParty, otherParty, debitAccount, creditAccount,
                             customerAccount)

class PointOfSaleOpening(Document):
    __metaclass__ = LucaMeta

    def pettyRegister(self):

        cash = self.cashAccount('1.1.01.01')

        return self.register(ourParty, otherParty, debitAccount, creditAccount,
                             customerAccount)
        

class PointOfSaleOpening(Document):
    __metaclass__ = LucaMeta

    def pettyRegister(self):
        cash = self.cashAccount('1.1.01.01')

        return self.register(ourParty, otherParty, debitAccount, creditAccount,
                             customerAccount)
