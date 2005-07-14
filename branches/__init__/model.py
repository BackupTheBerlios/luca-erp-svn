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

    def __init__(self, store=None):
        self.store = store

    def values(cls, trans, qualifier):
        return trans.search(cls, qualifier)
    values = classmethod(values)

    def record(self):
        self.store.add(self)

    def delete(self):
        raise UndeletableClassError, \
              "You can't delete %r instances" % self.__class__.__name__

class DeletableModel(Model):
    def delete(self):
        self.store.delete(self)

from zope import interface
class pseudoIModel(interface.Interface):
    def getattr(attr):
        pass
    def setattr(attr, val):
        pass
    def values(qual):
        pass
    def valuesFor(attr, qual):
        pass

class ITransaction(interface.Interface):
    def commit():
        """
        Saves the transaction to its parent transaction if there is
        one; otherwise, to permanent storage.
        """
    def rollback():
        """
        Discards changes performed in the transaction.
        """
    def track(anObject):
        """
        Adds anObject to the list of objects the transaction is
        tracking.
        """
    def forget(anObject):
        """
        Stop tracking anObject.
        """
    def search(aClass, qualifier):
        """
        Return a generator for a search.
        """

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
