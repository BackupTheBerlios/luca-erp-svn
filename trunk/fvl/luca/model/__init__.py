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

logger = logging.getLogger('fvl.luca.model')

model_name = os.path.join(os.path.dirname(__file__), 'pymodel_luca.py')
try:
    model = Model.loadModel(model_name)
except ImportError:
    logger.critical("I couldn't load the pymodel from file %r. Please read INSTALL.txt" % model_name)
    raise
del model_name
ModelSet.defaultModelSet().addModel(model)

class LucaMeta(dynamic.CustomObjectMeta):
    def __new__(cls, className, bases, namespace):
        namespace['mdl_define_properties'] = 1
        return super(LucaMeta, cls).__new__(cls, className, bases, namespace)

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
        namespace[className] = LucaMeta(className, (), {})
