from Modeling.EditingContext import EditingContext

from fvl.cimarron.model import Model as CimarronModel

class autoproperty(type):
    def __new__(cls, name, bases, attrDict):
        """
        Builds properties using the methods 'get<st>', 'set<st>'
        for every attribute 'validate<st>'. it's very tied to Modeling.
        """
        properties = []
        for key in attrDict:
            if key.startswith('validate'):
                properties.append(key[8:])
        theClass = super(autoproperty, cls).__new__(cls, name, bases, attrDict)
        for prop in properties:
            setattr(theClass, prop[0].lower() + prop[1:],
                    property(getattr(theClass, 'get' + prop),
                             getattr(theClass, 'set' + prop)))
        return theClass
            
class Model(CimarronModel):
    __metaclass__ = autoproperty
    def search (cls, trans, **kw):
        return trans.search (cls.__name__, **kw)
    search = classmethod(search)

class Transaction(object):
    def __init__(self):
        self.ec = EditingContext()
        
    def append(self,obj):
        try:
            self.ec.insert(obj)
        except ValueError:
            pass
        
    def commit(self):
        self.ec.saveChanges()

    def rollBack(self):
        """
        Discards all the changes made to the model.
        The objects associated to this Transaction will be in an
        undefined state.
        """
#         for i in self.ec.allDeletedObjects():
#             self.ec.refaultObject(i)
#         for i in self.ec.allInsertedObjects():
#             self.ec.refaultObject(i)
#         for i in self.ec.allUpdatedObjects():
#             self.ec.refaultObject(i)
        self.ec = EditingContext()

    def search(self, className, **kw):
        qual = " and ".join([ '%s ilike "%s*"' % (attr, value and value or '')
                              for attr, value in kw.items() ])
        return self.ec.fetch(className, qualifier=qual)
