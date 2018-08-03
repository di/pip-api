import os
import subprocess


def call(*args):
    python_location = os.environ.get('PIPAPI_PYTHON_LOCATION', 'python')
    result = subprocess.check_output(
        [python_location, '-m', 'pip'] + list(args)
    )
    return result.decode()
