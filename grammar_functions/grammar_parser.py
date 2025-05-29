def parse_grammar(file_path):
    grammar = {
        "variables": [],
        "start_symbol": "",
        "productions": {}
    }

    with open(file_path, "r") as file:
        lines = [line.strip() for line in file if line.strip()]

    # variáveis
    grammar["variables"] = lines[0].split()

    # símbolo inicial
    grammar["start_symbol"] = lines[1]

    # produções
    for line in lines[2:]:
        parts = line.split()
        left = parts[0]
        right = parts[1:]

        if left not in grammar["productions"]:
            grammar["productions"][left] = []

        grammar["productions"][left].append(right)

    return grammar
