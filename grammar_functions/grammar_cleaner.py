from grammar_functions.grammar_parser import parse_grammar


def clean_grammar(grammar):
    variables = set(grammar["variables"])
    start_symbol = grammar["start_symbol"]
    productions = grammar["productions"]

    # Remover variáveis inalcançáveis
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

    # Mantém apenas as produções com LHS acessíveis
    productions = {
        var: [prod for prod in rhs if all(sym not in variables or sym in reachable for sym in prod)]
        for var, rhs in productions.items()
        if var in reachable
    }

    # Remover produções vazias (ε-produções)
    nullable = set()
    changed = True
    while changed:
        changed = False
        for var, prods in productions.items():
            for prod in prods:
                if all(sym in nullable or sym == '' for sym in prod):
                    if var not in nullable:
                        nullable.add(var)
                        changed = True

    # Criar novas produções sem os símbolos anuláveis
    new_productions = {}
    for var, prods in productions.items():
        new_productions[var] = []
        for prod in prods:
            subsets = [[]]

            for symbol in prod:
                if symbol in nullable:
                    subsets += [s + [symbol] for s in subsets]
                else:
                    for s in subsets:
                        s.append(symbol)

            for s in subsets:
                if s != []:  # Remove produção vazia
                    if s not in new_productions[var]:
                        new_productions[var].append(s)

    productions = new_productions

    # Se o start_symbol é anulável, podemos opcionalmente adicionar a produção S → ε
    # (Isso depende se você quer permitir ou não)

    # ---------- PASSO 3: Remover produções unitárias ----------
    for var in productions:
        unit_productions = []
        direct_productions = []

        for prod in productions[var]:
            if len(prod) == 1 and prod[0] in variables:
                unit_productions.append(prod[0])
            else:
                direct_productions.append(prod)

        productions[var] = direct_productions

        # Expandir as unitárias
        while unit_productions:
            target = unit_productions.pop()
            for prod in productions.get(target, []):
                if len(prod) == 1 and prod[0] in variables and prod[0] not in unit_productions:
                    unit_productions.append(prod[0])
                elif prod not in productions[var]:
                    productions[var].append(prod)

    # ---------- PASSO FINAL: Remover variáveis sem produções ----------
    productions = {k: v for k, v in productions.items() if v}
    cleaned_variables = set(productions.keys())

    return {
        "variables": sorted(cleaned_variables),
        "start_symbol": start_symbol,
        "productions": productions
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
