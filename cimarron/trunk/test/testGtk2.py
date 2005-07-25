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

from unittest import TestCase
import pygtk
pygtk.require ('2.0')
import gtk
import gobject

from run import test_options

from fvl import cimarron
from fvl.cimarron.skins.common import Unknown, ForcedNo

from model.person import Person

from testCommon import abstractTestWidget, abstractTestVisibility
from testWindow import TestWindow
from testLabel import TestLabel
from testImage import TestImage
from testButton import TestButton, TestCheckbox
from testEntry import TestEntry, TestEntrySomeMore
from testBox import TestBoxes
from testNotebook import TestNotebook
from testGrid import TestSelectionGrid, TestGrid, TestGridInit


__all__ = ('TestGtkEntry',
           'TestEntrySomeMore',
           'TestGtkWindow',
           'TestGtkLabel',
	   'TestImage',
           'TestGtkButton',
           'TestGtkCheckbox',
           'TestGtkBoxes',
           'TestGtkNotebook',
           'TestGtkSelectionGrid',
           'TestGtkGrid',
           'TestGridInit',
           )

class testGtkParenting (abstractTestWidget):
    def testGtkParent (self):
        self.assertEqual (self.widget._widget.parent, self.parent._widget)

    def testGtkChildInChildren (self):
        self.assert_ (self.widget._widget
                      in self.parent._widget.get_children ())

class testGtkVisibility(abstractTestVisibility):
    def testGtkShow(self):
        self.app.show()
        self.widget.hide()
        self.widget.show()
        self.assert_(self.widget._widget.window is not None
                     and self.widget._widget.window.is_visible())

    def testGtkHide(self):
        self.app.show()
        self.widget.hide()
        self.assert_(self.widget._widget.window is None
                     or not self.widget._widget.window.is_visible(),
                     "calling hide on the widget didn't actually hide it")

class testGtkFocusable(TestCase):
    def setUp (self):
        super (testGtkFocusable, self).setUp ()
        self.other= cimarron.skin.Entry (parent=self.parent)
        self.widget.delegates.append (self)

    if test_options.focus_events:
        def testOnFocusIn (self):
            import gtk

            self.app.show ()
            while gtk.events_pending():
                gtk.main_iteration ()
            self.passed = 0
            self.other._widget.grab_focus ()
            while not self.other._widget.is_focus():
                gtk.main_iteration()
            self.widget._widget.grab_focus ()
            while not self.widget._widget.is_focus():
                gtk.main_iteration ()
            while not self.passed is 'in':
                gtk.main_iteration ()
            self.assertEqual(self.passed, 'in')
        def will_focus_in (self, widget):
            self.passed = 'in'
            return 0

        def testOnFocusOut (self):
            import gtk

            self.app.show ()
            while gtk.events_pending():
                gtk.main_iteration ()
            self.passed = 0
            self.widget._widget.grab_focus ()
            while not self.widget._widget.is_focus():
                gtk.main_iteration()
            while not self.passed is 'in':
                gtk.main_iteration ()
            self.other._widget.grab_focus ()
            while not self.other._widget.is_focus():
                gtk.main_iteration ()
            while not self.passed is 'out':
                gtk.main_iteration ()
            self.assertEqual(self.passed, 'out')
        def will_focus_out(self, widget):
            self.passed = 'out'
            return 0

    def testFocus (self):
        self.other._widget.grab_focus ()

        self.app.show ()
        gobject.timeout_add (100, self.doTestFocus)
        gobject.timeout_add (500, gtk.main_quit)
        self.app.run ()
        self.assert_ (self.widget._widget.is_focus ())

    def doTestFocus (self, *ignore):
        self.widget.focus ()

class TestGtkEntry(testGtkFocusable, testGtkParenting, TestEntry):
    def testSetValue (self):
        self.widget.value= 'this is a test'
        self.assertEqual (self.widget._widget.get_text(), self.widget.value)

    def testValueIsTargetWhenNoAttr (self):
        self.target= getattr (self.target, self.attribute)
        super (TestGtkEntry, self).testValueIsTargetWhenNoAttr ()

    def testEntryKnowsIfDirty(self):
        self.widget.value = 'foo'
        self.widget._widget.set_text('bar')
        self.assertEqual(self.widget.dirty(), True)

    def testEntryChangesWhenDirty(self):
        w = self.widget._widget
        self.widget.value = 'foo'
        s = w.get_style()
        clean = (s.fg, s.bg, s.text)
        w.set_text('bar')
        self.widget.dirty()
        s = w.get_style()
        dirty = (s.fg, s.bg, s.text)
        self.assertNotEqual(clean, dirty)

