from pip_api._call import call


def hash(filename, algorithm='sha256'):
    if algorithm not in ['sha256', 'sha384', 'sha512']:
        raise Exception('Algorithm {} not supported'.format(algorithm))

    result = call('hash', '--algorithm', algorithm, filename)

    # result is of the form:
    # <filename>:\n--hash=<algorithm>:<hash>\n
    return result.strip().split(':')[-1]
