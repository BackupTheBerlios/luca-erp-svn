from fvl.cimarron.skin import CRUDController, Application

s = CRUDController.fromXmlFile('person.xml')
a = Application ()
s.parent = a
s.show()
a.run()
