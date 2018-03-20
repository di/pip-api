import subprocess


def call(*args):
    result = subprocess.check_output(
        ['python', '-m', 'pip'] + list(args)
    )
    return result.decode()
