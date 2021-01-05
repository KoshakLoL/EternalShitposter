from random import choice


def shitpost():
    array = []
    for i in range(1, 4):
        with open(f"arrays/array{i}.txt", "r") as f:
            array.append(choice(list(f)).strip())
    return " ".join(array)
