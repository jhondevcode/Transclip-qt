import os


def prepare_workspace():
    static_home = str(__file__).replace("/transclip.py", "")
    if os.getcwd() != static_home:
        os.chdir(static_home)


def main():
    prepare_workspace()
    
    
if __name__ == '__main__':
    main()
