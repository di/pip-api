import sys

import packaging.version

# Import this now because we need it below
from pip_api._version import version

PIP_VERSION = packaging.version.parse(version())
PYTHON_VERSION = sys.version_info

# Import these because they depend on the above
from pip_api._hash import hash  # noqa
from pip_api._installed_distributions import (  # noqa
    installed_distributions
)

# Import these whenever, doesn't matter
from pip_api._parse_requirements import parse_requirements  # noqa
