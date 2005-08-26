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
#
from fvl import cimarron
from fvl.luca.model import Client, MovementAccount
from fvl.luca.model.document import Receipt
from fvl.luca.transaction import Transaction
from fvl.cimarron.model.qualifier import Qualifier
from mx.DateTime import today, now

from fvl.cimarron.skin import WindowController, VBox, HBox, Label, \
     SearchEntry, Column, Frame, Button, Entry, Application, MultiLine

class ReceiptGui(WindowController):
    def __init__(self, **kwargs):
        super(ReceiptGui, self).__init__(**kwargs)
        self.trans = Transaction()
        self.pos ,= self.trans.search('PointOfSale')
        self.buildUI()

    def buildUI(self):
        self.window.title = 'Generacion de Recibo'

        v1 = VBox(parent=self.window, expand=True, fill=True)
        h0 = HBox(parent=v1, expand=False, fill=True)
        v0left = VBox(parent=h0, expand=False, fill=True)
        v0right = VBox(parent=h0, expand=False, fill=True)
        v2 = VBox(parent=v1)
        actionContainer = HBox(parent=v1, expand=False, fill=True)

        Label(parent=v0left, text='Cuenta Contable:')
        columns= (Column(name='Cod', attribute='code'),
                  Column(name='Nombre', attribute='name',
                         operator=Qualifier.like),)
        self.category = SearchEntry(parent=v0right, columns=columns,
                                    searcher=self.trans, cls=MovementAccount)

        Label(parent=v0left, text='Cliente:')
        columns = (Column(name='Nombre', attribute='person.name',
                          operator=Qualifier.like),
                   Column(name='Apellido', attribute='person.surname',
                          operator=Qualifier.like),)
        self.otherParty = SearchEntry(parent=v0right, cls=Client,
                                      searcher=self.trans,
                                      columns=columns)


        Label(parent=v0left, text='Numero:')
        self.docNumber = Entry(parent=v0right)

        Label(parent=v0left, text='Fecha:')
        self.actualDate = Entry(parent=v0right,emptyValue=now())
        self.actualDate.commitValue(self.actualDate.value)

        Label(parent=v0left, text='Monto:')
        self.amount = Entry(parent=v0right)
        
        Label(parent=v2, text='Concepto:', expand=False, fill=False)
        self.concept = MultiLine(parent=v2)
        
        save = Button(parent=actionContainer, label='Guardar',
                      onAction=self.save)

        discard = Button(parent=actionContainer, label='Descartar',
                         onAction=self.discard)


    def save(self, *ignore):
        receipt = Receipt(number=self.docNumber.value,
                          type='X',
                          detail=self.concept.value,
                          amount=self.amount.value,
                          actualDate=self.actualDate.value)
        self.trans.track(receipt)
        #we use pettyRegister beacause we store the same data that pettyCash
        #doing a receipt
        receipt.pettyRegister(self.pos,
                              self.otherParty.value,
                              self.category.value, None)
                             # self.account.value) this goes instead
                             #of the above none, do we wand this data?
        self.trans.save()

    def discard(self, *ignore):
        self.trans.discard()
        

        

if __name__=='__main__':
    a = cimarron.skin.Application()
    #w = ReceiptWindow(parent=a)
    w = ReceiptGui(parent=a)
    w.show()
    a.run()
