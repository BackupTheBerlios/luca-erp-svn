import unittest
from papo.cimarron import skin
from commonTests import abstractTestWidget

__all__ = ('TestLabel',
           )

class TestLabel(abstractTestWidget):
    def setUp(self):
        super(TestLabel, self).setUp()
        self.parent = self.win = skin.Window(title='Test', parent=self.app)
        self.widget = self.label = skin.Label(text='hello', parent=self.win)

    def testLabel(self):
        self.assertEqual(self.label.text, 'hello')

    def testSetLabel(self):
        raise NotImplementedError
        
    def testShow(self):
        self.win.show()
