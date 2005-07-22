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

__revision__ = int('$Rev: 200 $'[5:-1])

import os
import logging

from Modeling import ModelSet, Model, dynamic
from Modeling.CustomObject import CustomObject

from fvl.cimarron.model import Model as CimarronModel

logger = logging.getLogger('fvl.luca.model')

model_name = os.path.join(os.path.dirname(__file__), 'pymodel_luca.py')
try:
    model = Model.loadModel(model_name)
except ImportError:
    logger.critical("I couldn't load the pymodel from file %r."
                    " Please read INSTALL.txt" % model_name)
    raise
del model_name
ModelSet.defaultModelSet().addModel(model)

# HACK!!
# we mess around with the internals of Modeling.dynamic here.
orig_setters_code = dynamic.setters_code
def setters_code(prop):
    rv = orig_setters_code(prop)
    if 'type' in prop.__class__.__dict__:
        # if it has a type, rv is a list of a single 2-uple
        (fname, code), = rv
        aType = prop.type()
        if aType == 'DateTime':
            aType = 'DateTimeFrom'
        code = code[:-3] + aType + '(obj)'
        rv = [(fname, code)]
    return rv
dynamic.setters_code = setters_code
from mx.DateTime import DateTimeFrom
dynamic.DateTimeFrom = DateTimeFrom
del DateTimeFrom

orig_getter_code = dynamic.getter_code
def getter_code(prop):
    rv = orig_getter_code(prop)
    fname, code = rv
    if 'type' in prop.__class__.__dict__:
        pos = code.find('return') + len('return') + 1
        code = '%sunicode(%s)' % (code[:pos], code[pos:])
    return fname, code
dynamic.getter_code = getter_code
# end HACK

class LucaMeta(type):
    def __new__(cls, className, bases, namespace):
        entity = model.entityNamed(className)
        if entity is None:
            raise RuntimeError, 'BUG!'
        dynamic.define_init(entity, className, namespace)
        dynamic.define_getters(entity, className, namespace)
        dynamic.define_setters(entity, className, namespace)
        dynamic.define_properties(entity, className, namespace)
        return super(LucaMeta, cls).__new__(cls, className, bases, namespace)

class LucaModel(CimarronModel):
    def entityName(cls):
        return cls.__name__
    entityName = classmethod(entityName)

__metaclass__ = LucaMeta

# now the idea is that, for every class in the model you create a
# class, and add methods to it if necessary. E.g,
#   class Person:
#       pass
# since this would be tedious and error-prone, just define the classes
# you actually need below, and we'll automatically generate the rest
# (below).
# be sure to ad the classes *below* this line

# just be sure to add the classes *above* this line
namespace = globals()
for className in model.entitiesNames():
    if className not in namespace:
        namespace[className] = LucaMeta(className,
        # add superclasses here --------------------vvvvv
                                        (LucaModel, CustomObject), {})
