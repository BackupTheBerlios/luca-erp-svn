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
from fvl.cimarron.model.qualifier import Qualifier

from fvl.luca.model import Invoice, AlienInvoice, CustomerAccount, \
     MovementAccount, Person, Client, Provider, PointOfSaleOpening,\
     PointOfSaleClosure
from fvl.luca.transaction import Transaction

import re

from mx.DateTime import now

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
        ModelDict(name='Apertura de Caja', type='X', cls=PointOfSaleOpening,
                  other=None),
        ModelDict(name='Cierre de Caja', type='X', cls=PointOfSaleClosure,
                  other=None),
# ASK MARIANA!!!
#         ModelDict(name='Ticket Externo', type=None, cls=AlienInvoice,
#                   other=Provider),
#         ModelDict(name='Comprobante Externo', type=None, cls=AlienInvoice,
#                   other=Provider),
        )
    def search(cls, ignoreClass, qualifier):
        # '' or 'name == "thing"'
        qual = repr(qualifier)
        
        if qual!='':
            # *HACKY* *WHACKY*
            result = re.compile('==.*\"([^\"]*)\"').search(qual)
            # +*HACKY* +*WHACKY*
            if result:
                qual = result.group(1)
        return [docType for docType in cls.__values__
                if qual.upper() in docType['name'].upper()]
    search = classmethod(search)

class LoadPettyCashEntry(WindowController):
    def __init__(self, **kwargs):
        super(LoadPettyCashEntry, self).__init__(**kwargs)
        self.trans = Transaction()
        self.pos ,= self.trans.search('PointOfSale')
        self.buildUI()
        
    def buildUI(self):
        self.window.title = 'Caja chica - Carga'
        v = VBox(parent=self.window)


        f0 = Frame(parent=v, label='Cuenta')
        h0 = HBox(parent=f0)
        right0 = VBox(parent=h0)
        columns= (Column(name='Nombre', attribute='name',
                         operator=Qualifier.like),)
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
                  Column(name='Nombre', attribute='name',
                         operator=Qualifier.like),)
        self.category = SearchEntry(parent=right1, columns=columns,
                                    searcher=self.trans, cls=MovementAccount)


        f2 = Frame(parent=v, label='Comprobante')
        h2 = HBox(parent=f2)
        left2 = VBox(parent=h2)
        right2 = VBox(parent=h2)

        Label(parent=left2, text='Tipo')
        columns= (Column(name='Nombre', attribute='name',
                         operator=Qualifier.like),)
        self.docType = SearchEntry(parent=right2, columns=columns,
                                   searcher=DocumentType,
                                   onAction=self.setThirdLabel)

        Label(parent=left2, text='Numero')
        self.docNumber = Entry(parent=right2)

        Label(parent=left2, text='Fecha')
        self.docDate = Entry(parent=right2, emptyValue=now())
        self.docDate.commitValue(self.docDate.value)

        self.thirdLabel = Label(parent=left2)
        columns= (Column(name='Apellido', attribute='person.surname',
                         operator=Qualifier.like),)
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
        Button(parent=h4, label='Descartar', onAction=self.discard)

    def setThirdLabel(self, *ignore):
        if self.docType.value:
            if self.docType.value['other']:
                self.thirdLabel.text = self.docType.value['other'].__name__
                self.otherParty.cls = self.docType.value['other']
                self.otherParty.enable()
            else:
                self.thirdLabel.text = "Documento interno"
    

    def save(self, *ignore):
        # build a document of the right kind
        # cls = self.docType.value['cls']
        # document = cls(amount=self.amount.value, number=self.docNumber.value,
        #                type=self.docType.value['type'], )
        # set the other side
        # document.setattr(self.docType.value['attr'], self.provider.value)
        cls = self.docType.value['cls']
        document = cls(number=self.docNumber.value,
                       type=self.docType.value['type'],
                       detail=self.description.value,
                       amount=self.amount.value,
                       actualDate=self.docDate.value)
        self.trans.track(document)
        document.pettyRegister(self.pos,
                               self.otherParty.value,
                               self.category.value,
                               self.account.value)
        # register w/ the trans!
        # save it
        self.trans.save()

    def discard(self, *ignore):
        self.trans.discard()
        for i in self.__dict__:
            if isinstance(self.__dict__[i],Entry) or isinstance(self.__dict__[i],SearchEntry):
                if hasattr(self.__dict__[i],'emptyValue'):
                    self.__dict__[i].commitValue(self.__dict__[i].emptyValue)
                else:
                    self.__dict__[i].commitValue(None)
                    self.__dict__[i].refresh()

        #this is made apart beacause is not generic, thirdLabel is the only
        #label in self that changes and otherParty is the only widget Disabled
        self.thirdLabel.text = ''
        self.otherParty.disable()
        

if __name__=='__main__':
    a = Application()
    w = LoadPettyCashEntry(parent=a)
    w.show()
    a.run()
