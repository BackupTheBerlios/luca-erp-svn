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
from fvl.luca.model import Person, Receipt
from fvl.luca.transaction import Transaction

class ReceiptWindow(cimarron.skin.WindowController):
    def __init__(self, **kw):
        super(ReceiptWindow, self).__init__(**kw)
        self.win.title = "Receipt Generation"
        self.trans = Transaction()
        self.commitValue(Receipt())

        v = cimarron.skin.VBox(parent=self.win)
        h1 = cimarron.skin.HBox(parent=v)
        h2 = cimarron.skin.HBox(parent=v)

        columns = (cimarron.skin.Column(name="Name", attribute="name"),
                   cimarron.skin.Column(name="surname", attribute="surname"))
        self.person = cimarron.skin.SearchEntry(parent=h1, searcher=Person,
                                                transaction=self.trans, columns=columns,
                                                attribute="person")
        self.amount = cimarron.skin.Entry(parent=h1,  attribute="amount")
        self.concept = cimarron.skin.Entry(parent=h2, attribute="concept")
        self.date = cimarron.skin.Entry(parent=h2, attribute="date")
        
        self.refresh()
    
    def refresh(self):
        super(ReceiptWindow, self).refresh()
        for entry in ("person", "amount", "concept", "date"):
            getattr(self, entry).newTarget(self.value)

if __name__=='__main__':
    a = cimarron.skin.Application()
    w = ReceiptWindow(parent=a)
    w.show()
    a.run()
