from plumbum import local


if __name__ == "__main__":
    ls = local["ls"]
    print(ls())
    
