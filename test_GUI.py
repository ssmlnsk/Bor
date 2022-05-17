import os
import unittest

from PyQt5 import QtCore
from PyQt5.QtTest import QTest

from wind import Window


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.gui = Window()

    def test_GUIadd(self):
        self.gui.menu_load()
        QTest.mouseClick(self.gui.an_win.add_btn, QtCore.Qt.MouseButton.LeftButton)
        words = ['cat', 'calm', 'call', 'computer', 'palm']
        QTest.qWaitForWindowActive(self.gui)
        for w in words:
            self.gui.an_win.lineEdit.setText(w)
            QTest.mouseClick(self.gui.an_win.confirm_btn, QtCore.Qt.MouseButton.LeftButton)
        self.assertEqual(dict(self.gui.labels), {1: 'c', 2: 'a', 3: 't', 5: 'l', 6: 'm', 8: 'l',
                                                 10: 'o', 11: 'm', 12: 'p', 13: 'u', 14: 't',
                                                 15: 'e', 16: 'r', 18: 'p', 19: 'a', 20: 'l', 21: 'm'})

    def test_GUIclear(self):
        self.gui.menu_load()
        QTest.mouseClick(self.gui.an_win.add_btn, QtCore.Qt.MouseButton.LeftButton)
        words = ['cat', 'calm', 'call', 'computer', 'palm']
        for w in words:
            self.gui.an_win.lineEdit.setText(w)
            QTest.mouseClick(self.gui.an_win.confirm_btn, QtCore.Qt.MouseButton.LeftButton)

        QTest.mouseClick(self.gui.an_win.del_btn, QtCore.Qt.MouseButton.LeftButton)
        QTest.mouseClick(self.gui.an_win.clear_btn, QtCore.Qt.MouseButton.LeftButton)
        self.gui.an_win.close()
        self.assertEqual(dict(self.gui.labels), dict())

    def test_GUIsearch(self):
        self.gui.menu_load()
        QTest.mouseClick(self.gui.an_win.add_btn, QtCore.Qt.MouseButton.LeftButton)
        words = ['cat', 'calm', 'call', 'computer', 'palm']
        for w in words:
            self.gui.an_win.lineEdit.setText(w)
            QTest.mouseClick(self.gui.an_win.confirm_btn, QtCore.Qt.MouseButton.LeftButton)

        QTest.mouseClick(self.gui.an_win.search_btn, QtCore.Qt.MouseButton.LeftButton)
        self.gui.an_win.searchEdit.setText('kot')
        QTest.mouseClick(self.gui.an_win.confirm_btn3, QtCore.Qt.MouseButton.LeftButton)
        self.assertEqual(self.gui.an_win.search_res.text(), "Слово не найдено -_-")
        self.gui.an_win.searchEdit.setText('cat')
        QTest.mouseClick(self.gui.an_win.confirm_btn3, QtCore.Qt.MouseButton.LeftButton)
        self.assertEqual(self.gui.an_win.search_res.text(), "Слово существует :D")

    def test_GUIremove(self):
        self.gui.menu_load()
        QTest.mouseClick(self.gui.an_win.add_btn, QtCore.Qt.MouseButton.LeftButton)
        words = ['cat', 'calm', 'call', 'computer', 'palm']
        for w in words:
            self.gui.an_win.lineEdit.setText(w)
            QTest.mouseClick(self.gui.an_win.confirm_btn, QtCore.Qt.MouseButton.LeftButton)

        QTest.mouseClick(self.gui.an_win.del_btn, QtCore.Qt.MouseButton.LeftButton)
        self.gui.an_win.lineEdit3.setText('cat')
        QTest.mouseClick(self.gui.an_win.confirm_btn2, QtCore.Qt.MouseButton.LeftButton)
        self.assertEqual(dict(self.gui.labels), {1: 'c', 2: 'a', 3: 'l', 4: 'm', 6: 'l', 8: 'o', 9: 'm',
                                                 10: 'p', 11: 'u', 12: 't', 13: 'e', 14: 'r', 16: 'p',
                                                 17: 'a', 18: 'l', 19: 'm'})

    def test_GUIsaveload(self):
        self.gui.menu_load()
        QTest.mouseClick(self.gui.an_win.add_btn, QtCore.Qt.MouseButton.LeftButton)
        words = ['cat', 'calm', 'call', 'computer', 'palm']
        for w in words:
            self.gui.an_win.lineEdit.setText(w)
            QTest.mouseClick(self.gui.an_win.confirm_btn, QtCore.Qt.MouseButton.LeftButton)
        QTest.mouseClick(self.gui.an_win.sv_button, QtCore.Qt.MouseButton.LeftButton)
        self.gui.an_win.fileline.setText('temp_test')
        QTest.mouseClick(self.gui.an_win.save_but, QtCore.Qt.MouseButton.LeftButton)
        QTest.mouseClick(self.gui.an_win.del_btn, QtCore.Qt.MouseButton.LeftButton)
        QTest.mouseClick(self.gui.an_win.clear_btn, QtCore.Qt.MouseButton.LeftButton)
        QTest.mouseClick(self.gui.an_win.sv_button, QtCore.Qt.MouseButton.LeftButton)
        QTest.mouseClick(self.gui.an_win.load_but, QtCore.Qt.MouseButton.LeftButton)
        self.assertEqual(dict(self.gui.labels), {1: 'c', 2: 'a', 3: 't', 5: 'l', 6: 'm', 8: 'l',
                                                 10: 'o', 11: 'm', 12: 'p', 13: 'u', 14: 't', 15: 'e',
                                                 16: 'r', 18: 'p', 19: 'a', 20: 'l', 21: 'm'})
        os.remove('temp_test.db')

