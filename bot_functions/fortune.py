from python_fortune import main


def fortune():
    return main.Fortune(["fortunes/aphorisms", "fortunes/zippy", "fortunes/groucho"]).get()
