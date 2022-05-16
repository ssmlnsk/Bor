import sys

from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QDialog, QMessageBox, QMenuBar, QListWidget, QAction
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


from tree_view import hierarchy_pos
from main import Trie
from sql_m import sqldb
import networkx as nx

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.trie = Trie()

        self.initUI()
        self.setWindowTitle('Trie')
        self.an_win = None
        self.graph = nx.Graph()

    def initUI(self):
        self.grid = QVBoxLayout()
        self.setLayout(self.grid)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.grid.addWidget(self.canvas, 0)
        self.menu_bar = QMenuBar()
        self.menubtn = QAction("Меню", self)
        self.menu_bar.addAction(self.menubtn)
        self.menubtn.triggered.connect(self.MenuLoad)
        self.grid.setMenuBar(self.menu_bar)
        #self.redraw()

    def MenuLoad(self):
        self.an_win = MenuWindow(self)
        self.an_win.show()


    def redraw(self):
        plt.clf()
        self.graph = nx.Graph()

        self.labels = {}
        self.endwrd = []
        self.count = 0

        if self.trie.root != {}:
            self.nx_trie()
            pos = hierarchy_pos(self.graph, 0)
            nx.draw(self.graph, pos=pos)
            nx.draw_networkx_nodes(self.graph, pos=pos, nodelist=self.endwrd, node_color="tab:red")
            nx.draw_networkx_labels(self.graph, pos=pos, labels=self.labels, font_size=18, font_color="whitesmoke")
        self.canvas.draw()

    def nx_trie(self, current=None, prev_node=None):
        if current is None:
            current = self.trie.root

        prev_node = self.count
        node = self.count
        i=1
        for obj in current:
            if "_end" not in obj:
                self.count += i
                self.labels[self.count] = obj
                self.graph.add_edge(prev_node, self.count)
                self.nx_trie(current[obj], self.count)
                i += 1
            else:
                self.endwrd.append(node)

class MenuWindow(QWidget):
    def __init__(self, w):
        super().__init__()
        uic.loadUi('Menu.ui', self)
        self.w = w
        self.add_btn.clicked.connect(self.frm1show)
        self.del_btn.clicked.connect(self.frm2show)
        self.search_btn.clicked.connect(self.frm3show)
        self.sv_button.clicked.connect(self.frm4show)
        self.confirm_btn.clicked.connect(self.add_word)
        self.clear_btn.clicked.connect(self.del_all_word)
        self.confirm_btn2.clicked.connect(self.del_word)
        self.confirm_btn3.clicked.connect(self.search_word)
        self.save_but.clicked.connect(self.savedb)
        self.load_but.clicked.connect(self.loaddb)
        self.sqlcmds = sqldb()
        #self.load_but.clicked.connect(self)

        self.hideAll()

    def hideAll(self):
        self.frame1.hide()
        self.frame2.hide()
        self.frame3.hide()
        self.frame4.hide()

    def frm1show(self):
        self.hideAll()
        self.frame1.show()

    def frm2show(self):
        self.hideAll()
        self.frame2.show()

    def frm3show(self):
        self.hideAll()
        self.frame3.show()

    def frm4show(self):
        self.hideAll()
        self.frame4.show()

    def add_word(self):
        word = self.lineEdit.text()
        self.w.trie.insert(word)
        self.w.redraw()

    def del_all_word(self):
        self.w.trie.clear()
        self.w.redraw()

    def del_word(self):
        word = self.lineEdit3.text()
        self.w.trie.remove(word)
        self.w.redraw()

    def search_word(self):
        word = self.searchEdit.text()
        result = self.w.trie.search(word)
        if result == True:
            self.search_res.setText('Слово существует :D')
        else:
            self.search_res.setText('Слово не найдено -_-')

    def savedb(self):
        file_name = self.fileline.text()
        words = self.w.trie.all_words([])
        self.sqlcmds.save_it(words,file_name + '.db')
    def loaddb(self):
        file_name = self.fileline.text()
        words = self.sqlcmds.load_it(file_name + '.db')
        self.w.trie.clear()
        for wrd in words:
            self.w.trie.insert(wrd[0])
        self.w.redraw()

app = QApplication(sys.argv)
if __name__ == '__main__':
    w = Window()
    w.resize(600, 500)
    w.show()
    sys.exit(app.exec_())