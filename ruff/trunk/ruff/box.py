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

from UserList import UserList
from errors import *

__all__ = ("Box",)

Left = -1
Right = 1
Center = 0

class Box(list):
    def __init__(self, *args, **kw):
        for i in ('parent', 'line', 'column', 'width', 'height', 'align', 'vfill', 'raw', 'wrap', 'style'):
            setattr(self, i, kw[i])
        self.encoder = self.parent.encoder
        self.caps = self.parent.root.caps
        self(*args)

    def reset(self):
        self.data = []

    def __call__(self, *vals):
        self.reset()
        if hasattr(self.parent, 'add_fields'):
            self.parent.add_fields(*vals)
        self.extend(vals)

    def render(self, container_height=0):
        s = "".join(map(str, self))
        if self.encoder and not self.raw:
            # self.encoder devuelve una dupla (string convertido,
            # bytes consumidos). Si hubo error de conversión, los
            # bytes consumidos son menos que la longitud del string
            # original.
            (t, m) = self.encoder(s)
            if m != len(s):
                raise "uh?"
            else:
                s=t
        if self.width:
            if len(s) > self.width:
                if self.wrap:
                    r,s=s,[]
                    while r:
                        if len(r) < self.width:
                            n=len(r)
                        else:
                            n=r.rfind(" ", 1, self.width)
                        if n==-1:
                            n=self.width
                        s.append(r[:n])
                        r=r[n:]
                else:
                    s = [s[:self.width]]
            else:
                s=[s]
            s = [getattr(i, ("center", "rjust", "ljust")[self.align])(self.width)
                 for i in s]
            if self.height:
                if len(s) < self.height:
                    s.extend([' '*self.width for i in xrange(self.height-len(s))])
                else:
                    s=s[:self.height]
        else:
            s=[s]
        if container_height and self.vfill:
            s = (s*container_height)[:container_height]
        #i=self.caps.start(self.style)
        #o=self.caps.end(self.style)
        #return [i+j+o for j in s]
        return s

if __name__ == '__main__':
    d=Box('hola', 'que', 'tal', 'los chicos bien la familia bien',
          parent=None, line=0, column=0, width=20, height=3, align=Left, vfill=0, raw=0, wrap=1)
    for i in d.render():
        print '|%s| (%d)' % (i, len(i))

