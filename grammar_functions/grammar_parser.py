def parse_grammar(file_path):
    grammar = {
        "variaveis": [],
        "simbolo_inicial": "",
        "producoes": {}
    }

    with open(file_path, "r") as file:
        lines = [line.strip() for line in file if line.strip()]

    # variáveis
    grammar["variaveis"] = lines[0].split()

    # símbolo inicial
    grammar["simbolo_inicial"] = lines[1]

    # produções
    for line in lines[2:]:
        parts = line.split()
        left = parts[0]
        right = parts[1:]

        if left not in grammar["producoes"]:
            grammar["producoes"][left] = []

        grammar["producoes"][left].append(right)

    return grammar


def write_grammar(grammar, file_path):
    with open(file_path, 'w') as f:
        # variaveis
        f.write(' '.join(grammar['variaveis']) + '\n')
        # simbolo inicial
        f.write(grammar['simbolo_inicial'] + '\n')
        # producoes
        for A in grammar['variaveis']:
            for r in grammar['producoes'].get(A, []):
                line = A + ' ' + ' '.join(r if r else ['h'])
                f.write(line + '\n')
