from collections import defaultdict
import itertools as IT

class Trie:
    def __init__(self):
        self.root = defaultdict()
        self.tree_str = ''

    def insert(self, word):
        current = self.root
        for letter in word:
            current = current.setdefault(letter, {})
        current.setdefault("_end")

    def clear(self):
        self.root = defaultdict()
        self.tree_str = ''

    def remove(self, word):
        self.delete(self.root, word, 0)

    def delete(self, dicts, word, i):
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
        current = self.root
        for letter in word:
            if letter not in current:
                return False
            current = current[letter]
        if "_end" in current:
            return True
        return False

    def startsWith(self, prefix):
        current = self.root
        for letter in prefix:
            if letter not in current:
                return False
            current = current[letter]
        return True

    def print_words(self, current=None, word=""):
        if current is None:
            current = self.root

        for obj in current:
            if "_end" not in obj:
                self.print_words(current[obj],word+obj)
            else:
                print(word)

    def all_words(self,wlist, current=None, word=""):
        if current is None:
            current = self.root

        for obj in current:
            if "_end" not in obj:
                self.all_words(wlist, current[obj], word+obj)
            else:
                wlist.append(word)
        return wlist

    def print_trie(self, current=None, n=0):
        if current is None:
            current = self.root

        for obj in current:
            if "_end" not in obj:
                self.tree_str += '    |' * n + '-' * 4 + obj + '\n'
                self.print_trie(current[obj], n+1)


if __name__ == "__main__":
    test = Trie()
    test.insert('hills')
    test.insert('high')
    test.insert('hole')
    test.insert('hope')
    test.insert('hunter')
    test.insert('host')


    print(test.root)
    test.print_words()
    print("````````````")
    test.print_trie()
    print(test.tree_str)

    print (test.search('hello'))
    print (test.startsWith('whe'))
    print (test.search('girls'))
    test.remove('high')
    test.remove('hills')
    test.print_words()

