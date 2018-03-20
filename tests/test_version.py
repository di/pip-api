import pip_api


def test_version():
    result = pip_api.version()

    assert result == str(pip_api.PIP_VERSION)
