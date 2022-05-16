import cProfile
import test_GUI
import test_unit


def start():
    cProfile.run('test_GUI.unittest.main()')
    cProfile.run('test_unit.unittest.main()')

if __name__ == "__main__":
    start()