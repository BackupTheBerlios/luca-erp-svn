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
L{Search}es and related junk.
"""

__revision__ = int('$Rev$'[5:-1])

import logging
import gtk

from fvl.cimarron.controllers.base import Controller, WindowController
from fvl.cimarron.controllers.column import ColumnAwareXmlMixin
from fvl.cimarron.skins.common import No as DelegateNo

logger = logging.getLogger('fvl.cimarron.controllers.search')
# logger.setLevel(logging.DEBUG)

class SelectionWindow(WindowController):
    """
    Not public. Please Ignore :)
    """
    def __init__(self, columns=None, **kwargs):
        from fvl.cimarron import skin
        
        if columns is None:
            columns = []
        super(SelectionWindow, self).__init__(parent=self.parent,
                                              title='Select', size=(30, 5),
                                              **kwargs)
        vbox = skin.VBox(parent=self.window)
        self.grid = skin.SelectionGrid(parent=vbox, columns=columns,
                                       onAction=self.onOk)
        hbox = skin.HBox(parent=vbox, expand=False)
        self.ok = skin.Button(parent=hbox, label='Ok',
                              onAction=self.onOk)
        self.cancel = skin.Button(parent=hbox, label='Cancel',
                                  onAction=self.onCancel)

    def onOk(self, *ignore):
        """
        onAction for 'Ok' button.
        """
        self.value = self.grid.value
        self.hide()
        self.onAction()

    def onCancel(self, *ignore):
        """
        onAction for 'Cancel' button
        """
        self.value = None
        self.hide()
        self.onAction()

    def refresh(self):
        self.grid.refresh()

class Search(ColumnAwareXmlMixin, Controller):
    """
    Abstract class for searching. Consist of a widget
    with one Entry for each Column.

    The method C{search()} must be
    implemented in the subclass, which sould take one parameter
    for each column and return the list of objects found to that
    search criteria.

    This class already handles the case when the amount of objets
    found is greater that one. In that case, it presents a window
    where the user can select from a list.

    When one object is found or selected, it calls the action.
    """
    def attributesToConnect(cls):
        """
        See L{XmlMixin.attributesToConnect
        <fvl.cimarron.skins.common.XmlMixin.attributesToConnect>}
        """
        attrs = super (Search, cls).attributesToConnect()
        return attrs+['searcher']
    attributesToConnect = classmethod(attributesToConnect)
    
    def __init__(self, columns=None, cls=None, searcher=None, **kwargs):
        """
        @param columns: A list of Columns. Only the C{read} attribute
            needs to be set.

        @param searcher: an object that knows the values() for the right type of
            objects. Typically a Store.

        @param cls: The class that we'll want to look for with C{searcher}.
        """
        from fvl.cimarron.skin import HBox

        super(Search, self).__init__(**kwargs)
        self.entries = []
        # self.h = HBox(parent=self, expand=False)
        self.h = HBox(expand=False)
        self._outerWidget = self.h._outerWidget
        self.columns = columns
        self.value = None
        self.searcher = searcher
        self.cls = cls

    def _set_columns(self, columns):
        logger.debug (`columns`)
        if columns is not None:
            from fvl.cimarron.skin import Label, Button
            for column in columns:
                # build label and entry
                Label(text=column.name+":", parent=self.h)
                entryConstr = column.entry
                entry = entryConstr(parent=self.h, onAction=self.search)
                entry.delegates.append (self)
                # if columns are added at creation it willset the first entry
                # as the _concreteWidget, else it will be the button
                if '_concreteWidget' not in self.__dict__:
                    self._concreteWidget = entry
                self.entries.append(entry)

            # search button
            b = Button(parent=self.h, label='Search!', onAction=self.search)
            if '_concreteWidget' not in self.__dict__:
                self._concreteWidget = b
            
            # the widget that fires the action.
            self.mainWidget = b
        self.__columns = columns
    def _get_columns(self):
        return self.__columns
    columns = property(_get_columns, _set_columns)

    def doSearch(self, *ignore):
        """
        Performs the abstract search. The result ends up in aSearch.value as a
        list and returns the length of the list.
        """
        self.window.disable()
        try:
            data = {}
            for i in xrange(len(self.columns)):
                e = self.entries[i]
                c = self.columns[i]
                if e.value != '':
                    # '' means `don't filter by me'
                    data[c.attribute] = e.value
                else:
                    data[c.attribute] = None

            logger.debug ('searching %r, %r', self.searcher, data)
            self.value = self.searcher.search(self.cls, **data)
        finally:
            self.window.enable()
        return len(self.value)
    def search (self, *ignore):
        """
        Performs the search and fires the action thereupon.
        """
        ans = self.doSearch()
        self.onAction()
        return ans

    # def will_focus_out(self, *ignore):
    #     return DelegateNo

class SearchEntry(Search):
    _cellDataType = object
    # now we can only specify one column
    # _cellDataType = gobject.TYPE_STRING
    def _setupCell(cls, grid, dataColumn, viewColumn, index, readOnly=False):
        logger.debug('setting up cell '+`dataColumn`)
        def cellData(tvcolumn, cell, model, iter):
            data = cell.user_data
            (index, attr) = data
            obj = model.get_value(iter, index)
            if obj is not None:
                value = obj.getattr(attr)
            else:
                # the search gave `nothing found`
                value = ''
            logger.debug(value)
            cell.set_property('text', value)
        # we build a SearchEntry here so it can really search
        # it takes the params from the dataColumn :: Column (haskell notation)
        self = cls(cls=dataColumn.cls, columns=dataColumn.columns,
                   searcher=dataColumn.searcher)

        def search(cell, path, newVal, colNo, *ignore):
            # This function is launched when the user edits a cell.
            index = grid.index
            for renderer in self.entries:
                # fake the values for the `entries`
                if renderer == cell:
                    renderer.value = newVal
                    logger.debug('cell %d, %s' % (index, newVal))
                else:
                    obj = getattr(grid.value[index], dataColumn.attribute)
                    if obj is not None:
                        value = obj.getattr(renderer.column.attribute)
                    else:
                        value = None
                    logger.debug('get %d, %s' % (index, value))
                    renderer.value = value

            # setup the action so it updates the grid
            # when none or one is found/selected
            self.onAction= lambda *ignore: selectedValue(cell, path, colNo,
                                                         *ignore)
            # do the actual search
            self.search()

        def selectedValue(cell, path, colNo, *ignore):
            logger.debug(self.value)
            # update the grid
            grid._cell_edited(cell, path, self.value, colNo)
            
        self.entries = []
        for c in self.columns:
            # c.entry._setupCell()
            renderer = gtk.CellRendererText()

            if not (readOnly or dataColumn.readOnly):
                renderer.set_property('editable', True)
                renderer.connect('edited', search, index)

            renderer.column = c
            self.entries.append(renderer)
            renderer.user_data = (index, c.attribute)
            viewColumn.pack_start(renderer, True)
            # you can't set the cell_data_func unless is already packed
            viewColumn.set_cell_data_func(renderer, cellData)
    _setupCell = classmethod(_setupCell)

    def _set_columns(self, columns):
        logger.debug (`columns`)
        super(SearchEntry,self)._set_columns(columns)
        if columns is not None:
            # build the selection window here because:
            # a) we can't build it w/o columns (well, we *could*,
            # but then we'll need more API just for this case) and
            # b) we must change the columns in the SelectionWindow
            # when new Columns are supplied.
            self.selwin= SelectionWindow (columns= columns,
                                          onAction= self.selected,)
    def _get_columns(self):
        return super(SearchEntry, self)._get_columns()
    columns= property (_get_columns, _set_columns)
        
    def search (self, *ignore):
        """
        Performs the search, and handles the case
        when more than one object is found.
        """
        self.doSearch()

        ans = self.value
        if len(ans)==0:
            self.commitValue(None)
        elif len(ans)==1:
            self.commitValue(ans[0])
            self.refresh()
        if len(ans)>1:
            # too much information, select one please.
            self.selwin.grid.data = ans
            # this `comes back` in selected() (see below).
            self.selwin.show()
        else:
            logger.debug('here!')
            self.onAction()
        # logger.debug(`self.value`)
        return len(ans)

    def selected(self, *ignore):
        """
        Callback for the selection window when finally
        one object is selected.
        """
        self.commitValue(self.selwin.value)
        self.refresh()
        self.selwin.hide()
        logger.debug('here!')
        self.onAction()
        # logger.debug(`self.value`)

    def refresh(self):
        """
        Show the value.
        """
        logger.debug(`self.value`)
        super(SearchEntry, self).refresh()
        logger.debug(`self.value`)
        entries = self.entries
        try:
            self.value.getattr
        except AttributeError:
            for index, entry in enumerate(self.entries):
                entry.value = None
        else:
            for index, entry in enumerate(self.entries):
                entry.value = self.target.getattr(self.columns[index].attribute)
