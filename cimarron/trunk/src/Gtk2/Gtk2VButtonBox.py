# -*- python -*- coding: ISO-8859-1 -*-
# Copyright 2004 Fundacion Via Libre
#
# This file is part of PAPO.
# 
# PAPO is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# PAPO is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with PAPO; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import gtk
from Generic.VButtonBox import VButtonBox
from Gtk2ButtonBox import Gtk2ButtonBox

class Gtk2VButtonBox(VButtonBox,Gtk2ButtonBox):
    def __init__(self, **kw):
        if not hasattr(self,'_obj'):
            self._obj = gtk.VButtonBox()
        super(Gtk2VButtonBox, self).__init__(**kw)

