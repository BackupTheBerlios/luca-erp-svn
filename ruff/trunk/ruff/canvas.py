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

from UserDict import UserDict
#from UserString import UserString
#import re

__all__ = ("Canvas",)

class Canvas(dict):
    def __init__(self, height, *args):
        self.height = height
        self.reset()
        self(*args)

    def __call__(self, *args):
        #self.reset()
        for i in args:
            self[i.column,i.line] = i

    def reset(self):
        """
        Remove all boxes from the canvas
        """
        self.data = {}

    def clear(self):
        """
        Reset all boxes in the canvas
        """
        for i in self.data.values():
            i.reset()

    def render(self, **kw):
        """
        Boil it down to a rectangular list of strings
        """
        keys = self.keys()
        if keys==[]:
            return []
        X = max([key[0] for key in keys])
        if not self.height:
            Y = max([key[1] for key in keys])+1
        else:
            Y = self.height
        a = [' '*X for j in xrange(Y)]
        deferred = {}
        for x in xrange(X+1):
            curr = []
            for y in xrange(len(a)):
                if self.has_key((x, y)):
                    if self[x,y].vfill:
                        deferred[x,y] = self[(x,y)]
                    else:
                        curr = self[x,y].render(len(a))
                        a[y] = a[y][:x] + ' '*(x-len(a[y][:x])) + curr.pop(0)
                elif curr:
                    a[y] += ' '*(x-len(a[y]))
                    a[y] = a[y][:x] + curr.pop(0)
            if curr and not self.height:
                a.extend([' '*x + i for i in curr])
        for (x, y), v in deferred.items():
            r = v.render(len(a))
            for i in xrange(len(r)):
                a[y+i] = a[y+i][:x] + ' '*(x-len(a[y+i][:x])) + r[i] + a[y+i][x+len(r[i]):]

        w = max([len(i) for i in a])
        return [i.ljust(w) for i in a]

if __name__ == '__main__':
    from box import *
    c=Canvas(0)
    b1 = Box(parent=c, line=0, column=0, width=10, height=0, align=-1, vfill=0, raw=0, wrap=0)
    b2 = Box(parent=c, line=0, column=48, width=32, height=0, align=1, vfill=0, raw=0, wrap=0)
    c(b1, b2)
    b1('Planilla de Caja Diaria')
    b2('[ sin fecha ]')

    r = c.render()
    for i in r:
        print "%5d: |%s|" % (len(i), i)
    print "total:", len(r)
