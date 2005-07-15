import os

from Modeling import ModelSet, Model, dynamic

model = Model.searchModel('luca', os.path.dirname(__file__))
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
print model.entitiesNames()
for className in model.entitiesNames():
    if className not in namespace:
        namespace[className] = LucaMeta(className, (), {})
