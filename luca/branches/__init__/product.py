from fvl import cimarron
cimarron.config ()

s= cimarron.skin.CRUDController.fromXmlFile ('product.xml')
a= cimarron.skin.Application ()
s.parent= a
s.show ()
a.run ()
