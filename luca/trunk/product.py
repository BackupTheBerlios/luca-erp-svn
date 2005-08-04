from fvl import cimarron
from fvl.cimarron.skin import CRUDController, Application
from fvl.luca.transaction import Transaction

t = Transaction()
s = CRUDController.fromXmlFile('product.xml')
s.store = t
a = Application ()
s.parent = a
s.show()
a.run()
