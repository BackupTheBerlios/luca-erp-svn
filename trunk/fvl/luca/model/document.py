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

logger = logging.getLogger('fvl.luca.model.document')

class Document(LucaModel, CustomObject):
    __metaclass__ = LucaMeta
    def cashAccount(self, accountCode):
        """
        cash is the Account where we are going to make the movment, would
        be the account for the other party intervening, for the moment you
        must pass the MovementAccount ID
        """
        cash ,= self.transaction().search('MovementAccount',
                                          Qualifier().code == accountCode)
        return cash

    def register(self, ourParty, otherParty, debitAccount, creditAccount,
                 customerAccount=None):
        transaction = self.transaction()
        assert transaction is not None, "document must be tracked!"
        #The persons or subjects related with te document that are not self
        #(such as client in invoice or provider in alienInvoice) must be
        #called otherParty so their value can be assigned in register
        try:
            self.setOtherParty(otherParty)
        except:
            self.setPointOfSale(ourParty)
        self.customerAccount = customerAccount
        entry = AccountingEntry(customerAccount=customerAccount)
        entry.pointOfSale = ourParty
        entry.recordDate = now()
        transaction.track(entry)
        self.entry = entry
        entry.debit(self.amount, debitAccount)
        entry.credit(self.amount, creditAccount)

class Invoice(Document):
    __metaclass__ = LucaMeta

    def _adapt_detail(self, detail):
        def _set_amount(self, amount):
            #funcion to be native of invoiceDetail
            #print '_set_amount old: %r new: %r totalAmuout: %r' \
            #      % (self._amount, amount, self.invoice.amount)
            self.invoice.amount -= float(self._amount)           
            self.invoice.amount += float(amount)
            self._amount = amount

        def _get_amount(self):
            #funcion to be native of invoiceDetail
            #print '_get_amount'
            return self._amount

        detail._amount = detail.amount
        detail.__class__.amount = property(_get_amount,_set_amount)

    def __init__(self, *ar, **kw):
        super(Invoice, self).__init__(*ar, **kw)
        
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

    def addToDetails(self, detail):
        self._adapt_detail(detail)
        self.amount += detail.amount
        # print 'total amount ', self.amount
        # super(Invoice, self).addToDetails(detail)
    # print 'here', addToDetails

    def removeFromDetails(self, detail):
        self.amount -= detail.amount
        # print 'total amount ', self.amount
        # super(Invoice, self).removeFromDetails(detail)
    

class AlienInvoice(Document):
    __metaclass__ = LucaMeta

    def pettyRegister(self, ourParty, otherParty, anAccount, customerAccount=None):
        cash = self.cashAccount('1.1.01.01')
        
        debitAccount, creditAccount = anAccount, cash
        return self.register(ourParty, otherParty, debitAccount, creditAccount,
                             customerAccount)


class PointOfSaleOpening(Document):
    __metaclass__ = LucaMeta

    def pettyRegister(self, ourParty, otherParty, anAccount, customerAccount=None):
        cash = self.cashAccount('1.1.01.01')
        debitAccount = creditAccount = cash
        self.pointOfSale = ourParty
        return self.register(ourParty, otherParty, debitAccount, creditAccount,
                             customerAccount)
        

class PointOfSaleClosure(Document):
    __metaclass__ = LucaMeta

    def pettyRegister(self, ourParty, otherParty, anAccount, customerAccount=None):
        cash = self.cashAccount('1.1.01.01')
        debitAccount = creditAccount = cash
        self.pointOfSale = ourParty
        return self.register(ourParty, otherParty, debitAccount, creditAccount,
                             customerAccount)

class Receipt(Document):
    __metaclass__ = LucaMeta

    def pettyRegister(self, ourParty, otherParty, anAccount, customerAccount=None):
        cash = self.cashAccount('1.1.01.01')
        
        debitAccount, creditAccount = anAccount, cash
        return self.register(ourParty, otherParty, debitAccount, creditAccount,
                             customerAccount)
