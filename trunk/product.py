from fvl.cimarron.skin import CRUDController, Application

s = CRUDController.fromXmlFile('product.xml')
a = Application ()
s.parent = a
s.show()
a.run()
