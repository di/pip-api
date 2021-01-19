import pip_api


def test_version(pip):
    from_api = pip_api.version()
    from_call = pip.run("--version").split()[1]
    from_import = str(pip_api.PIP_VERSION)

    assert from_api == from_call == from_import
