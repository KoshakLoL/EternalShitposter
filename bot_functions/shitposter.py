from random import choice


def shitpost():
    return (get_file_array("arrays/array1.txt") +
            get_file_array("arrays/array2.txt") +
            get_file_array("arrays/array3.txt")).replace("\n", "")


def get_file_array(file):
    with open(file, "r") as array:
        return choice(list(array)) + " "
