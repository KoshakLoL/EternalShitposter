import subprocess


def fortune():
    return subprocess.run(['fortune', '-eso'], capture_output=True, text=True).stdout