class TestGtkWindow(testGtkVisibility, TestWindow):
    def testWindowCanScreenshot(self):
        from tempfile import NamedTemporaryFile
        import Image
        import time
        
        f = NamedTemporaryFile(suffix='.png')
        self.window.show()
        while gtk.events_pending():
            gtk.main_iteration()
        time.sleep(1)
        while gtk.events_pending():
            gtk.main_iteration()
        self.window.screenshot(f.name)
        i = Image.open(f.name)
        self.assertEqual(i.format, 'PNG')

    def testWindowCanSetSize(self):
        self.window.size = (80, 25)
        cell = self.window._get_cell_size()
        expected = int(80*cell[0]), int(25*cell[1])
        self.assertEqual(self.window._widget.get_size(), expected)

class TestGtkLabel(testGtkParenting, TestLabel):
    def testSetLabel(self):
        self.widget.text= 'This is a label'
        self.assertEqual (self.widget.text, self.widget._widget.get_text ())

class TestGtkButton(testGtkFocusable, testGtkParenting, TestButton):
    def testSetLabel (self):
        self.widget.label= "Don't click me"
        self.assertEqual(self.widget.label, self.widget._widget.get_label ())

class TestGtkCheckbox(TestCheckbox, TestGtkButton):
    def testSetChecked(self):
        self.widget.checked = True
        self.assertEqual(self.widget._widget.get_active(), True)
        self.widget.checked = False
        self.assertEqual(self.widget._widget.get_active(), False)

class TestGtkBoxes(testGtkParenting, TestBoxes):
    pass

class TestGtkNotebook (testGtkParenting, TestNotebook):
    def testActivate (self):
        for i in xrange (10):
            other= cimarron.skin.Entry ()
            other.label= "label"+str (i)
            other.parent= self.widget
        self.app.show ()

        for i in xrange (10):
            self.widget.activate (i)
            while gtk.events_pending (): gtk.main_iteration ()
            self.assertEqual (i, self.widget._widget.get_current_page ())
            
        for i in xrange (10):
            self.widget.activate (self.widget._children[i])
            while gtk.events_pending (): gtk.main_iteration ()
            self.assertEqual (i, self.widget._widget.get_current_page ())

    def testPreventPageChange (self):
        self.testActivate ()
        self.widget.activate (0)
        self.widget.delegates.append (self)
        self.widget.activate (1)
        self.assertEqual (self.widget._widget.get_current_page (), 0)

    def will_change_page (self, *ignore):
        return ForcedNo

class TestGtkSelectionGrid (testGtkParenting, TestSelectionGrid):
    def testOnAction (self):
        event= gtk.gdk.Event (gtk.gdk.KEY_PRESS)
        event.keyval= gtk.keysyms.Return
        self.widget.onAction= self.notify

        self.widget._keyreleased (self.widget, event)
        self.assert_(self.widget in self.messages_recieved)

    def testSelect (self):
        self.setUpControl (target=None, attr=None)
        event= gtk.gdk.Event (gtk.gdk.KEY_PRESS)
        event.keyval= gtk.keysyms.Return

        for i in xrange (len (self.widget.data)):
            self.widget.index= i

            self.widget._keyreleased (self.widget, event)
            
            self.assertEqual (self.widget.value, self.widget.data[i])

class TestGtkGrid (testGtkParenting, TestGrid):
    def setUp (self):
        super (TestGtkGrid, self).setUp ()
        
    def testOnAction (self):
        # grids have no action
        pass

    def triggerNew (self):
        event= gtk.gdk.Event (gtk.gdk.KEY_PRESS)
        event.keyval= gtk.keysyms.Down
        self.widget._keyreleased (self.widget, event)

    ######################
    # tests from no-value
    def testNew (self):
        self.widget.value= None
        self.triggerNew ()

        # tests:
        # _tvdata is longer
        self.assertEqual(self.widget._tvdatalen, 1)
        # not on the value yet
        self.assert_ (self.widget.value is None)

    def testNewEditable (self):
        self.widget.value= None
        self.testNew ()
        # is editable
        self.testWrite ()

    def testNewNew (self):
        self.widget.value= None

        self.testNew ()
        self.triggerNew ()

        # tests:
        # nothing went to the value
        self.assert_ (self.widget.value is None)
        # no new obejct was created
        self.assertEqual(self.widget._tvdatalen, 1)

    def testNewEditedNew (self):
        self.widget.value= None

        self.testNewEditable ()
        self.triggerNew ()

        # tests:
        self.assertEqual(self.widget._tvdatalen, 2)
        
        # the other one got into the value
        # this should not be the behaviour
        self.assertEqual (type (self.widget.value), list)
        self.assertEqual (len (self.widget.value), 1)

    ########################
    # test from some-values
    def testSomethingNew (self):
        """
        Tests that, having some values already loaded,
        we can add more.
        """
        l= len(self.widget.value)
        self.widget.index= l-1
        self.triggerNew ()
        
        # tests:
        # right type
        # no more new attr
        # self.assertEqual (type (self.widget.new), Person)
        # the other one got into the value
        # this should not be the behaviour
        self.assertEqual (type (self.widget.value), list)
        self.assertEqual (len (self.widget.value), l)
