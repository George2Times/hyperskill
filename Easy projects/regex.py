import re


def main():
    pattern, text = input().split('|')
    p = re.compile(pattern)
    result = p.search(text)
    if result is None:
        print(False)
    else:
        print(True)


if __name__ == '__main__':
    main()
