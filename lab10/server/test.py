import os

if __name__ == '__main__':
    local_path = '.\Server'
    filename = 'banana'
    local_file_path = os.path.normpath(os.path.join(local_path, filename))
    f = open(local_file_path, 'wb')
