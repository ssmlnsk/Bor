import sqlite3


class SqlDB:
    """
    Класс с функциями для взаимодействия с базой данных
    """
    def save_it(self, word_list, name):
        """
        Функция сохранения данных в базу данных
        :param word_list: список слов
        :param name: название файла с базой данных
        :return: None
        """
        conn = sqlite3.connect(name)
        cur = conn.cursor()
        cur.execute("""DROP TABLE IF EXISTS Trie;""")
        cur.execute("""CREATE TABLE Trie(
           id INT PRIMARY KEY, word TEXT)
        """)

        conn.commit()
        for i in range(len(word_list)):
            cur.execute("""INSERT INTO Trie(id, word) 
            VALUES("""+str(i)+""", '"""+word_list[i]+"""');""")
            conn.commit()

    def load_it(self, name):
        """
        Функция загрузки данных из базы данных в приложение
        :param name: название файла с базой данных
        :return: cur
        """
        conn = sqlite3.connect(name)
        cur = conn.cursor()
        cur.execute("SELECT word FROM Trie;")
        return cur
