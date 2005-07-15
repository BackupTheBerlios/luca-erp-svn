from fvl import cimarron
cimarron.config()

from fvl.luca.model import Product, Stock
from model import Transaction

class StockAdjustmentWindow(cimarron.skin.WindowController):
    def __init__(self, **kw):
        super(StockAdjustmentWindow, self).__init__(**kw)
        self.win.title = "Stock Adjustment"
        self.trans= Transaction ()
        
        v= cimarron.skin.VBox (parent=self.win)

        columnas = (cimarron.skin.Column(name="Code", attribute="product.code", readOnly= True),
                    cimarron.skin.Column(name="Name", attribute="product.name", readOnly= True))
        self.searcher = cimarron.skin.Search(parent=v, columns=columnas,
                                             transaction=self.trans, searcher=Stock,
                                             onAction=self.listValues)
        columnas = (cimarron.skin.Column(name="Code", attribute="product.code", readOnly= True),
                    cimarron.skin.Column(name="Name", attribute="product.name", readOnly= True),
                    cimarron.skin.Column(name="Level", attribute="level"))
        self.stockEditor = cimarron.skin.Grid(parent=v, columns=columnas)
        actionContainer = cimarron.skin.HBox(parent=v)
        save = cimarron.skin.Button(parent=actionContainer, label="Save", onAction=self.save)
        discard = cimarron.skin.Button(parent=actionContainer, label="Discard", onAction=self.discard)

    def listValues(self,sender):
        self.stockEditor.commitValue(sender.value)
        self.stockEditor.refresh()

    def save(self):
        pass

    def discard(self):
        pass

if __name__=='__main__':
    a = cimarron.skin.Application()
    w = StockAdjustmentWindow(parent=a)
    w.show()
    a.run()
