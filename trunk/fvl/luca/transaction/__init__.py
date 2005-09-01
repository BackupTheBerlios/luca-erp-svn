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

import logging
import weakref

from zope import interface
from Modeling.EditingContext import EditingContext

from fvl.cimarron.interfaces import IStore
from fvl.cimarron.model.qualifier import Qualifier, nullQualifier

logger = logging.getLogger('fvl.luca.transaction')
# logger.setLevel(logging.DEBUG)

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

    def track(self, *objects):
        for anObject in objects:
            if anObject.editingContext() is None:
                self.editingContext.insertObject(anObject)
                self.tracked.append(anObject)
            if anObject.editingContext() is not self.editingContext:
                raise ValueError, 'object already is being tracked'
            if anObject.transaction() is None:
                anObject.transaction = weakref.ref(self)

    def forget(self, anObject):
        if anObject.editingContext():
            self.editingContext.forgetObject(anObject)

    def search(self, aClass, qual=nullQualifier):
        try:
            name = aClass.__name__
        except AttributeError:
            # pray it's a string
            name = aClass
        logger.debug (name+": "+qual.value)
        result = self.editingContext.fetch(name, qual.value)
        for i in result:
            self.track(i)
        print 'ok', result
        return result

    def discard(self):
        for i in self.tracked:
            self.forget(i)
        self.reset()
    
    def save(self):
        self.editingContext.saveChanges()
