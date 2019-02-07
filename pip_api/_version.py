from pip_api._call import call

_VERSION = None


def version():
    global _VERSION
    if not _VERSION:
        result = call('--version')

        # result is of the form:
        # pip <version> from <directory> (python <python version>)

        _VERSION = result.split(' ')[1]

    return _VERSION
