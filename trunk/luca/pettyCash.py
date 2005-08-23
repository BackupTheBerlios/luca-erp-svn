# -*- coding: utf-8 -*-
#
# Copyright 2003, 2004, 2005 Fundación Via Libre
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

from fvl import cimarron
from fvl.cimarron.skin import WindowController, VBox, HBox, Label, \
     SearchEntry, Column, Frame, Button, Entry, Application

from fvl.luca.model import Invoice, AlienInvoice, PettyCash, CustomerAccount, \
     MovementAccount, Person, Client, Provider
from fvl.luca.transaction import Transaction

import re

class ModelDict(dict):
    def getattr(self, attr):
        return self[attr]
    def setattr(self, attr, value):
        self[attr] = value

class DocumentType(object):
    __values__ = (
        ModelDict(name='Factura A', type='A', cls=Invoice, other=Client),
        ModelDict(name='Factura B', type='B', cls=Invoice, other=Client),
        ModelDict(name='Factura C', type='C', cls=Invoice, other=Client),
        ModelDict(name='Factura Externa A', type='A', cls=AlienInvoice,
                  other=Provider),
        ModelDict(name='Factura Externa B', type='B', cls=AlienInvoice,
                  other=Provider),
        ModelDict(name='Factura Externa C', type='C', cls=AlienInvoice,
                  other=Provider),
        ModelDict(name='Ticket Externo', type=None, cls=AlienInvoice,
                  other=Provider),
        ModelDict(name='Comprobante Externo', type=None, cls=AlienInvoice,
                  other=Provider),
        )
    def search(cls, ignoreClass, qualifier):
        # '' or 'name == "thing"'
        qual = repr(qualifier)
        
        if qual!='':
            # *HACKY* *WHACKY*
            qual = re.compile('==.*\"([^\"]*)\"').search(qual).group(1)
        return [docType for docType in cls.__values__
                if qual in docType['name']]
    search = classmethod(search)

class LoadPettyCashEntry(WindowController):
    def __init__(self, **kwargs):
        super(LoadPettyCashEntry, self).__init__(**kwargs)
        self.trans = Transaction()
        self.pettyCash = PettyCash
        self.buildUI()
        
    def buildUI(self):
        self.window.title = 'Caja chica - Carga'
        v = VBox(parent=self.window)


        f0 = Frame(parent=v, label='Cuenta')
        h0 = HBox(parent=f0)
        right0 = VBox(parent=h0)
        columns= (Column(name='Nombre', attribute='name'),)
        self.account = SearchEntry(parent=right0, columns=columns,
                                   searcher=self.trans, cls=CustomerAccount)


        f1 = Frame(parent=v, label='Operacion')
        h1 = HBox(parent=f1)
        left1 = VBox(parent=h1)
        right1 = VBox(parent=h1)

        # Label(parent=left1, text='Fecha')
        # fecha = Entry(parent=right1)
        
        Label(parent=left1, text='Categoria')
        columns= (Column(name='Cod', attribute='code'),
                  Column(name='Nombre', attribute='name'),)
        self.category = SearchEntry(parent=right1, columns=columns,
                                   searcher=self.trans, cls=MovementAccount)


        f2 = Frame(parent=v, label='Comprobante')
        h2 = HBox(parent=f2)
        left2 = VBox(parent=h2)
        right2 = VBox(parent=h2)

        Label(parent=left2, text='Tipo')
        columns= (Column(name='Nombre', attribute='name'),)
        self.docType = SearchEntry(parent=right2, columns=columns,
                                   searcher=DocumentType,
                                   onAction=self.setThirdLabel)

        Label(parent=left2, text='Numero')
        self.docNumber = Entry(parent=right2)

        Label(parent=left2, text='Fecha')
        self.docDate = Entry(parent=right2)

        self.thirdLabel = Label(parent=left2)
        columns= (Column(name='Apellido', attribute='person.surname'),)
        self.otherParty = SearchEntry(parent=right2, columns=columns,
                                      searcher=self.trans)
        self.otherParty.disable()


        # f3 = Frame(parent=v, label='Montos')
        h3 = HBox(parent=v)

        # Label(parent=h3, text='Ingreso')
        # self.moneyIn = Entry(parent=h3)

        # Label(parent=h3, text='Egreso')
        # self.moneyOut = Entry(parent=h3)

        Label(parent=h3, text='Monto')
        self.amount = Entry(parent=h3)

        Label(parent=h3, text='Descripcion')
        self.description = Entry(parent=h3)


        h4 = HBox(parent=v)
        Button(parent=h4, label='Guardar', onAction=self.save)
        Button(parent=h4, label='Descartar')

    def setThirdLabel(self, *ignore):
        if self.docType.value:
            self.thirdLabel.text = self.docType.value['other'].__name__
            self.otherParty.cls = self.docType.value['other']
            self.otherParty.enable()
    

    def save(self, *ignore):
        # build a document of the right kind
        # cls = self.docType.value['cls']
        # document = cls(amount=self.amount.value, number=self.docNumber.value,
        #                type=self.docType.value['type'], )
        # set the other side
        # document.setattr(self.docType.value['attr'], self.provider.value)
        self.pettyCash.registerDocument(self.docType.value['cls'],
                                        self.docNumber.value,
                                        self.docType.value['type'],
                                        self.description.value,
                                        self.amount.value, self.docDate.value,
                                        self.otherParty.value,
                                        self.category.value, self.account.value)
        # register w/ the trans!
        # save it
        self.trans.save()
        

if __name__=='__main__':
    a = Application()
    w = LoadPettyCashEntry(parent=a)
    w.show()
    a.run()
