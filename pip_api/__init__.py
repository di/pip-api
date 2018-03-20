import sys

import packaging.version

# Import this now because we need it below
from pip_api._version import version

PIP_VERSION = packaging.version.parse(version())
PYTHON_VERSION = sys.version_info

# Import these because they depend on the above
from pip_api._hash import hash  # noqa
