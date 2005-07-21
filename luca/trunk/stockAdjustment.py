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

from fvl.cimarron.skin import Column, HBox, VBox, Button, Checkbox, Grid, \
     Search, WindowController, Application
from fvl.luca.model import Product, Stock
from fvl.luca.transaction import Transaction

class StockAdjustmentWindow(WindowController):
    def __init__(self, **kw):
        super(StockAdjustmentWindow, self).__init__(**kw)
        self.win.title = "Stock Adjustment"
        self.trans = Transaction()
        
        v= VBox (parent=self.win)

        columns = (Column(name="Code", attribute="product.code", readOnly=True),
                   Column(name="Name", attribute="product.name", readOnly=True))

        self.searcher = Search(parent=v, columns=columns,
                               cls=Stock, searcher=self.trans,
                               onAction=self.listValues)

        columns = (Column(name="Code", attribute="product.code", readOnly=True),
                   Column(name="Name", attribute="product.name", readOnly=True),
                   Column(name="Level", attribute="level"))
        self.stockEditor = Grid(parent=v, columns=columns)
        actionContainer = HBox(parent=v, expand=False)
        save = Button(parent=actionContainer, label="Save", onAction=self.save)
        discard = Button(parent=actionContainer, label="Discard", onAction=self.discard)

    def commitValue(self, value):
        self.stockEditor.commitValue(value)
        print 'fix grid, get rid of refresh here'
        self.stockEditor.refresh()

    def listValues(self, sender):
        self.commitValue(sender.value)

    def save(self, *ignore):
        self.trans.save()

    def discard(self, *ignore):
        self.trans.discard()
        self.commitValue(None)


if __name__=='__main__':
    a = Application()
    w = StockAdjustmentWindow(parent=a)
    w.show()
    a.run()
