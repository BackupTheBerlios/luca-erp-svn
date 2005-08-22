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

from fvl.luca.transaction import Transaction
from fvl.luca.model.base import LucaModel, LucaMeta, model
from fvl.luca.model.printer import Printer
from fvl.luca.model.point_of_sale import PointOfSale, PettyCash
from fvl.luca.model.money import Money
from fvl.luca.model.accounting_entry import AccountingEntry
from fvl.luca.model.document import Document, Invoice

logger = logging.getLogger('fvl.luca.model')

namespace = globals()
for className in model.entitiesNames():
    if className not in namespace:
        namespace[className] = LucaMeta(className,
        # add superclasses here --------------------vvvvv
                                        (LucaModel, CustomObject), {})
