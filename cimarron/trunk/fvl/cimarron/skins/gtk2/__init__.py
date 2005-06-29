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

import logging
from itertools import izip, repeat

import pygtk
pygtk.require('2.0')
import gtk, gobject
from zope import interface

from fvl.cimarron.interfaces import IWindow
# clients of cimarron won't want to worry where their stuff is coming
# from
from fvl.cimarron.skins.common import *
from fvl.cimarron.controllers import *

logger = logging.getLogger('fvl.cimarron.skins.gtk2')

class GtkVisibilityMixin(object):
    """
    Mixin that lets show and hide the object.
    Used only by Window.
    """
    def _get_visible(self):
        w = self._widget.window
        return w is not None and w.is_visible()
    visible = property(_get_visible, None, None, """""")

    def show(self):
        """
        Show the object.
        """
        self._widget.show_all()

    def hide(self):
        """
        Hide the object, after delegates agrees.
        """
        if self.delegate ('will_hide'):
            self._widget.hide_all()

class GtkFocusableMixin(object):
    """
    Mixin that delegates focus in/out and makes the object
    to be focusable programatically.
    """
    def __init__ (self, **kw):
        super (GtkFocusableMixin, self).__init__ (**kw)
        self._widget.connect ('focus-in-event', self._focusIn)
        self._widget.connect ('focus-out-event', self._focusOut)

    def _focusIn (self, *ignore):
        return not self.delegate ('will_focus_in')

    def _focusOut (self, *ignore):
        return not self.delegate ('will_focus_out')

    def focus (self):
        """
        Set the focus on this object.
        """
        self._widget.grab_focus ()

class Window(GtkVisibilityMixin, Container):
    """
    A Window. Duh.
    """
    interface.implements(IWindow)
    
    def __init__(self, title='', **kw):
        """
        @param title: the title for the window.
        """
        self._widget = gtk.Window()
        super(Window, self).__init__(**kw)

        def delete_callback(*a):
            self.hide()
            return True

        self._widget.connect('delete-event', delete_callback)
        self.title = title

    def _set_title(self, title):
        self._widget.set_title(title)
    def _get_title(self):
        return self._widget.get_title()
    title = property(_get_title, _set_title, None, """The title for the window.""")


class Label(Widget):
    """
    A Label is a piece of uneditable static text.
    """
    is_dirty = False
    def __init__(self, text='', **kw):
        """
        @param text: The static test.
        """
        self._widget = gtk.Label()
        super(Label, self).__init__(**kw)
        self.text = text

    def show(self):
        self._widget.show()

    def _set_text(self, text):
        self._widget.set_text(text)
    def _get_text(self):
        return self._widget.get_text()
    text = property(_get_text, _set_text, None, """The static test.""")

class Image(Widget):
    """
    A Image is a Static Picture loaded from a file
    """
    is_dirty = False

    def __init__(self,aFile=None,**kw):
        self._widget = gtk.Image()
        super(Image,self).__init__(**kw)
        self.imgFile = self.aFile = aFile

    def show(self):
        self._widget.show()

    def _set_file(self,aFile):
        self._widget.set_from_file(aFile)

    def _get_file(self):
        return self.aFile

    imgFile = property(_get_file, _set_file, None, """The static test.""")
	
		

class Button(GtkFocusableMixin, Control):
    """
    A Button is a Control that can be pressed, and when it does,
    it fires the action.
    """
    is_dirty = False

    def __init__(self, label='', **kw):
        """
        @param label: text that is shown in the middle of the button.
        """
        if not '_widget' in self.__dict__:
            self._widget = gtk.Button()
        super(Button, self).__init__(**kw)
        self.label = label
        self._widget.connect('clicked', self._activate)

    def _set_label(self, label):
        self._widget.set_label(label)
    def _get_label(self):
        return self._widget.get_label()
    label = property(_get_label, _set_label, None,
                     """See the C{label} parameter for the constructor.""")

    def skelargs(self):
        skelargs = super(Button, self).skelargs()
        skelargs['label'] = self.label
        return skelargs

