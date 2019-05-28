import os
import subprocess
import sys


def call(*args):
    python_location = os.environ.get("PIPAPI_PYTHON_LOCATION", sys.executable)
    result = subprocess.check_output([python_location, "-m", "pip"] + list(args))
    return result.decode()
