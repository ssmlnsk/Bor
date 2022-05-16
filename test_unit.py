import unittest
from main import Trie


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.trie = Trie()

    def test_add(self):
        words = ['cat', 'calm', 'call', 'computer', 'palm']

        for w in words:
            self.trie.insert(w)
        self.assertEqual(self.trie.all_words([]), words)

    def test_remove(self):
        words = ['cat', 'calm', 'call', 'computer', 'palm']
        for w in words:
            self.trie.insert(w)

        self.trie.remove('call')
        words.pop(2)
        self.assertEqual(self.trie.all_words([]), words)
        self.trie.remove('computer')
        words.pop(2)
        self.assertEqual(self.trie.all_words([]), words)

    def test_search(self):
        words = ['cat', 'calm', 'call', 'computer', 'palm']
        for w in words:
            self.trie.insert(w)

        self.assertEqual(self.trie.search('cat'), True)
        self.assertEqual(self.trie.search('dog'), False)
        self.assertEqual(self.trie.search('cal'), False)

    def test_startsWith(self):
        words = ['cat', 'calm', 'call', 'computer', 'palm']
        for w in words:
            self.trie.insert(w)

        self.assertEqual(self.trie.startsWith('comp'), True)
        self.assertEqual(self.trie.startsWith('call'), True)
        self.assertEqual(self.trie.startsWith('ro'), False)


if __name__ == '__main__':
    unittest.main()
