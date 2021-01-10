from random import choice


def fortune():
    with open("arrays/fortunes.txt", "r") as f:
        return choice(list(f)[:-1]).strip()
