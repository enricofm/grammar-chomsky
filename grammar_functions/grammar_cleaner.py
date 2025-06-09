from itertools import chain, combinations


def add_new_start_symbol(grammar):
    original_start = grammar["simbolo_inicial"]

    # gera novo simbolo inicial
    new_start = "S0"
    while new_start in grammar["variaveis"] or new_start in grammar["producoes"]:
        new_start += "0"

    grammar["variaveis"].insert(0, new_start)
    grammar["simbolo_inicial"] = new_start

    grammar["producoes"][new_start] = [[original_start]]

    return grammar


def find_nullable_variables(grammar):
    nullable = set()

    changed = True
    while changed:
        changed = False
        for left, rights in grammar["producoes"].items():
            for right in rights:
                if right == ['h'] or all(symbol in nullable for symbol in right):
                    if left not in nullable:
                        nullable.add(left)
                        changed = True
    return nullable


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1))


def remove_epsilon_productions(grammar):
    nullable = find_nullable_variables(grammar)
    new_productions = {}

    for left, rights in grammar["producoes"].items():
        new_rights = set()
        for right in rights:
            if right == ['h']:
                continue

            # acha posicao das variaveis que geram producoes vazias
            nullable_positions = [i for i, symbol in enumerate(
                right) if symbol in nullable]

            # gera todas as combinacoes da remocao de variaveis vazias
            subsets = list(powerset(nullable_positions))

            for subset in subsets:
                if len(subset) == len(right):
                    continue

                new_right = [symbol for i, symbol in enumerate(
                    right) if i not in subset]
                if new_right:
                    new_rights.add(tuple(new_right))

            # mantem producao inicial
            new_rights.add(tuple(right))

        new_productions[left] = [list(prod) for prod in new_rights]

    # se o simbolo inicial deriva vazio, mantem h
    if grammar["simbolo_inicial"] in nullable:
        new_productions[grammar["simbolo_inicial"]].append(['h'])

    grammar["producoes"] = new_productions
    return grammar


def limpar_gramatica(grammar):
    new_grammar = add_new_start_symbol(grammar)
    new_grammar = remove_epsilon_productions(new_grammar)
    return new_grammar
