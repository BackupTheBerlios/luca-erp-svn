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
Column-related stuff.

Columns aren't really L{Controller}s, but they are designed to work
with them (and viceversa).
"""

__revision__ = int('$Rev$'[5:-1])

import logging

from fvl import cimarron
from fvl.cimarron.skins.common import XmlMixin

logger = logging.getLogger('fvl.cimarron.controllers.column')

class ColumnAwareXmlMixin(object):
    """
    A Mixin for classes that want to load columns from XML.
    """
    def fromXmlObj(cls, xmlObj, skin):
        """
        Helper function for loading a Cimarrón app from an xml file. (see
        L{Controller.fromXmlFile}).
        """
        self = cls()
        self.fromXmlObjProps(xmlObj.properties)
        attrs = {self: cls.attributesToConnect()}
        try:
            idDict = {self.id: self}
        except AttributeError:
            idDict = {}

        columns = []
        xmlObj = xmlObj.children
        while xmlObj:
            (obj, attrsInChild, idDictInChild) = \
                  self.childFromXmlObj(xmlObj, skin)
            if obj is not None:
                columns.append(obj)
                attrs.update(attrsInChild)
                # print `attrs`
                idDict.update(idDictInChild)
            xmlObj = xmlObj.next
        if columns:
            # warn (if not?)
            self.columns = columns

        return(self, attrs, idDict)
    fromXmlObj = classmethod(fromXmlObj)


class Column(XmlMixin):
    """
    A Column describes a field. This field can be used for both
    B{SearchEntry}s and B{Grid}s.
    """
    def attributesToConnect(cls):
        """
        See L{XmlMixin.attributesToConnect}
        """
        attrs = super (Column, cls).attributesToConnect()
        return attrs+['attribute']
    attributesToConnect = classmethod(attributesToConnect)

    def __init__(self, name='', attribute='', entry=None):
        """
        @param name: A text associated with the field.
            In the case of B{Grids}, it's the colunm header.
        """
#         @param read: A callable that, given an object, returns the value
#             of that object for the field. Tipically, is an unbound getter
#             method from the object class.

#         @param write: A callable that, given an object and a new value,
#             modifies the object. Tipically, is an unbound setter method
#             from the object class.

        self.name = name
        self.attribute = attribute
        if entry is None:
            entry = cimarron.skin.Entry
        self.entry = entry


