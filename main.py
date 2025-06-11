from grammar_functions.grammar_parser import parse_grammar, write_grammar
from grammar_functions.grammar_cleaner import limpar_gramatica


def main():
    grammar = parse_grammar("input.txt")
    clean_grammar = limpar_gramatica(grammar)
    write_grammar(clean_grammar, "output.txt")


if __name__ == "__main__":
    main()
