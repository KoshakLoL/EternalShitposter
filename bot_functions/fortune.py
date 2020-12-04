import subprocess


def fortune():
    return subprocess.check_output(['fortune', '-eso'])