class Checkbox(Button):
    """
    A Control that represents a boolean value.
    """
    def __init__(self, checked=False, **kw):
        self._widget = gtk.CheckButton()
        super(Checkbox, self).__init__(**kw)
        self.checked = checked
    def _get_checked(self):
        return self._widget.get_active()
    def _set_checked(self, checked):
        self._widget.set_active(checked)
    checked = property(_get_checked, _set_checked)

class Entry(GtkFocusableMixin, Control):
    """
    The simplest text input control.
    """
    def __init__(self, **kw):
        self._widget = gtk.Entry ()
        super(Entry, self).__init__(**kw)
        self.refresh ()
        self._widget.connect ('activate', self._activate)
        self._widget.connect ('key-release-event', self._keyreleased)
        self.delegates.append (self)

    def _get_value (self):
        return self.__value
    def _set_value (self, value):
        self.__value = value
        self._gtkCommit()
    value= property (_get_value, _set_value, None, """""")

    def _gtkCommit(self):
        value = self.value
        if value is None:
            value = ''
        self._widget.set_text(value)

    def refresh (self):
        """
        Show the value on the control.
        """
        super(Entry, self).refresh()
        self._gtkCommit()

    def will_focus_out (self, *ignore):
        """
        Called when the focus goes out the Entry.
        Copies the shown value to the value property.
        Do not call directly.
        """
        # is not the same as _activate ()
        self.value= self._widget.get_text ()
        return Unknown

    def _activate(self, widget=None):
        """
        Called when <Enter> is hit. 
        Copies the shown value to the value property.
        Do not call directly.
        """
        if widget is None:
            widget = self._widget
        self.value = widget.get_text()
        super(Entry, self)._activate()

    def _keyreleased (self, widget, key_event):
        """
        Called whenever a key is hit.
        If that key is <Esc>, undo the edition.
        Do not call directly.
        """
        if key_event.keyval == gtk.keysyms.Escape:
            # esc; `reset' the value
            self.refresh()
            widget.select_region(0,-1)
        self.is_dirty

    def _is_dirty(self):
        is_dirty = self.value != self._widget.get_text()
        if is_dirty:
            self._widget.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('red'))
        else:
            self._widget.modify_bg(gtk.STATE_NORMAL, None)
        return is_dirty
    is_dirty = property(_is_dirty)

class VBox(Container):
    """
    A vertical container. The children of this object
    will be placed one on top of the other.
    """
    def __init__ (self, **kw):
        self._widget = gtk.VBox()
        # self._widget.set_border_width (5)
        self._widget.set_spacing (5)
        super (VBox, self).__init__ (**kw)

class HBox(Container):
    """
    A horizontal container. The children of this object
    will be placed from left to right.
    """
    def __init__ (self, **kw):
        self._widget = gtk.HBox()
        # self._widget.set_border_width (5)
        self._widget.set_spacing (5)
        super (HBox, self).__init__ (**kw)

class Notebook (Container):
    """
    A container where all the children are put in `tabs´ and
    only one of them is shown at any given time.
    """
    def __init__ (self, **kw):
        self._widget = gtk.Notebook ()
        super (Notebook, self).__init__ (**kw)
        self._widget.connect ('change-current-page', self.__change_page)

    def activate (self, other):
        """
        Show a particular tab.

        @param other: either the child to show or
            the index of the child.
        """
        if type (other)==int:
            # assume it's the page no
            pageNo= other
        else:
            # assume it's a child
            pageNo= self._children.index (other)
        if 0<=pageNo and pageNo<len (self._children) and self.delegate ('will_change_page'):
            self._widget.set_current_page (pageNo)

    def concreteParenter (self, child):
        super (Notebook, self).concreteParenter (child)
        if getattr (child, '_widget', None):
            label= gtk.Label()
            label.set_text (child.label)
            self._widget.set_tab_label (child._widget, label)

    def __change_page (self, *ignore):
        """
        Makes that page switching
        """
        ans= False
        if self.delegate ('will_change_page'):
            ans= True
        return ans


