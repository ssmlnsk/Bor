import sys
import re

import matplotlib.pyplot as plt
import networkx as nx
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QMenuBar, QAction, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from main import Trie
from sql_m import SqlDB
from tree_view import hierarchy_pos


class Window(QWidget):
    """
    Класс создания главного окна
    """
    def __init__(self):
        """
        Инициализация окна приложения
        """
        super(Window, self).__init__()
        self.trie = Trie()
        self.initUI()
        self.setWindowTitle('Trie')
        self.an_win = None
        self.graph = nx.Graph()

    def initUI(self):
        """
        Прикрепление функций к элементам окна
        :return: None
        """
        self.grid = QVBoxLayout()
        self.setLayout(self.grid)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.grid.addWidget(self.canvas, 0)
        self.menu_bar = QMenuBar()
        self.menubtn = QAction("Меню", self)
        self.menu_bar.addAction(self.menubtn)
        self.menubtn.triggered.connect(self.menu_load)
        self.grid.setMenuBar(self.menu_bar)

    def menu_load(self):
        """
        Функция загрузки окна "Меню"
        :return:
        """
        self.an_win = MenuWindow(self)
        self.an_win.show()

    def redraw(self):
        """
        Функция перерисовки графа
        :return:
        """
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
        """
        Функция записи слова
        :param current: текущий элемент
        :param prev_node: предыдущий узел
        :return: None
        """
        if current is None:
            current = self.trie.root

        prev_node = self.count
        node = self.count
        i = 1
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
    """
    Класс окна "Меню"
    """
    def __init__(self, w):
        """
        Загрузка окна и прикрепление действий к кнопкам
        :param w: основное окно
        """
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
        self.save_but.clicked.connect(self.save_db)
        self.load_but.clicked.connect(self.load_db)
        self.sqlcmds = SqlDB()
        self.hide_all()

    def hide_all(self):
        """
        Функция закрытия всех форм
        :return: None
        """
        self.frame1.hide()
        self.frame2.hide()
        self.frame3.hide()
        self.frame4.hide()

    def frm1show(self):
        """
        Функция показа формы добавления
        :return: None
        """
        self.hide_all()
        self.frame1.show()

    def frm2show(self):
        """
        Функция показа формы удаления
        :return: None
        """
        self.hide_all()
        self.frame2.show()

    def frm3show(self):
        """
        Функция показа формы поиска
        :return: None
        """
        self.hide_all()
        self.frame3.show()

    def frm4show(self):
        """
        Функция показа формы сохранения и загрузки
        :return: None
        """
        self.hide_all()
        self.frame4.show()

    def add_word(self):
        """
        Функция добавления слова
        :return: None
        """
        word = self.lineEdit.text()
        if word.isalpha() == False:
            self.warning()
        else:
            self.w.trie.insert(word)
            self.w.redraw()

    def warning(self):
        """
        Создание MessageBox при некорректном вводе
        :return: None
        """
        messagebox_input = QMessageBox(self)
        messagebox_input.setWindowTitle("Ошибка ввода")
        messagebox_input.setText("Введите слово!")
        messagebox_input.setIcon(QMessageBox.Warning)
        messagebox_input.setStandardButtons(QMessageBox.Ok)
        messagebox_input.show()

    def del_all_word(self):
        """
        Функция удаления всех слов
        :return: None
        """
        self.w.trie.clear()
        self.w.redraw()

    def del_word(self):
        """
        Функция удаления введённого слова
        :return: None
        """
        word = self.lineEdit3.text()
        result = self.w.trie.search(word)
        if result == False:
            self.info.setText('Слово не найдено!')
        else:
            self.info.setText('Слово удалено!')
            self.w.trie.remove(word)
            self.w.redraw()

    def search_word(self):
        """
        Функция поиска слова
        :return: None
        """
        word = self.searchEdit.text()
        result = self.w.trie.search(word)
        if result == True:
            self.search_res.setText('Слово найдено!')
        else:
            self.search_res.setText('Слово не найдено!')

    def save_db(self):
        """
        Функция сохранения данных в базу данных
        :return: None
        """
        pattern = ('/', ':', '?', '*', '"', '|', '<', '>')
        regex = r'[\/:?*"|<>]'
        file_name = self.fileline.text()
        a = bool(re.search(regex, file_name))
        if a == True:
            self.file_name_warning()
        else:
            words = self.w.trie.all_words([])
            self.sqlcmds.save_it(words, file_name + '.db')

    def load_db(self):
        """
        Функция загрузки данных из базы данных в приложение
        :return: None
        """
        file_name = self.fileline.text()
        words = self.sqlcmds.load_it(file_name + '.db')
        self.w.trie.clear()
        for wrd in words:
            self.w.trie.insert(wrd[0])
        self.w.redraw()

    def file_name_warning(self):
        """
        Создание MessageBox при некорректном вводе
        :return: None
        """
        messagebox_file = QMessageBox(self)
        messagebox_file.setWindowTitle("Ошибка ввода")
        messagebox_file.setText("Имя файла не должно содержать следующих знаков:")
        messagebox_file.setInformativeText(f''' \ / : ? * " | < > ''')
        messagebox_file.setIcon(QMessageBox.Warning)
        messagebox_file.setStandardButtons(QMessageBox.Ok)
        messagebox_file.show()

app = QApplication(sys.argv)
if __name__ == '__main__':
    w = Window()
    w.resize(600, 500)
    w.show()
    sys.exit(app.exec_())
