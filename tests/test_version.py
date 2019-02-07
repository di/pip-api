import pip_api

def test_version(pip):
    a = pip_api.version()
    b = pip.run('--version').split(' ')[1]

    assert a == b
