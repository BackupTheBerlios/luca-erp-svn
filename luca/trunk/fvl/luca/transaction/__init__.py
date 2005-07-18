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

from zope import interface
from Modeling.EditingContext import EditingContext

class ITransaction(interface.Interface):
    def commit():
        """
        Saves the transaction to its parent transaction if there is
        one; otherwise, to permanent storage.
        """
    def rollback():
        """
        Discards changes performed in the transaction.
        """
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
    def __init__(self):
        self.tracked= []
        self.ec = EditingContext()
        
#     def append(self,obj):
#         try:
#             self.ec.insert(obj)
#         except ValueError:
#             pass


    def track(self, obj):
        self.tracked.append (obj)
    
    def commit(self):
        self.ec.saveChanges()

    def rollBack(self):
        """
        Discards all the changes made to the model.
        The objects associated to this Transaction will be in an
        undefined state.
        """
        self.ec = EditingContext()

    def search(self, aClass, **kw):
        qual = " and ".join([ '%s ilike "%s*"' % (attr, value and value or '')
                              for attr, value in kw.items() ])
        return self.ec.fetch(aClass.__name__, qualifier=qual)
