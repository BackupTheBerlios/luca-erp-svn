from fvl.cimarron.skin import CRUDController, Application
from fvl.luca.transaction import Transaction

t = Transaction()
s = CRUDController.fromXmlFile('point_of_sale.xml')
s.store = t
a = Application()
s.parent = a
s.show()
a.run()
