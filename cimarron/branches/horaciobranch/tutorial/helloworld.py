from fvl import cimarron
cimarron.config()

class MainWindowController(cimarron.skin.WindowController):
   def __init__(self, **kw):
       super(MainWindowController, self).__init__(**kw)
       self.win.title = 'Main Window'
       cimarron.skin.Button(parent=self.win, label='Hello')

app = cimarron.skin.Application()
w = MainWindowController(parent=app)
w.show()
app.run()
