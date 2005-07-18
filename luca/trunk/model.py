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

"""
FIXME: this file must go.

This file has not been garbage collected because some ideas still
referr to it. Please update your ideas.
"""
__revision__ = int('$Rev: 200 $'[5:-1])

from Modeling.EditingContext import EditingContext

from fvl.cimarron.model import Model as CimarronModel

class autoproperty(type):
    def __new__(cls, name, bases, attrDict):
        """
        Builds properties using the methods 'get<st>', 'set<st>'
        for every attribute 'validate<st>'. it's very tied to Modeling.
        """
        properties = []
        for key in attrDict:
            if key.startswith('validate'):
                properties.append(key[8:])
        theClass = super(autoproperty, cls).__new__(cls, name, bases, attrDict)
        for prop in properties:
            setattr(theClass, prop[0].lower() + prop[1:],
                    property(getattr(theClass, 'get' + prop),
                             getattr(theClass, 'set' + prop)))
        return theClass
            
class Model(CimarronModel):
    __metaclass__ = autoproperty

    def __init__(self, store=None):
        self.store = store

    def values(cls, trans, qualifier):
        return trans.search(cls, qualifier)
    values = classmethod(values)

    def record(self):
        self.store.add(self)

    def delete(self):
        raise UndeletableClassError, \
              "You can't delete %r instances" % self.__class__.__name__

class DeletableModel(Model):
    def delete(self):
        self.store.delete(self)

from zope import interface
class pseudoIModel(interface.Interface):
    def getattr(attr):
        pass
    def setattr(attr, val):
        pass
    def values(qual):
        pass
    def valuesFor(attr, qual):
        pass

