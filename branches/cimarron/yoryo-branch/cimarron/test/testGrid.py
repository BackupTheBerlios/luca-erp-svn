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

import unittest

from fvl import cimarron
from fvl.cimarron.skin import Column, Window, Grid, SelectionGrid, EditableGrid

from model.person import Person
from fvl.cimarron.model import Model

from testCommon import abstractTestControl

__all__ = ('TestSelectionGrid', 'TestGrid', 'TestGridInit', 'TestEditableGrid')

class DummyTarget(Model):
    def __init__(self, dummy):
        self.dummy = dummy

class TestGridInit(unittest.TestCase):
    """
    Test we can create empty Grids
    """
    def testGrid(self):
        grid = Grid()
        self.assertEqual(list(grid.columns), [])
    def testSelectionGrid(self):
        grid = SelectionGrid()
        self.assertEqual(list(grid.data), [])

class TestGrid(abstractTestControl):
    def setUp(self):
        super (TestGrid, self).setUp()
        self.list = [Person('jose', 'perez'),
                     Person('marcos', 'dione'),
                     Person('john', 'lenton'),
                     ]
        columns = (Column(name='Nombre', attribute='name'),
                   Column(name='Apellido', attribute='surname'),
                   )

        self.parent = self.window = Window(title='Test', parent=self.app)
        self.widget = self.grid = Grid(parent = self.parent,
                                       columns = columns,
                                       cls = Person,
                                       )

        target = DummyTarget(self.list)
        self.setUpControl(target=target, attr='dummy')

    def testIndex(self):
        for i in xrange (len(self.widget.value)):
            self.widget.index = i
            self.assertEqual(self.widget.index, i)
            self.assertEqual(self.value[i], self.widget.value[i])

    def testWrite(self):
        self.widget._cell_edited(None, 0, 'juan', 0)
        self.widget.index = 0
        try:
            self.assertEqual(self.widget.value[0].name, 'juan')
        except(TypeError, IndexError):
            self.assertEqual(self.widget.new.name, 'juan')

    def testValueIsTargetWhenNoAttr(self):
        self.target = self.list
        super (TestGrid, self).testValueIsTargetWhenNoAttr()

    def testOnAction (self):
        # grids have no action
        pass


class TestSelectionGrid(abstractTestControl):
    def setUp(self):
        super (TestSelectionGrid, self).setUp()
        self.list = [Person('jose', 'perez'),
                     Person('marcos', 'dione'),
                     Person('john', 'lenton'),
                     ]
        columns = (Column(name='Nombre', attribute='name'),
                   Column(name='Apellido', attribute='surname'),
                   )

        self.parent = self.window = Window(title='Test', parent=self.app)
        self.widget = self.grid = SelectionGrid(parent = self.parent,
                                                columns = columns,
                                                data = self.list,
                                                onAction=self.dummyAction,
                                                )

        target = DummyTarget(self.list[0])
        self.setUpControl(target=target, attr='dummy')

    def testIndex(self):
        for i in xrange (len(self.list)):
            self.widget.index = i
            self.assertEqual(self.list[i], self.widget.value)

    def testValue(self):
        for i in xrange (len(self.list)):
            self.widget.value = self.list[i]
            self.assertEqual(self.list[i], self.widget.value)

    def testNoValue(self):
        self.widget.data = []
        self.widget.value = None
        self.assert_(self.widget.value is None)

    def testValueIsTargetWhenNoAttr(self):
        self.setUpControl(target=self.list[0], attr=None)
        self.widget.index = 0
        super (TestSelectionGrid, self).testValueIsTargetWhenNoAttr()

    def testNoTarget(self):
        self.setUpControl(target=None, attr=None)
        self.testIndex()
        self.testValue()

    def testDoubleClickSelection(self):
        self.widget.index=1
        self.widget._double_click(widget=self.widget._concreteWidget)
        self.assertEquals(self.dummyDCValue,self.widget.data[self.widget.index],
                                    """Double click did not sent the values""") 

    def testOnAction (self):
        # grids have no action
        pass

    def dummyAction(self,sender): #action to test double click functioning
        self.dummyDCValue = sender.data[sender.index]

