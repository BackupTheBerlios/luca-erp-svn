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

import logging

from zope import interface
from Modeling.EditingContext import EditingContext

from fvl.cimarron.interfaces import IStore

logger = logging.getLogger('fvl.luca')

class ITransaction(IStore):
    def track(anObject):
        """
        Adds anObject to the list of objects the transaction is
        tracking.
        """
    def forget(anObject):
        """
        Stop tracking anObject.
        """
    def search(aClass, qualifier):
        """
        Return a generator for a search.
        """

class Transaction(object):
    """
    Modeling-specific! API should settle into something agnostic.
    """
    interface.implements(ITransaction)

    def __init__(self):
        self.reset()

    def reset(self):
        self.editingContext = EditingContext()
        self.tracked = []

    def track(self, anObject):
        if anObject.editingContext() is None:
            self.editingContext.insertObject(anObject)
            self.tracked.append(anObject)
        if anObject.editingContext() is not self.editingContext:
            raise ValueError, 'object already is being tracked'

    def forget(self, anObject):
        print 'forgetting', anObject.snapshot_raw()
        if anObject.editingContext():
            self.editingContext.forgetObject(anObject)

    def search(self, aClass, **kwargs):
        qual = " and ".join([ '%s ilike "%s*"' % (attr, value or '')
                              for attr, value in kwargs.items() ])
        result = self.editingContext.fetch(aClass.__name__, qual)
        self.tracked.extend(result)
        return result

    def discard(self):
        for i in self.tracked:
            self.forget(i)
        self.reset()
    
    def save(self):
        self.editingContext.saveChanges()


# class Transaction(object):
#     def __init__(self):
#         self.tracked= []
#         self.ec = EditingContext()
        
# #     def append(self,obj):
# #         try:
# #             self.ec.insert(obj)
# #         except ValueError:
# #             pass


#     def track(self, obj):
#         self.tracked.append (obj)
    
#     def commit(self):
#         self.ec.saveChanges()

#     def rollBack(self):
#         """
#         Discards all the changes made to the model.
#         The objects associated to this Transaction will be in an
#         undefined state.
#         """
#         self.ec = EditingContext()

#     def search(self, aClass, **kw):
#         qual = " and ".join([ '%s ilike "%s*"' % (attr, value and value or '')
#                               for attr, value in kw.items() ])
#         return self.ec.fetch(aClass.__name__, qualifier=qual)