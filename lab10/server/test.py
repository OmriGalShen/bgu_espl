import os
import pathlib

if __name__ == '__main__':
    os.chdir('Server')
    # parent_dir = pathlib.Path(__file__).parent.resolve()
    # rel_path = os.path.relpath(os.getcwd(), start=parent)
    print(os.getcwd())
