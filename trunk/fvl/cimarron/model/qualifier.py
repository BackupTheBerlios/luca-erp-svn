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

import logging
from mx.DateTime import DateTimeType

logger = logging.getLogger('fvl.cimarron.model.qualifier')

class Qualified(object):
    def __init__(self, value=''):
        self.value = value
    def __repr__(self):
        return str(self.value)
    def and_(self, other):
        return self.binop(other, 'and')
    __and__ = and_
    def or_(self, other):
        return self.binop(other, 'or')
    __or__ = or_
    def like(self, other):
        return self.binop(other, "ilike")
    __xor__ = like
    def less(self, other):
        return self.binop(other, '<')
    __lt__ = less
    def greater(self, other):
        return self.binop(other, '>')
    __gt__ = greater
    def lessOrEqual(self, other):
        return self.binop(other, '<=')
    __le__ = lessOrEqual
    def greaterOrEqual(self, other):
        return self.binop(other, '>=')
    __ge__ = greaterOrEqual
    def equal(self, other):
        return self.binop(other, '==')
    __eq__ = equal
    def notEqual(self, other):
        return self.binop(other, '!=')
    __ne__ = notEqual
    def binop(self, other, op):
        return Qualified("(%r) %s (%s)" % (self, op, self.quote(other)))
    def quote_string(cls, string):
        assert '"' not in string, \
               "Qualified.quote can't quote strings with quotes (fix it!)"
        return '"%s"' % string
    quote_string = classmethod(quote_string)
    def quote_mxdatetime(cls, mxdatetime):
        return cls.quote_string(str(mxdatetime))
    quote_mxdatetime = classmethod(quote_mxdatetime)
    def quote(cls, other):
        for cls, qtr in ((basestring, cls.quote_string),
                         (DateTimeType, cls.quote_mxdatetime)):
            if isinstance(other, cls):
                break
        else:
            qtr = repr
        return qtr(other)
    quote = classmethod(quote)

class Qualifier(Qualified):
    def binop(self, other, op):
        return Qualified("%r %s %s" % (self, op, self.quote(other)))
    def __getattr__(self, attr):
        if self.value:
            attr = "%s.%s" % (self.value, attr)
        return Qualifier(attr)

nullQualifier = Qualified()
