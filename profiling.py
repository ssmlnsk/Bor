from main import Trie
import cProfile


with cProfile.Profile() as p:
    trie = Trie()

    with open('test.txt', 'r') as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    for i in content:
        trie.insert(i)

    for j in content:
        trie.remove(j)

    for k in content:
        trie.search(k)


if __name__ == '__main__':
    p.print_stats()
