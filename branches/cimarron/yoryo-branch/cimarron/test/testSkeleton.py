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
import libxml2

import fvl.cimarron
from fvl.cimarron import skin

__all__ = ('TestSkeleton',)

class TestSkeleton(unittest.TestCase):
    def setUp(self):
        self.app = skin.Application()
        self.window = skin.Window(parent=self.app)
        self.vbox = skin.VBox(parent=self.window)
        self.button = skin.Button(parent=self.vbox,
                                  label='click my clicker',
                                  value=5)
        self.entry = skin.Entry(parent=self.vbox)

    def testLeafSkeleton(self):
        skel = self.button.skeleton()
        self.assertEqual(skel.serialize(), 
                         '<Button value="5" label="\'click my clicker\'"/>')

    def testInteriorNodeSkeleton(self):
        skel = self.vbox.skeleton()
        self.assertEqual(skel.serialize(),
                         '<VBox>'
                           '<Button value="5" label="\'click my clicker\'"/>'
                           '<Entry value="None"/>'
                         '</VBox>')

    def testWindowSkeleton(self):
        skel = self.window.skeleton()
        self.assertEqual(skel.serialize(),
                         '<Window>'
                           '<VBox>'
                             '<Button value="5" label="\'click my clicker\'"/>'
                             '<Entry value="None"/>'
                           '</VBox>'
                         '</Window>')

    def testAppSkeleton(self):
        skel = self.app.skeleton()
        self.assertEqual(skel.serialize(),
                         '<Application value="None">'
                           '<Window>'
                             '<VBox>'
                               '<Button value="5" label="\'click my clicker\'"/>'
                               '<Entry value="None"/>'
                             '</VBox>'
                           '</Window>'
                         '</Application>')

    def testRoundTrip(self):
        sk = self.app.skeleton()
        app = skin.Application.fromXmlObj(sk.doc.children, skin)[0]
        self.assertEqual(app.skeleton().serialize(), sk.serialize())

    def testSkipSpaces (self):
        xmlRaw= """<Application>
  <Window>
    <VBox>
      <Button value="5" label="'click my clicker'"/>
    </VBox>
  </Window>
</Application>"""
        xmlObj= libxml2.parseMemory (xmlRaw, len (xmlRaw))
        app = skin.Application.fromXmlObj(xmlObj.children, skin)
