from grammar_functions.grammar_parser import parse_grammar
from grammar_functions.grammar_cleaner import limpar_gramatica


def main():
    grammar = parse_grammar("input.txt")
    clean_grammar = limpar_gramatica(grammar)
    
    producoes = clean_grammar.get("producoes", {})
    
    with open("output.txt", "w", encoding="utf-8") as f:
        for variavel, regras in producoes.items():
            for regra in regras:
                linha = f"{variavel} " + " ".join(regra).replace("''", 'h')  # substitui ε por h
                f.write(linha + "\n")


if __name__ == "__main__":
    main()
