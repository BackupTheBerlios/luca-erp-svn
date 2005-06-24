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
from testCommon import abstractTestWidget

__all__=('TestImage',)

class TestImage(abstractTestWidget):
	def setUp(self):
		super(TestImage, self).setUp()
		self.parent = self.win = cimarron.skin.Window(title='Test', parent=self.app)
		self.widget = self.image = cimarron.skin.Image(aFile='./dummy.jpg',parent=self.win) #the method doesn't care if the file exists or it's an image

	def testImage(self):
		getFileResult=self.widget.imgFile 
		self.assertEqual(getFileResult, './dummy.jpg')

	def testSet_from_file(self):
		setImgResult= self.widget._set_file('testDummy.jpg')
		self.assertEqual(setImgResult, None)

	def testShow(self):
		self.win.show()
		#self.app.run()
