from grammar_functions.grammar_parser import parse_grammar


def clean_grammar(grammar):
    variables = set(grammar["variables"])
    start_symbol = grammar["start_symbol"]
    productions = grammar["productions"]

    # encontrar variáveis alcançáveis a partir do símbolo inicial
    reachable = set()
    queue = [start_symbol]

    while queue:
        current = queue.pop()
        if current in reachable:
            continue
        reachable.add(current)
        for prod in productions.get(current, []):
            for symbol in prod:
                if symbol in variables and symbol not in reachable:
                    queue.append(symbol)

    # Mantem apenas produções cujos LHS são alcançáveis
    cleaned_productions = {
        var: [prod for prod in rhs if all(
            sym not in variables or sym in reachable for sym in prod)]
        for var, rhs in productions.items()
        if var in reachable
    }

    # Remove produções vazias
    cleaned_productions = {k: v for k, v in cleaned_productions.items() if v}

    return {
        "variables": sorted(reachable),
        "start_symbol": start_symbol,
        "productions": cleaned_productions
    }


def generate_output(grammar, file_path):
    with open(file_path, "w") as f:
        f.write(" ".join(grammar["variables"]) + "\n")
        f.write(grammar["start_symbol"] + "\n")
        for left, right_list in grammar["productions"].items():
            for right in right_list:
                f.write(f"{left} {' '.join(right)}\n")


def clean(file_name):
    initial_grammar = parse_grammar(file_name)
    cleaned = clean_grammar(initial_grammar)
    generate_output(cleaned, "output_clean.txt")
