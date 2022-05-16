import sqlite3

class sqldb:
    def save_it(self, word_list, name):
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
        conn = sqlite3.connect(name)
        cur = conn.cursor()
        cur.execute("SELECT word FROM Trie;")
        return cur
