from collections import defaultdict


class Trie:
    """
    Класс структуры данных
    """
    def __init__(self):
        """
        Инициализация класса структуры данных
        """
        self.root = defaultdict()
        self.tree_str = ''

    def insert(self, word):
        """
        Функция добавления слова
        :param word: введённое слово
        :return: None
        """
        current = self.root
        for letter in word:
            current = current.setdefault(letter, {})
        current.setdefault("_end")

    def clear(self):
        """
        Функция очистки дерева
        :return: None
        """
        self.root = defaultdict()
        self.tree_str = ''

    def remove(self, word):
        """
        Функция удаления слова
        :param word: введённое слово
        :return: None
        """
        self.delete(self.root, word, 0)

    def delete(self, dicts, word, i):
        """
        Функция удаления
        :param dicts: список слов
        :param word: введённое слово
        :param i: итератор
        :return: True/False
        """
        if i == len(word):
            if '_end' in dicts:
                del dicts['_end']
                if len(dicts) == 0:
                    return True
                else:
                    return False
            else:
                return False
        else:
            if word[i] in dicts and self.delete(dicts[word[i]], word, i + 1):
                if len(dicts[word[i]]) == 0:
                    del dicts[word[i]]
                    return True
                else:
                    return False

            else:
                return False

    def search(self, word):
        """
        Функция поиска слова
        :param word: введённое слово
        :return: True/False
        """
        current = self.root
        for letter in word:
            if letter not in current:
                return False
            current = current[letter]
        if "_end" in current:
            return True
        return False

    def startsWith(self, prefix):
        """
        Функция поиска слов по префиксу
        :param prefix: префикс
        :return: True/False
        """
        current = self.root
        for letter in prefix:
            if letter not in current:
                return False
            current = current[letter]
        return True

    def print_words(self, current=None, word=""):
        """
        Функция вывода слова
        :param current: ключ элемента
        :param word: слово
        :return: None
        """
        if current is None:
            current = self.root

        for obj in current:
            if "_end" not in obj:
                self.print_words(current[obj], word+obj)
            else:
                print(word)

    def all_words(self, wlist, current=None, word=""):
        """
        Функция вывода слов
        :param wlist: список слов
        :param current: текущий элемент
        :param word: слово
        :return: wlist
        """
        if current is None:
            current = self.root

        for obj in current:
            if "_end" not in obj:
                self.all_words(wlist, current[obj], word+obj)
            else:
                wlist.append(word)
        return wlist

    def print_trie(self, current=None, n=0):
        """
        Вывод графа слов
        :param current: текущий элемент
        :param n: количество элементов графа
        :return: None
        """
        if current is None:
            current = self.root

        for obj in current:
            if "_end" not in obj:
                self.tree_str += '    |' * n + '-' * 4 + obj + '\n'
                self.print_trie(current[obj], n+1)
