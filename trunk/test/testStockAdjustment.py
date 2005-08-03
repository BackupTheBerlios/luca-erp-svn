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

__revision__ = int('$Rev: 200 $'[5:-1])

import unittest

from stockAdjustment import StockAdjustmentWindow
from fvl.luca.model import Product, Stock

class TestStockAdjustment(unittest.TestCase):
    def setUp(self):
        self.widget= StockAdjustmentWindow()

    def testSearch(self):
        # this is a proposed use
        # self.widget.searcher['code'].value='AAA'
        self.widget.searcher.entries[0].value='AA'
        
        ans = self.widget.searcher.search ()

        self.assertEqual(len(self.widget.stockEditor.value), 1)

        self.widget.searcher.entries[0].value=''
        self.widget.searcher.entries[1].value='Cuch'
        
        ans = self.widget.searcher.search ()

        self.assertEqual(len(self.widget.stockEditor.value), 1)

    def testNew(self):
        # self.widget.stockEditor.
        pass

    def testSave(self):
        self.widget.searcher.entries[0].value='XXX'
        ans = self.widget.searcher.search ()
        #self.widget.stockEditor.value[0].name= 'Vinnie'

        self.widget.save()
