from random import choice


def shitpost():
    return (get_file_array("../array1.txt") +
            get_file_array("../array2.txt") +
            get_file_array("../array3.txt")).replace("\n", "")


def get_file_array(file):
    with open(file, "r") as array:
        return choice(list(array)) + " "
