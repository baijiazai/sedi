import sys

from .engine import Baidu
from .config import TIPS


def main():
    try:
        Baidu(*sys.argv[1:]).begin()
    except Exception:
        print(TIPS)


if __name__ == '__main__':
    main()
