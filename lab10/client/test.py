import os
from pathlib import PurePath

if __name__ == '__main__':
    # base = PurePath('/Server')
    # p = PurePath('/Server/a/b/c')
    #
    # print(p.is_relative_to(base))
    # Path
    base = "/Server"
    path4 = os.path.normpath(os.path.join(base, "file.txt"))
    path5 = os.path.normpath(os.path.join(base, "/a/.."))

    print(path4)
    print(path5)
    print(PurePath(path4).is_relative_to(base))
    # print(path3.is_relative_to(base))

