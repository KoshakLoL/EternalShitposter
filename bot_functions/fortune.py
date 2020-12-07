from random import choice


def fortune():
    with open("fortunes/fortunes", "r") as f:
        return choice(list(f)).rstrip()