# shouldn't it be just a Control?
import traceback
class Grid (ColumnAwareXmlMixin, Controller):
    """
    Grids are used for editing a list of objects.
    """
    def __init__ (self, columns=[], klass=None, **kw):
        """
        @param columns: a list of B{Column}s that describe
            what to show in the grid, how obtain it from the
            objects, and eventually how to save data back to.
        """
        self._widget= self._tv= gtk.TreeView ()
        # self.mainWidget= self
        self.columns= columns

        self.klass= klass

        # put the TreeView in a scrolled window
        self._widget= gtk.ScrolledWindow ()
        self._widget.set_policy(gtk.POLICY_NEVER, gtk.POLICY_ALWAYS)
        self._widget.add (self._tv)

        self._tv.connect ('key-release-event', self._keyreleased)

        super (Grid, self).__init__ (**kw)
        # this was not done because it was initializing
        # is this still true?
        self.refresh ()

    def attributesToConnect (klass):
        return ['klass']+super (Grid, klass).attributesToConnect ()
    attributesToConnect= classmethod (attributesToConnect)

    def _set_columns (self, columns):
        self._columns= columns
        if columns!=[]:
            # build the tv columns and the data types tuple
            (self._tvcolumns, self._dataspec)= izip(*izip(
                [ gtk.TreeViewColumn (c.name) for c in columns ],
                repeat(str)
                ))

            # add the columns and attrs
            for i in xrange (len (columns)):
                c= self._tvcolumns[i]
                crt= gtk.CellRendererText ()
                # editable
                crt.set_property ('editable', True)
                crt.connect ('edited', self._cell_edited, i)
                c.pack_start (crt, True)
                c.add_attribute (crt, 'text', i)
                self._tv.append_column (c)
    def _get_columns (self):
        return self._columns
    columns= property (_get_columns, _set_columns)
        
    def _set_index (self, index):
        if index is not None:
            self._tv.set_cursor ((index, ))
    def _get_index (self):
        try:
            return int (self._tv.get_cursor ()[0][0])
        except TypeError:
            # None is unsubscriptable, the cursor is not set
            return None
    index= property (_get_index, _set_index, None,
                     """The index of the object currently selected.
                     If no object is selected, it is None.""")

    def _cell_edited (self, cell, path, text, colNo, *ignore):
        write= self.columns[colNo].write
        # modify the ListStore model...
        self._tvdata[path][colNo]= text
        # ... and our model
        try:
            write (self.value[int (path)], text)
        except (TypeError, IndexError):
            # we're editing the new value
            write (self.new, text)
            
        # coming soon: our models will (should) suport the generic TreeModel protocol
        # also: if write() returns false, the entry flashes and
        # a) rollbacks the value or
        # b) leaves it with wrong value, so the user can edit it (preferred)
        return False
    def _keyreleased (self, widget, key_event, *ignore):
        last= self.value is None or len (self.value)==0 or self.index==len (self.value)-1
        # print `self.value`, `self._tv.get_cursor ()`, last

        if key_event.keyval==gtk.keysyms.Down and last:
            try:
                if self.new.isDirty:
                    if self.value is None:
                        self.value= [self.new]
                    else:
                        self.value.append (self.new)
                    self.new= self.klass ()
                    self._tvdata.append ([j.read (self.new) for j in self.columns])
            except AttributeError:
                # print 'self.new does not exist. so, go create it'
                self.new= self.klass ()
                self._tvdata.append ([j.read (self.new) for j in self.columns])
            
        return False

    def refresh (self):
        super(Grid, self).refresh()
        if len (self.columns)>0:
            self._tvdata= gtk.ListStore (*self._dataspec)
        else:
            self._tvdata= gtk.ListStore (str)
        # print 'Grid.refresh:', `self.value`, self.columns
        if self.value is not None:
            for i in self.value:
                # add all the values
                # NOTE: this forces the data to be read.
                data= [j.read (i) for j in self.columns]
                # print 'Grid: adding', data
                self._tvdata.append (data)
            self.index= 0
        else:
            self.index= None
        self._tv.set_model (self._tvdata)


