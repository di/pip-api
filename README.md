The official unofficial `pip` API.

## About

Since [`pip`](https://pypi.org/p/pip) is a command-line-tool, [it does not have
an official, supported, _importable_
API](https://pip.pypa.io/en/latest/user_guide/#using-pip-from-your-program).

However, this does not mean that people haven't tried to `import pip`, usually
to end up with much headache when `pip`'s maintainers do routine refactoring.

This project attempts to provide an importable `pip` API, which is _fully
compliant_ with the recommended method of using `pip` from your program.

## Supported Commands

Not all commands are supported in all versions of `pip` and on all platforms.
If the command you are trying to use is not compatible, `pip_api` will raise a
`pip_api.exceptions.Incompatible` exception for your program to catch.

### Available with all `pip` versions:
* `pip_api.version()`
  > Returns the `pip` version as a string, e.g. `"9.0.1"`

### Available with `pip>=8.0.0`:
* `pip_api.hash(filename, algorithm='sha256')`
  > Returns the resulting as a string.
  > Valid `algorithm` parameters are `'sha256'`, `'sha384'`, and `'sha512'`
