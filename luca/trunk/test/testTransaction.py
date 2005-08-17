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

import unittest
import os

from fvl.luca.transaction import Transaction
from Modeling import Model, ModelSet, dynamic
from Modeling.EditingContext import EditingContext

dn = os.path.dirname(__file__)
model_file = 'test/tr_pymodel_test.py'

model=Model.loadModel(model_file)
ModelSet.defaultModelSet().addModel(model)
dynamic.build_with_metaclass(model, define_properties=1)

database_file = model._connectionDictionary['database']

from Tester.aProduct import aProduct

class TestTransaction(unittest.TestCase):
    def setUp(self):
        self.tr = Transaction()
        self.other_tr = Transaction()

class TestsThatRequireNoDatabase(TestTransaction):
    def testNothing(self):
        """
        This is here just to test the setUp.

        If this fails or errors, look there.
        """

    def testTrack(self):
        """
        Try to create an object, specifying the transaction against
        which you're working.
        """
        p = aProduct()
        self.tr.track(p)
        self.assertEqual(len(self.tr.tracked), 1)

    def testMultipleTrack(self):
        """
        Try to create several objects, specifying the transaction against
        which you're working.
        """
        p=[]
        for i in xrange(10):
            p.append(aProduct())
        self.tr.track(*p)
        self.assertEqual(len(self.tr.tracked), 10)

    def testDoubleTrackFails(self):
        """
        If you try tracking an object in two different transactions,
        you'll find that you can't.
        """
        p = aProduct()
        self.tr.track(p)
        self.assertRaises(ValueError, self.other_tr.track, p)

    def testDoubleTrackSameTranOk(self):
        """
        However, if you try tracking an object twice on the same
        transaction, you're ok.
        """
        p = aProduct()
        self.tr.track(p)
        self.tr.track(p)
        self.assertEqual(len(self.tr.tracked), 1)

class TestWithDatabase(TestTransaction):
    def setUp(self):
        os.system('cp -f tr_cache.db ' + database_file)
        super(TestWithDatabase, self).setUp()
        self.tr.track(aProduct(name='one'))

class TestInsertOne(TestWithDatabase):
    def testWorked(self):
        """
        Even before save, the current transaction should be able to
        find an object it's tracking.
        """
        self.assertEqual(len(self.tr.search(aProduct)), 1)

    def testOtherTransaction(self):
        """
        However, the other transactions should *not* see the objects
        created but not yet saveed.
        """
        self.assertEqual(len(self.other_tr.search(aProduct)), 0)

    def testDiscard(self):
        """
        After a discard, things should go back to normal.
        """
        self.tr.discard()
        self.assertEqual(len(self.tr.search(aProduct)), 0)

    def testSave(self):
        """
        After a save, the transaction should still be able to find
        the objects :)
        """
        self.tr.save()
        self.assertEqual(len(self.tr.search(aProduct)), 1)

    def testSaveOtherTransaction(self):
        """
        After a save, the other transactions should be able to find
        the objects inserted.
        """
        self.tr.save()
        self.assertEqual(len(self.other_tr.search(aProduct)), 1)

class TestEditOne(TestWithDatabase):
    def setUp(self):
        super(TestEditOne, self).setUp()
        self.tr.save()
        self.tr.reset()

    def testFindit(self):
        """
        Silly check to ensure we're finding the thing we're wanting to
        find.
        """
        p ,= self.tr.search(aProduct)
        self.assertEqual(p.name, 'one')

    def testVisibleFromOwnTransaction(self):
        """
        Load the product from the database, edit it: if you look for
        it again with the same transaction, you should see the edit
        """
        p ,= self.tr.search(aProduct)
        p.name = 'two'
        p ,= self.tr.search(aProduct)
        self.assertEqual(p.name, 'two')

    def testInvisibleFromOtherTransactionsBeforeSave(self):
        """
        Load the product from the database, edit it: if you look for
        it again with a different transaction, you should *not* see
        the edit
        """
        p ,= self.tr.search(aProduct)
        p.name = 'two'
        p ,= self.other_tr.search(aProduct)
        self.assertEqual(p.name, 'one')

    def testInvisibleFromOwnTransactionAfterDiscard(self):
        """
        Load the product from the database, edit it, discard: if you
        look for it again with the same transaction, you should *not*
        see the edit
        """
        p ,= self.tr.search(aProduct)
        p.name = 'two'
        self.tr.discard()
        p ,= self.tr.search(aProduct)
        self.assertEqual(p.name, 'one')

    def testVisibleFromOtherTransactionsAfterSave(self):
        """
        Load the product from the database, edit it, save: if you
        look for it again with a different transaction, you should see
        the edit
        """
        p ,= self.tr.search(aProduct)
        p.name = 'two'
        self.tr.save()
        p ,= self.other_tr.search(aProduct)
        self.assertEqual(p.name, 'two')

    def testOverwriting(self):
        """
        Load the product from the database, edit it, save: if you
        look for it again with a different transaction, you should see
        the edit
        """
        p1 ,= self.tr.search(aProduct);
        p1.name = 'two'
        p2 ,= self.other_tr.search(aProduct);
        p2.name = 'three'
        self.tr.save();
        self.other_tr.save()

        t = Transaction()
        p ,= t.search(aProduct)
        self.assertEqual(p.name, p2.name)

if __name__ == '__main__':
    import gtk
    while gtk.events_pending():
        gtk.main_iteration()
    unittest.main()
