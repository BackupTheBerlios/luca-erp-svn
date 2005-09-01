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

"""
Several widgets that are L{Container}s.
"""

__revision__ = int('$Rev$'[5:-1])

import logging
logger = logging.getLogger('fvl.cimarron.skins.gtk2.container')

import gtk

from fvl.cimarron.skins.common import Container
from fvl.cimarron.skins.gtk2.mixin import GtkDisableMixin

class Gtk2Container(Container, GtkDisableMixin):
    """
    stuff specific to all Gtk2 containers
    """
    pass

class VBox(Gtk2Container):
    """
    A vertical container. The children of this object
    will be placed one on top of the other.
    """
    def __init__ (self, **kwargs):
        if '_concreteWidget' not in self.__dict__:
            self._innerWidget = self._outerWidget = \
                                self._concreteWidget = gtk.VBox()
        # self._concreteWidget.set_border_width (5)
        self._concreteWidget.set_spacing (5)
        super(VBox, self).__init__(**kwargs)

class HBox(Gtk2Container):
    """
    A horizontal container. The children of this object
    will be placed from left to right.
    """
    def __init__ (self, **kwargs):
        if '_concreteWidget' not in self.__dict__:
            self._innerWidget = self._outerWidget = \
                                self._concreteWidget = gtk.HBox()
        self._concreteWidget.set_spacing(5)
        super(HBox, self).__init__(**kwargs)

class Notebook (Gtk2Container):
    """
    A container where all the children are put in `tabs´ and
    only one of them is shown at any given time.
    """
    def __init__ (self, **kwargs):
        if '_concreteWidget' not in self.__dict__:
            self._innerWidget = self._outerWidget = \
                                self._concreteWidget = gtk.Notebook()
        super(Notebook, self).__init__(**kwargs)
        self._concreteWidget.connect('change-current-page', self.__change_page)

    def activate (self, other):
        """
        Show a particular tab.

        @param other: either the child to show or
            the index of the child.
        """
        if type (other)==int:
            # assume it's the page number
            pageNo = other
        else:
            # assume it's a child
            pageNo = self._children.index(other)
        if 0 <= pageNo and pageNo < len(self._children) \
               and self.delegate('will_change_page'):
            self._concreteWidget.set_current_page(pageNo)

    def _concreteParenter (self, child):
        """
        See L{fvl.cimarron.skins.gtk2._concreteParenter}
        """
        super(Notebook, self)._concreteParenter(child)
        if getattr(child, '_concreteWidget', None):
            label = gtk.Label()
            label.set_text(child.label)
            self._innerWidget.set_tab_label(child._outerWidget, label)

    def __change_page (self, *ignore):
        """
        Makes that page switching
        """
        return self.delegate('will_change_page')

class Frame(Gtk2Container):
    def __init__(self, label='', **kwargs):
        if '_concreteWidget' not in self.__dict__:
            self._innerWidget = self._outerWidget = \
                                self._concreteWidget = gtk.Frame()
        super(Frame, self).__init__(**kwargs)
        self.label = label

    def _set_label(self, label):
        self._concreteWidget.set_label(label)
    def _get_label(self):
        return self._concreteWidget.get_label()
    label = property(_get_label, _set_label)

class Table(Gtk2Container):
    def __init__(self, rows=1,columns=1, homogeneous=False,**kwargs):

        self.rows = rows 
        self.columns = columns 

        if '_concreteWidget' not in self.__dict__:
            self._innerWidget = \
            self._outerWidget = \
            self._concreteWidget = gtk.Table(rows=self.rows,
                                             columns=self.columns,
                                             homogeneous=homogeneous)
        super(Table,self).__init__(**kwargs)

    def addItem(self, child, column=0, row=0, horLenght=1, verLenght=1, xpadding=0, ypadding=0):
        """
        The gtk Table requires as parameters to add widgets the 'borders'
        of the table that will be his limits, as an example to add an
        Entry in the first cell of a 2x2 table we must give to the table
        as parameters left and top limits as 0, and, bottom and right as 1.
        We ask here instead the lenght and then calculte the left and bottom
        limits
        """

        rightLimit = column + horLenght
        #this checks if the lenght of the cells isn't outside the table
        if rightLimit > self.columns:
            rightLimit = self.columns

        bottomLimit = row + verLenght
        if bottomLimit > self.rows:
            bottomLimit = self.rows
        
        self._innerWidget.attach(child=child._outerWidget, 
                                 left_attach=column,
                                 right_attach=rightLimit,
                                 top_attach=row,
                                 bottom_attach=bottomLimit,
                                 xpadding=xpadding,
                                 ypadding=ypadding) 


    def resize(self, rows=None, columns=None):
        """
        Once shown the widget the resize won't be noticeable neither the newly
        added widgets but, anyway, this may be useful to someone so it stays
        """
        if not rows:
            rows = self.rows
        if not columns:
            columns = self.columns
        self.rows = rows
        self.columns = columns
        self._concreteWidget.resize(rows=rows,columns=columns)
        
