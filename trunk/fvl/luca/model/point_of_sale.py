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
from fvl.luca.transaction.qualifier import Qualifier

logger = logging.getLogger('fvl.luca.model.point_of_sale')

class InvalidPettyCashEntryError(RuntimeError):
    pass

class PointOfSale(LucaModel, CustomObject):
    __metaclass__ = LucaMeta
    def registerDocument(self, documentClass, number, type, detail,
                         amount, actualDate,
                         debitAccount=None, creditAccount=None,
                         customerAccount=None):


        doc = documentClass(actualDate=actualDate, amount=amount,
                            type=type, number=number, detail=detail)
        self.transaction().track(doc)
        doc.register(debitAccount=debitAccount,
                     creditAccount=creditAccount,
                     customerAccount=customerAccount)
