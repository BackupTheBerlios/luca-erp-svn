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

# this implementation of Model is tightly tied to Modeling
# http://modeling.sf.net/

import os
import logging

from Modeling import ModelSet, Model, dynamic
from Modeling.CustomObject import CustomObject
from Modeling.utils import capitalizeFirstLetter

from fvl.cimarron.model import Model as CimarronModel
from fvl.luca.transaction import Transaction

logger = logging.getLogger('fvl.luca.model')
# logger.setLevel(logging.DEBUG)

model_name = os.getenv('LUCA_PYMODEL',
                       os.path.join(os.path.dirname(__file__),
                                    'pymodel_luca.py' ))
try:
    model = Model.loadModel(model_name)
except ImportError:
    logger.critical("I couldn't load the pymodel from file %r."
                    " Please read INSTALL.txt" % model_name)
    raise
del model_name
ModelSet.defaultModelSet().addModel(model)


class ModelingList(object):
    def __init__(self, value=None, relatesTo=None,
                 append=None, remove=None, inverse=None):
        # print 'one of these', append, remove, inverse
        self.value = value
        self.appendMethod = append
        self.removeMethod = remove
        self.relatesTo = relatesTo
        self.inverse = inverse

    def append(self, other):
        getattr(self.relatesTo, self.appendMethod)(other)
        setattr(other, self.inverse, self.relatesTo)
    def remove(self, other):
        getattr(self.relatesTo, self.removeMethod)(other)
        setattr(other, self.inverse, None)

    def __len__(self):
        return len(self.value)

    def __getitem__(self, index):
        return self.value[index]
    def __setitem__(self, index, item):
        self.value[index] = item


# HACK!!
# we mess around with the internals of Modeling.dynamic here.
orig_setters_code = dynamic.setters_code
def setters_code(prop):
    rv = orig_setters_code(prop)
    if 'type' in prop.__class__.__dict__:
        # if it has a type, rv is a list of a single 2-uple
        (fname, code), = rv
        aType = prop.type()
        if aType == 'DateTime':
            aType = 'DateTimeFrom'
        code = code[:-3] + aType + '(obj)'
        rv = [(fname, code)]
    return rv
dynamic.setters_code = setters_code
from mx.DateTime import DateTimeFrom
dynamic.DateTimeFrom = DateTimeFrom
del DateTimeFrom
dynamic.ModelingList = ModelingList

orig_getter_code = dynamic.getter_code
def getter_code(prop):
    rv = orig_getter_code(prop)
    fname, code = rv
    if hasattr(prop, 'isToMany') and prop.isToMany():
        # we wrap it up in a ModelingList
        pos = code.find('return ') + len('return ')
        propName = capitalizeFirstLetter(prop.name())
        addFname = "addTo"+propName
        remFname = "removeFrom"+propName
        inv = prop.inverseRelationship()
        inverseName = inv._name
        
        code = "%sModelingList(%s, self, '%s', '%s', '%s')" % \
               (code[:pos], code[pos:], addFname, remFname, inverseName)
        logger.debug(code)
    if 'type' in prop.__class__.__dict__:
        pos = code.find('return ') + len('return ')
        if prop.type in ('string', ):
            # convert anything reminiscent of string to unicode
            code = '%sunicode(%s)' % (code[:pos], code[pos:])
    return fname, code
dynamic.getter_code = getter_code
# end HACK

class LucaMeta(type):
    def __new__(cls, className, bases, namespace):
        # print className, bases
        entity = model.entityNamed(className)
        if entity is None:
            raise RuntimeError, 'BUG!'
        # print className, namespace
        dynamic.define_init(entity, className, namespace)
        dynamic.define_getters(entity, className, namespace)
        dynamic.define_setters(entity, className, namespace)
        dynamic.define_properties(entity, className, namespace)
        # print className, namespace
        return super(LucaMeta, cls).__new__(cls, className, bases, namespace)

class LucaModel(CimarronModel):
    def entityName(cls):
        return cls.__name__
    entityName = classmethod(entityName)

    def values(cls, transaction, **kwargs):
        return transaction.search(cls, **kwargs)
    values = classmethod(values)
    def valuesFor(cls, transaction, attribute):
        # hmm, how to?
        return []
    valuesFor = classmethod(valuesFor)

# now the idea is that, for every class in the model you create a
# class, and add methods to it if necessary. E.g,
#   class Person(LucaModel, CustomObject):
#       __metaclass__ = LucaMeta
#       pass

# since this would be tedious and error-prone, just define the classes
# you actually need below, and we'll automatically generate the rest
# (below).
# be sure to ad the classes *below* this line

# aye, sir!
class Printer(LucaModel, CustomObject):
    __metaclass__ = LucaMeta
    def __init__ (self, transaction=None, **kwargs):
        super(Printer, self).__init__(**kwargs)
        documentTypes = transaction.search(DocumentType)
        for dt in documentTypes:
            dn = DocumentNumber(documentType=dt, number='00001')
            self.documentNumbers.append(dn)

from mx.DateTime import now
class PointOfSale(LucaModel, CustomObject):
    __metaclass__ = LucaMeta
    def __init__(self, **kwargs):
        super(PointOfSale, self).__init__(**kwargs)

    def open(self, amount, transaction):
        doc = DrawerOpen(pointOfSale=self, amount=amount, dateTime=now())
        transaction.track(doc)

    def moveIn(self, amount, category, account, transaction):
        movement = Movement(pointOfSale=self, amount=amount, category=category,
                            account=account, dateTime=now())
        transaction.track(movement)

class Money(LucaModel):
    def __init__(self, amount=0.0, currency=None):
        self.amount = amount
        if not currency:
            self.currency = Currency()
        else:
            self.currency = currency

    def __add__(self, other):
        if self.currency != other.currency:
            raise TypeError #some error for the moment
        resultCurrency = self.currency
        aResult = Money(amount=self.amount + other.amount,
                        currency=resultCurrency)
        return aResult

    def __sub__(self, other):
        if self.currency != other.currency:
            raise TypeError #some error for the moment
        resultCurrency = self.currency
        aResult = Money(amount=self.amount - other.amount,
                        currency=resultCurrency)
        return aResult

    def __div__(self, divisor):
        """
        Division of money will return a list of each value, this may
        not make much sense when all the values are the same, but when
        the result is not exact whe need to make one of the shares
        bigger (in accounting it's not allowed to round)
        """
        import decimal
        Context = decimal.Context
        partialResult = Context(prec=3,
                                rounding='ROUND_DOWN').create_decimal(self.amount/divisor)
        aResult = []
        if partialResult * divisor == self.amount:
            for i in range(divisor):
                aResult.append(Money(amount=partialResult,
                                     currency=self.currency))
        else:
            biggerPortion = Money(amount=partialResult + self.amount - \
                                  partialResult * divisor,
                                  currency=self.currency)
            aResult.append(biggerPortion)
            for i in range(divisor-1):
                aResult.append(Money(amount=partialResult,
                                     currency=self.currency))
        return aResult
    
# just be sure to add the classes *above* this line
namespace = globals()
for className in model.entitiesNames():
    if className not in namespace:
        namespace[className] = LucaMeta(className,
        # add superclasses here --------------------vvvvv
                                        (LucaModel, CustomObject), {})