class TestEditableGrid(TestGrid):
    def setUp(self):
        super (TestGrid, self).setUp()
        self.list = [Person('jose', 'perez'),
                     Person('marcos', 'dione'),
                     Person('john', 'lenton'),
                     ]
        columns = (Column(name='Nombre', attribute='name'),
                   Column(name='Apellido', attribute='surname'),
                   )

        self.parent = self.window = Window(title='Test', parent=self.app)
        self.widget = self.grid = EditableGrid(parent = self.parent,
                                               columns = columns,
                                               cls = Person
                                               )

        target = DummyTarget(self.list)
        self.setUpControl(target=target, attr='dummy')

    def testMoveWithCls(self):
        self.widget.index = 0
        self.widget.indexColumn = 0
        self.widget.modoEdit = True
        self.assertEqual(self.widget.modoEdit, True)
        for x in [(i,j) for i in range(0,4) for j in range(0,2)]:
            self.assertEqual(x, (self.widget.index, self.widget.indexColumn))
            self.widget._move()
        else:
            self.assertEqual(None, self.widget.index)
            self.assertEqual(self.widget.modoEdit, False)

    def testMoveWithoutCls(self):
        self.widget.cls = None
        self.widget.index = 0
        self.widget.indexColumn = 0
        self.widget.modoEdit = True
        for x in [(i,j) for i in range(0,3) for j in range(0,2)]:
            self.assertEqual(x, (self.widget.index, self.widget.indexColumn))
            self.widget._move()
        else:
            self.assertEqual(None, self.widget.index)
            self.assertEqual(self.widget.modoEdit, False)


    def testWriteAndMove(self):
        #Estas dos lineas no van, pero la edicion no cambia el cursor...yo pense que si
        self.widget.indexColumn = 0
        self.widget.index = 2
        self.widget._cell_edited(None, 2, 'hi me dear', 0)
        self.assertEqual(self.widget.modoEdit, True)
        self.widget._move()
        self.assertEqual((2,1), (self.widget.index, self.widget.indexColumn))
        self.assertEqual(self.widget.modoEdit, True)

    def testAddRow(self):
        if self.widget._newRow():
            self.assertEqual(3, self.widget.index)
            self.assertEqual(self.widget._newRow(), False)

    def testDelRow(self):
        self.widget._delRow(0)
        try:
            self.assertEqual(self.widget.value[0].name, 'marcos')
        except(TypeError, IndexError):
            self.assertEqual(self.widget.new.name, 'marcos')

    def testDelRowCheckIndex(self):
        self.widget.index = 2
        self.widget._delRow(1)
        self.assertEqual(1, self.widget.index)
        try:
            self.assertEqual(self.widget.value[1].name, 'john')
        except(TypeError, IndexError):
            self.assertEqual(self.widget.new.name, 'john')

    def testDelRowCheckIndex(self):
        self.widget.index = 2
        self.widget._delRow(2)
        self.assertEqual(None, self.widget.index)
        try:
            self.assertEqual(self.widget.value[1].name, 'marcos')
        except(TypeError, IndexError):
            self.assertEqual(self.widget.new.name, 'marcos')
        self.widget.index = 2
        self.assertEqual(self.widget.index, None)

    def testDelAllRowAndAddRow(self):
        for i in ['jose', 'marcos', 'john']:
            self.widget._delRow(0)
        self.widget.index = 0
        self.assertEqual(None, self.widget.index)
        self.assertEqual(self.widget._newRow(), True)
        self.assertEqual(0, self.widget.index)

    def testDelegateAddRow(self):
        self.widget.delegates = [self]
        #delegate forceNo
        self.assertEqual(self.widget._newRow(), False)
        #delegate not call did_add_row()
        self.assertEqual([], [x for x in dir(self) if x == 'did_row'])
        #delegate yes.
        self.assertEqual(self.widget._newRow(), True)
        self.assertEqual(3, self.did_row)

    def testDelegateDelRow(self):
        self.widget.delegates = [self]
        #set index at last.
        self.widget.index = 2
        self.widget._delRow(2)
        #no did was call
        self.assertEqual([], [x for x in dir(self) if x == '_did_delete_row'])
        #no row was del
        self.assertEqual(2, self.widget.index)
        self.widget._delRow(2)
        self.assertEqual(2, self.will_row)
        self.assertEqual(None, self.widget.index)
        self.assertEqual(['_did_delete_row'], \
                         [x for x in dir(self) if x == '_did_delete_row'])

    def testDelegateEditRow(self):
        self.widget.delegates = [self]
        # first parameter don't use.
        self.widget._cell_edited(None, 0, 'editando', 0)
        self.assertEqual([], [x for x in dir(self) if x == 'did_row'])
        self.assertEqual(self.widget.value[0].name, 'jose')
        self.assertEqual(self.will_row, 0)
        self.assertEqual(self.will_col, 0)

        self.widget._cell_edited(None, 1, 'editando', 0)
        self.assertEqual(self.widget.value[1].name, 'editando')
        self.assertEqual(self.will_row, 1)
        self.assertEqual(self.will_col, 0)
        self.assertEqual(self.did_row, 1)
        self.assertEqual(self.did_col, 0)


    def will_edit_row_col(self, grid, row, col):
        self.assertEqual(self.widget, grid)
        self.will_row = row
        self.will_col = col
        try:
            self._will_edit_row_col
            return self._will_edit_row_col
        except AttributeError:
            self._will_edit_row_col = cimarron.skin.Yes
            return cimarron.skin.ForcedNo

    def did_edit_row_col(self, grid, row, col):
        self.assertEqual(self.widget, grid)
        self.did_row = row
        self.did_col = col

    def will_delete_row(self, grid, row):
        self.assertEqual(self.widget, grid)
        self.will_row = row
        try:
            self._will_delete_row
            return self._will_delete_row
        except AttributeError:
            self._will_delete_row = cimarron.skin.Yes
            return cimarron.skin.ForcedNo

    def did_delete_row(self, grid):
        self.assertEqual(self.widget, grid)
        self._did_delete_row = True

    def will_add_row(self, grid):
        self.assertEqual(self.widget, grid)
        try:
            self._will_add_row
            return self._will_add_row
        except AttributeError:
            self._will_add_row = cimarron.skin.Yes
            return cimarron.skin.ForcedNo

    def did_add_row(self, grid, row):
        self.assertEqual(self.widget, grid)
        self.did_row = row

