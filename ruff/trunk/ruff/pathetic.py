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

from box import Box
from canvas import Canvas
from errors import *

class Pathetic (object):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        if parent is not None:
            self.fqdn = parent.fqdn + name + '/'
            self.root = parent.root
            self.encoder = parent.encoder
            #if self.root.dict.get(self.fqdn) is not None:
            #    raise DuplicateFQDN, self.fqdn
            self.root.dict[self.fqdn] = self

class Field(Pathetic):
    def __init__(self, parent, name, default=None):
        self.default = default
        self.value = None
        Pathetic.__init__(self, parent, name)

    def __str__(self):
        if self.value is not None:
            return str(self.value)
        elif self.default is not None:
            return str(self.default)
        else:
            raise UnboundFieldError, "Attempted to render unbound field '%s'" % self.name

class Shelf(Pathetic):
    def __init__(self, parent, name,
                 height=0):
        Pathetic.__init__(self, parent, name)
        self.height = height
        self.canvas = Canvas(height)
        self.fields = {}
        self.boxes = []

    def add_box(self, *args, **kw):
        for k, v in {'line': 0, 'column': 0, 'width': 0, 'height': 0,
                     'align': -1, 'vfill': 0, 'raw': 0, 'wrap': 0}.items():
            kw.setdefault(k, v)
        kw['parent'] = self
        box = Box(*args, **kw)
        self.boxes.append(box)
        self.canvas(box)
        return box

    def add_fields(self, *maybefields):
        for i in maybefields:
            if isinstance(i, Field):
                self.fields[i.name] = i

    def render(self, **kw):
        self.canvas.height = self.height
        self(**kw)
        return self.canvas.render()

    def __call__(self, **kw):
        for k, v in kw.items():
            try:
                self.fields[k].value = v
            except KeyError, msg:
                raise UnknownFieldError, msg


#     def guess_height(self):
#         h = self.height
#         if not h:
#             for i in self.boxes:
#                 if i.height:
#                     h = max(h, i.height + i.line)
#         return h

class Dentry(Shelf):
    def __call__(self, **kw):
        for k, v in self.fields.items():
            if kw.has_key(k):
                v.value = kw[k]
                del kw[k]
            else:
                if v.default is None:
                    raise UnboundFieldError, "field %s isn't bound and has no default" % k
                v.value = v.default
        for k in kw.keys():
            raise UnknownFieldError, "field %s is unknown" % k

class Detail(Pathetic):
    def __init__(self, parent, name,
                 height=0):
        Pathetic.__init__(self, parent, name)
        self.height = height

    def add_dentry(self, name, height=0):
        return Dentry(self, name, height)

    def add_detail(self, name, height=0):
        return Detail(self, name, height)

class Template(Detail):
    def __init__(self,
                 max_height=0, max_num_pages=0, height=0, encoder=None):
        self.fqdn = '/'
        self.root = self
        self.dict = {'/': self}
        Detail.__init__(self, None, '/', height)
        if height and not max_height:
            max_height = height
        elif max_height and height:
            raise InvalidTemplateError, \
                  "you can't specify height and max_height simultaneously"
        self.max_height = max_height
        self.max_num_pages = max_num_pages
        self.encoder = encoder

if __name__=='__main__':
    r=Template()
    h=r.add_dentry('header')
    h.add_box('Planilla de Caja Diaria', column=0, width=10)
    h.add_box('[ sin fecha ]', column=48, align=1, width=32)
    for i in h.render():
        print "%4d !%s!" % (len(i), i)


    #d1=r.add_dentry('item')
    #d1.add_box(Field(d1, 'moneda'), column=1, width=32, wrap=1, align=-1)
    #d1.add_box('|', column=32, vfill=1)
    #d1.add_box(Field(d1, 'contado'), column=33, width=11, align=1)
    #d1.add_box('|', column=44, vfill=1)
    #d1.add_box(Field(d1, 'ctacte'), column=45, width=11, align=1)
    #d1.add_box('|', column=56, vfill=1)
    #d1.add_box(Field(d1, 'otros'), column=57, width=11, align=1)
    #d1.add_box('|', column=68, vfill=1)
    #d1.add_box(Field(d1, 'total'), column=69, width=11, align=1)
    #for i in d1.render(moneda='Morlacks with cochinillas arábigas', contado=100, ctacte=850, otros=50, total=1000):
    #    print "!%s!" % i
