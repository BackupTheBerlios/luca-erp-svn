# -*- python -*- coding: latin1 -*-
#
# Copyright 2003,2004 Fundación Vía Libre
#
# This file is part of ruff.
#
# ruff is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# ruff is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PAPO; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

_formulas = {'pageno': 0,
             'numpages': 5}

def set_numpages(numpages):
    _formulas['numpages'] = numpages

def set_pageno(pageno):
    _formulas['pageno'] = pageno

class Compute (object):

    def __init__(self, parent, expr, watch):
        self.expr = expr
        self.watch = watch
        self.parent = parent

    def __str__(self):
        return str(_formulas.get(self.expr, self.expr))
