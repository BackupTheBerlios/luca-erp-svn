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
#from mx.DateTime import DateTime
from mx.DateTime import today

class ReceiptWindow(cimarron.skin.WindowController):
    def __init__(self, **kw):
        super(ReceiptWindow, self).__init__(**kw)
        self.window.title = "Receipt Generation"
        self.trans = Transaction()
        self.target=Receipt(date=today())
        self.trans.track(self.target)

        v = cimarron.skin.VBox(parent=self.window, expand=True, fill=True)
        h1 = cimarron.skin.HBox(parent=v, expand=False, fill=True)
        h2 = cimarron.skin.HBox(parent=v, expand=False, fill=False)
        v1 = cimarron.skin.VBox(parent=v)
        actionContainer = cimarron.skin.HBox(parent=v, expand=False, fill=False)

        columns = (cimarron.skin.Column(name="Name", attribute="name"),
                   cimarron.skin.Column(name="Surname", attribute="surname"))
        self.person = cimarron.skin.SearchEntry(parent=h1, cls=Person,
                                                searcher=self.trans, columns=columns,
                                                attribute="person")
        cimarron.skin.Label(parent=h2, text="Date:")
        self.date = cimarron.skin.Entry(parent=h2, attribute="date")
        
        cimarron.skin.Label(parent=h2, text="Amount:")
        self.amount = cimarron.skin.Entry(parent=h2,  attribute="amount")
        
        cimarron.skin.Label(parent=v1, text="Concept:")
        self.concept = cimarron.skin.Entry(parent=v1, attribute="concept")
        
        save = cimarron.skin.Button(parent=actionContainer, label="Save", onAction=self.save)
        discard = cimarron.skin.Button(parent=actionContainer, label="Discard", onAction=self.discard)
        self.refresh()

    
    def refresh(self):
        super(ReceiptWindow, self).refresh()
        for entry in self.person, self.amount,self.concept,self.date:
            entry.newTarget(self.value)

    def save(self, *ignore):
        self.trans.save()

    def discard(self, *ignore):
        self.trans.discard()
        self.newTarget(Receipt(date=today()))
        self.trans.track(self.target)

if __name__=='__main__':
    a = cimarron.skin.Application()
    w = ReceiptWindow(parent=a)
    w.show()
    a.run()
