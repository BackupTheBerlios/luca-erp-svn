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

"""
Different utility functions that don't yet warrant a class of their own.
"""

__revision__ = int('$Rev$'[5:-1])


import re

def makeName(name):
    """
    Change C{name} from underscore-delimited words to camelcase.
    """
    def __upper__(letter):
        return letter.group(1).upper()
    # some_thing
    name = re.sub(r'_([a-z])', __upper__, name)
    # someThing
    return name

def MakeName(name):
    """
    Change C{name} from lowercase camelcase to uppercase camelcase.
    """
    name = makeName(name)
    # someThing
    name = name[0:1].upper()+name[1:]
    # SomeThing
    return name

def traverse (obj, path):
    """
    Returns the object found by traversing the path
    (as a string) starting from obj.
    """
    pathList = path.split('.')
    while pathList:
        elem = pathList[0]
        try:
            obj = getattr(obj, elem)
        except AttributeError, e:
            if callable(obj):
                return obj(*pathList)
            else:
                e.args = ('while traversing %r for %r on the %r path (%r left)'
                          % (obj, elem, path, pathList), )
                raise
        del pathList[0]
    return obj

class Null(object):
    """
    This object is a poisonous Null object.
    """
    __slots__ = ()
    def __call__(self, *a, **kw):
        return Null
    def __getattr__(self, attr):
        return Null
    def __setattr__(self, attr, val):
        pass
    def __nonzero__(self):
        return False
Null = Null()

simple_types = (str, unicode, type(None), bool, int, long, float, complex )
  	 
def is_simple(obj): 	 
    t = type(obj) 	 
    
    return (t in simple_types # really simple
            or ( t in (tuple, list) and 	 
                 len(filter(None, map(is_simple, obj))) == len(obj))
            # composite of simples 	 
            or ( t is dict and 	 
                 len(filter(None, map(is_simple, obj.keys()))) == \
                 len(filter(None, map(is_simple, obj.values()))) == len(obj))
            ) 	 
