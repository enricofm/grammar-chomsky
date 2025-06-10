from itertools import chain, combinations


def add_new_start_symbol(grammar):
    original_start = grammar["simbolo_inicial"]
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
                if right == ['h'] or all(sym in nullable for sym in right):
                    if left not in nullable:
                        nullable.add(left)
                        changed = True
    return nullable


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s) + 1))


def remove_epsilon_productions(grammar):
    nullable = find_nullable_variables(grammar)
    new_productions = {}
    for left, rights in grammar["producoes"].items():
        new_rights = set()
        for right in rights:
            if right == ['h']:
                continue
            null_pos = [i for i, sym in enumerate(right) if sym in nullable]
            for subset in powerset(null_pos):
                if len(subset) == len(right):
                    continue
                new_r = [sym for i, sym in enumerate(right) if i not in subset]
                if new_r:
                    new_rights.add(tuple(new_r))
            new_rights.add(tuple(right))
        new_productions[left] = [list(r) for r in new_rights]
    start = grammar["simbolo_inicial"]
    if start in nullable:
        new_productions[start].append(['h'])
    grammar["producoes"] = new_productions
    return grammar


def remove_unit_productions(grammar):
    prods = grammar["producoes"]
    vars_ = grammar["variaveis"]
    unit = set()
    for A in vars_:
        for right in prods.get(A, []):
            if len(right) == 1 and right[0] in vars_:
                unit.add((A, right[0]))
    for A in vars_:
        unit.add((A, A))
    changed = True
    while changed:
        changed = False
        for (A, B) in list(unit):
            for (C, D) in list(unit):
                if B == C and (A, D) not in unit:
                    unit.add((A, D))
                    changed = True
    new_productions = {}
    for A in vars_:
        rights = set()
        for (X, Y) in unit:
            if X == A:
                for r in prods.get(Y, []):
                    if not (len(r) == 1 and r[0] in vars_):
                        rights.add(tuple(r))
        new_productions[A] = [list(r) for r in rights]
    grammar["producoes"] = new_productions
    return grammar


def replace_terminals(grammar):
    prods = grammar["producoes"]
    term_map = {}
    for left in list(prods):
        rights = prods[left]
        new_rights = []
        for right in rights:
            if len(right) > 1:
                new_r = []
                for sym in right:
                    if sym not in grammar["variaveis"] and sym != 'h':
                        var = term_map.get(sym)
                        if not var:
                            var = f"T{sym.upper()}"
                            count = 0
                            while var in grammar["variaveis"]:
                                count += 1
                                var = f"T{sym}{count}"
                            term_map[sym] = var
                            grammar["variaveis"].append(var)
                            grammar["producoes"][var] = [[sym]]
                        new_r.append(var)
                    else:
                        new_r.append(sym)
                new_rights.append(new_r)
            else:
                new_rights.append(right)
        prods[left] = new_rights
    return grammar


def binarize_productions(grammar):
    prods = grammar["producoes"]
    new_prods = {}
    tail_map = {}
    counter = 0

    def get_or_create(pair):
        nonlocal counter
        if pair not in tail_map:
            var = f"X{counter}"
            counter += 1
            tail_map[pair] = var
            # register new variable and its production
            grammar["variaveis"].append(var)
            new_prods.setdefault(var, []).append(list(pair))
        return tail_map[pair]

    for left, rights in prods.items():
        for right in rights:
            if len(right) <= 2 or right == ['h']:
                new_prods.setdefault(left, []).append(right)
            else:
                # build chain from rightmost pair
                prev = None
                for i in range(len(right) - 1, 0, -1):
                    if prev is None:
                        # rightmost pair
                        pair = (right[i-1], right[i])
                        prev = get_or_create(pair)
                    else:
                        # intermediate pair
                        pair = (right[i-1], prev)
                        if i-1 == 0:
                            # head binary rule
                            new_prods.setdefault(
                                left, []).append([right[0], prev])
                        else:
                            prev = get_or_create(pair)
    grammar["producoes"] = new_prods
    return grammar


def limpar_gramatica(grammar):
    grammar = add_new_start_symbol(grammar)
    grammar = remove_epsilon_productions(grammar)
    grammar = remove_unit_productions(grammar)
    grammar = replace_terminals(grammar)
    grammar = binarize_productions(grammar)
    return grammar
