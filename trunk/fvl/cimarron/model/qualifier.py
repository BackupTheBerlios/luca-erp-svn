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

logger = logging.getLogger('fvl.luca.transaction.qualifier')

class Qualified(object):
    def __init__(self, qualLeft, op, qualRight):
        self.left = qualLeft
        self.op = op
        self.right = qualRight
    def __repr__(self):
        return "%s %s %s" % (self.quote(self.left),
                             self.op,
                             self.quote(self.right))  
    def and_(self, other):
        return self.binop(other, 'and')
    __and__ = and_
    def or_(self, other):
        return self.binop(other, 'or')
    __or__ = or_
    def startswith(self, other):
        return self.like(other + "*")
    __mod__ = startswith
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
        return Qualified(self, op, other)
    def quote_string(cls, string):
        assert '"' not in string, \
               "Qualified.quote can't quote strings with quotes (fix it!)"
        return '"%s"' % string
    quote_string = classmethod(quote_string)
    def quote_mxdatetime(cls, mxdatetime):
        return cls.quote_string(str(mxdatetime))
    quote_mxdatetime = classmethod(quote_mxdatetime) 
    def quote_qualified(cls, qual):
        return "(" + repr(qual) + ")"
    quote_qualified = classmethod(quote_qualified)
    def quote(cls, other):
        for cls, qtr in ((basestring, cls.quote_string),
                         (DateTimeType, cls.quote_mxdatetime),
                         (Qualifier, repr),
                         (Qualified, cls.quote_qualified)
                         ):
            if isinstance(other, cls):
                break
        else:
            qtr = repr
        return qtr(other)
    quote = classmethod(quote)
    value = property(__repr__)
    
class Qualifier(Qualified):
    def __init__(self, attr=''):
        self.attr = attr
    def __repr__(self):
        return str(self.attr)    
    def __getattr__(self, attr):
        if attr == 'left' or attr == 'right':
            return None
        if self.attr:
            attr = "%s.%s" % (self.attr, attr)
        return Qualifier(attr)
    value = property(__repr__)

class _NullQualifier(Qualified):
    def __init__(self):
        pass
    def __repr__(self):
        return ''
    value = property(__repr__)
    
nullQualifier = _NullQualifier()
