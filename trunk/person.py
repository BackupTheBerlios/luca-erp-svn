from fvl import cimarron
cimarron.config ()

s= cimarron.skin.CRUDController.fromXmlFile ('person.xml')
a= cimarron.skin.Application ()
s.parent= a
s.show ()
a.run ()