class SelectionGrid (ColumnAwareXmlMixin, Controller):
    """
    SelectionGrids are used for showing a list of objects,
    and for selecting one among those.
    """
    def __init__ (self, data=[], columns=[], **kw):
        """
        @param data: the list of objects to be shown.

        @param columns: a list of B{Column}s that describe
            what to show in the grid, how obtain it from the
            objects, and eventually how to save data back to.
        """
        self._tv= gtk.TreeView ()

        self._columns= columns
        # build the tv columns and the data types tuple
        (self._tvcolumns, self._dataspec)= izip(*izip(
            [ gtk.TreeViewColumn (c.name) for c in columns ],
            repeat(str)
            ))
        self.data= data

        # put the TreeView in a scrolled window
        self._widget= gtk.ScrolledWindow ()
        self._widget.set_policy(gtk.POLICY_NEVER, gtk.POLICY_ALWAYS)
        self._widget.add (self._tv)

        # add the columns and attrs
        for i in xrange (len (columns)):
            c= self._tvcolumns[i]
            crt= gtk.CellRendererText ()
            c.pack_start (crt, True)
            c.add_attribute (crt, 'text', i)
            self._tv.append_column (c)

        self._tv.connect ('key-release-event', self._keyreleased)
        self._tv.connect ('cursor_changed', self._cursor_changed)

        super (SelectionGrid, self).__init__ (**kw)

    def _keyreleased (self, widget, key_event, *ignore):
        if key_event.keyval==gtk.keysyms.Return:
            self.onAction ()
            return True
        return False

    def _set_data (self, data):
        # the model data
        self._data= data

        if len (self._columns)>0:
            self._tvdata= gtk.ListStore (*self._dataspec)
        if data is not None:
            for i in data:
                # build a ListStore w/ al the values
                # NOTE: this forces the data to be read.
                self._tvdata.append ([j.read (i) for j in self._columns])
        self._tv.set_model (self._tvdata)
    def _get_data (self):
        return self._data
    data= property (_get_data, _set_data, None,
                    """The list of objects to be shown.""")

    def _cursor_changed (self, *ignore):
        self.__index= int (self._tv.get_cursor ()[0][0])
    def _set_index (self, index):
        if index is not None:
            self._tv.set_cursor (index)
        self.__index= index
    def _get_index (self):
        return self.__index
    index= property (_get_index, _set_index, None,
                     """The index of the object currently selected.
                     If no object is selected, it is None.""")

    def _set_value (self, value):
        try:
            index= self.data.index (value)
        except (ValueError, AttributeError):
            #   the value is not present
            #               data might be None?
            index= None
            # what about building a new item?
        self.index= index
        # super (SelectionGrid, self)._set_value (value)
        # print '-> value:', value, 'index:', index
        
    def _get_value (self):
        ans= None
        if self.index is not None:
            ans= self.data[self.index]
        # print '<- value:', ans, 'index:', self.index
        return ans
    value= property (_get_value, _set_value, None,
                     """The selected object. If no object is selected, it is None.""")


def _run():
    gtk.main()

def _quit():
    if gtk.main_level():
        gtk.main_quit()

def _schedule(timeout, callback, repeat=False):
    def cb():
        gobject.timeout_add(timeout, callback)
        if repeat:
            cb()
    cb()

def concreteParenter(parent, child):
    """
    Does the skin-specific magic that `glues' a child with its parent.
    Do not call directly.
    """
    if '_widget' in child.__dict__:
        # print 'parenting', parent, child,
        if '_widget' in parent.__dict__:
            # print 'concreted'
            parent._widget.add(child._widget)
        else:
            if parent.parent is None:
                # print 'postponed'
                try:
                    parent._childrenToParent.append (child)
                except AttributeError:
                    parent._childrenToParent= [child]
            else:
                # print 'forwarded to', parent.parent
                parent.parent.concreteParenter (child)

from zope.interface import moduleProvides
from fvl.cimarron.interfaces import ISkin
moduleProvides(ISkin)
