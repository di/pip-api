from packaging.version import Version

# import pip_api
from pip_api._call import call
from pip_api.exceptions import Incompatible

incompatible = False


class Distribution:

    def __init__(self, name, version, location=None):
        self.name = name
        self.version = Version(version)
        self.location = location
        self.editable = bool(self.location)

    def __repr__(self):
        return '<Distribution(name=\'{}\', version=\'{}\'{})>'.format(
            self.name,
            self.version,
            ", location=\'{}\'".format(self.location) if self.location else '',
        )


def installed_distributions():
    if incompatible:
        raise Incompatible

    result = call('list', '--format=legacy')

    # result is of the form:
    # <package_name> (<version>)
    #
    # or, if editable
    # <package_name> (<version>, <location>)

    ret = {}

    for line in result.strip().split('\n'):
        # Split on the first whitespace to get
        # split = ['<name>', '(<version>, <location>)']
        split = line.split(' ', 1)
        name = split[0]
        # Strip the first/last parens, then split on the ', ' which may be
        # between <version> and <location> (if not pad with None)
        version, location = (split[1][1:-1].split(', ') + [None])[:2]
        ret[name] = Distribution(name, version, location)

    return ret
