from fvl.cimarron.skin import CRUDController, Application
from fvl.luca.transaction import Transaction

def main():
    t = Transaction()
    s = CRUDController.fromXmlFile('point_of_sale.xml')
    s.store = t
    a = Application()
    s.parent = Application()
    s.show()
    a.run()

if __name__=='__main__':
    print 'Running ', __file__
    main()
