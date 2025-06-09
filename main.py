from grammar_functions.grammar_parser import parse_grammar
from grammar_functions.grammar_cleaner import limpar_gramatica
from pprint import pprint


def main():
    grammar = parse_grammar("input.txt")
    clean_grammar = limpar_gramatica(grammar)
    pprint(clean_grammar)


if __name__ == "__main__":
    main()
