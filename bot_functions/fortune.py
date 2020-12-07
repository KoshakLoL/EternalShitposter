from random import choice


def fortune(fortunes, limit):
    with open(choice(fortunes), "r") as f:
        lines = list(f)
        while True:
            line = choice(lines)
            if len(line)-1 < limit:
                return line.rstrip()
