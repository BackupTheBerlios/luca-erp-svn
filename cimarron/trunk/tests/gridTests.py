import unittest
from papo import cimarron
from commonTests import abstractTestControl
from papo.cimarron.controllers import App, Grid

__all__= ('TestGrid', 'Person')


class Person (object):
    def __init__ (self, name, surname):
        self.setName (name)
        self.setSurname (surname)

    def getName (self):
        return self.__name
    def setName (self, name):
        self.__name= name
    name= property (getName, setName)

    def getSurname (self):
        return self.__surname
    def setSurname (self, sn):
        self.__surname= sn
    surname= property (getSurname, setSurname)

class TestGrid (abstractTestControl):
    def setUp (self):
        super (TestGrid, self).setUp ()
        self.model= [
            Person ('jose', 'perez'),
            Person ('marcos', 'dione'),
            Person ('john', 'lenton'),
            ]
        columns= (
            dict (name='Nombre', read=Person.getName, write=Person.setName, search=None),
            dict (name='Apellido', read=Person.getSurname, write=Person.setSurname, search=None),
            )

        self.parent = self.win = cimarron.skin.Window(title='Test', parent=self.app)
        self.widget= self.grid= Grid (
            parent= self.parent,
            columns= columns,
            )

        # so testValue passes
        self.value= None

    def testData (self):
        self.widget.data= self.model

    def testIndex (self):
        self.testData ()
        for i in xrange (len (self.model)):
            self.widget.index= i
            self.assertEqual (self.model[i], self.widget.value)

    def testValue (self):
        self.testData ()
        for i in xrange (len (self.model)):
            self.widget.value= self.model[i]
            self.assertEqual (self.model[i], self.widget.value)

#         self.app.show()
#         self.app.run ()

    def testNoValue (self):
        self.widget.value= None
        self.assertEqual (self.widget.value, None)

    def testWrite (self):
        self.testData ()
        # self.widget.entries[0, 0]._widget.set_text ('juan')
        self.widget.entries[0, 0].value= 'juan'
        self.widget.entries[0, 0].onAction ()
        self.widget.index= 0
        self.assertEqual (self.widget.value.name, 'juan')

if 0:
    def testLive(self):
        self.testData ()
        self.app.show()
        self.app.run ()
