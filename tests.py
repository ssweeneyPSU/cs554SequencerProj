import unittest

from interface import Button

class TestButtonClick(unittest.TestCase):

    def testCenterClick(self):
        b = Button(30, 30, 30, 30, "test", (0,0,0), "test")
        self.assertTrue(b.is_clicked(45,45))

    def testCornerClick(self):
        b = Button(30, 30, 30, 30, "test", (0,0,0), "test")
        self.assertTrue(b.is_clicked(30,30))

    def testOutsideClick(self):
        b = Button(30, 30, 30, 30, "test", (0,0,0), "test")
        self.assertFalse(b.is_clicked(0, 0))

unittest.main()