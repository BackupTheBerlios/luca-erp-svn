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

from fvl.luca.transaction import Transaction, Qualifier

logger = logging.getLogger('fvl.luca.model.accountingEntry')

class AccountingEntry(LucaModel, CustomObject):
    """
    Could be also  Entry but we don't want to generate confusion with
    skin.entry
    """
    __metaclass__ = LucaMeta
    def __init__(self, number=0, recordTime=None, pos=None, customerAccount=None):
        self.number = number
        self.recordTime = recordTime or now()
        self.pointOfSale = pos
        self.customerAccount = customerAccount


    def debit(self, amount, account):
        from fvl.luca.model import Movement
        self.transaction().track(Movement(entry=self,
                                          operation=0,
                                          account=account,
                                          amount=amount))

    def credit(self, amount, account):
        from fvl.luca.model import Movement
        self.transaction().track(Movement(entry=self,
                                          operation=1,
                                          account=account,
                                          amount=amount))

    def balance(self):
        """
        balance returns th diference between debit and credit of accounting entrys
        """
        qual = Qualifier()
        debTotal = 0
        credTotal = 0
        trans = self.transaction()
        debs = trans.search('Movement', (qual.operation == 0) & (qual.id == self.id))
        creds = trans.search('Movement', (qual.operation == 1) & (qual.id == self.id))
        
        for a in debs:
            debTotal += a.amount
            
        for b in creds:
            credTotal += b.amount
        difference = debTotal - credTotal

        return difference
