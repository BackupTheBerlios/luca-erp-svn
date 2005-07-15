from fvl import cimarron
cimarron.config()

from fvl.luca.model import Person, Receipt
from model import Transaction

class ReceiptWindow(cimarron.skin.WindowController):
    def __init__(self, **kw):
        super(ReceiptWindow, self).__init__(**kw)
        self.win.title = "Receipt Generation"
        self.trans = Transaction()
        self.commitValue(Receipt())

        v = cimarron.skin.VBox(parent=self.win)
        h1 = cimarron.skin.HBox(parent=v)
        h2 = cimarron.skin.HBox(parent=v)

        columns = (cimarron.skin.Column(name="Name", attribute="name"),
                   cimarron.skin.Column(name="surname", attribute="surname"))
        self.person = cimarron.skin.SearchEntry(parent=h1, searcher=Person,
                                                transaction=self.trans, columns=columns,
                                                attribute="person")
        self.amount = cimarron.skin.Entry(parent=h1,  attribute="amount")
        self.concept = cimarron.skin.Entry(parent=h2, attribute="concept")
        self.date = cimarron.skin.Entry(parent=h2, attribute="date")
        
        self.refresh()
    
    def refresh(self):
        super(ReceiptWindow, self).refresh()
        for entry in ("person", "amount", "concept", "date"):
            getattr(self, entry).newTarget(self.value)

if __name__=='__main__':
    a = cimarron.skin.Application()
    w = ReceiptWindow(parent=a)
    w.show()
    a.run()
