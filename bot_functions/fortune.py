from random import choice


def fortune():
    with open("fortunes/fortunes.txt", "r") as f:
        return choice(list(f)[:-1]).rstrip()
