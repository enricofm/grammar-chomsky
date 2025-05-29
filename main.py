from grammar_parser import parse_grammar
from pprint import pprint


def main():
    grammar = parse_grammar("input.txt")
    return pprint(grammar)


if __name__ == "__main__":
    main()
