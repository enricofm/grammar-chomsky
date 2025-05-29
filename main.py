from grammar_functions.grammar_cleaner import clean
from pprint import pprint


def main():
    grammar = clean("input.txt")
    return pprint(grammar)


if __name__ == "__main__":
    main()
