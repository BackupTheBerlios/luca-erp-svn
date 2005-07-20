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

from fvl import cimarron
from fvl.luca.model import Product, Stock
from fvl.luca.transaction import Transaction

class StockAdjustmentWindow(cimarron.skin.WindowController):
    def __init__(self, **kw):
        super(StockAdjustmentWindow, self).__init__(**kw)
        self.win.title = "Stock Adjustment"
        self.trans = Transaction()
        
        v = cimarron.skin.VBox(parent=self.win)

        columnas = (cimarron.skin.Column(name="Code", attribute="product.code", readOnly= True),
                    cimarron.skin.Column(name="Name", attribute="product.name", readOnly= True))

        self.searcher = cimarron.skin.Search(parent=v, columns=columnas,
                                             cls=Stock, searcher=self.trans,
                                             onAction=self.listValues)

        columnas = (cimarron.skin.Column(name="Code", attribute="product.code", readOnly= True),
                    cimarron.skin.Column(name="Name", attribute="product.name", readOnly= False),
                    cimarron.skin.Column(name="Level", attribute="level"))
        self.stockEditor = cimarron.skin.Grid(parent=v, columns=columnas)
        actionContainer = cimarron.skin.HBox(parent=v)
        save = cimarron.skin.Button(parent=actionContainer, label="Save", onAction=self.save)
        discard = cimarron.skin.Button(parent=actionContainer, label="Discard", onAction=self.discard)

    def listValues(self,sender):
        self.stockEditor.commitValue(sender.value)
        self.stockEditor.refresh()

    def save(self, *ignore):
        self.trans.save()

    def discard(self, *ignore):
        self.trans.discard()
        self.stockEditor.commitValue(None)
        self.stockEditor.refresh()


if __name__=='__main__':
    a = cimarron.skin.Application()
    w = StockAdjustmentWindow(parent=a)
    w.show()
    a.run()
