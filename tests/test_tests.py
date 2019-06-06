import pytest

import pip_api


@pytest.mark.parametrize("should_be_installed", [True, False])
def test_isolation(pip, some_distribution, should_be_installed):
    """
    Test the isolation between tests. The first time this test is run, the
    package should be installed, the second time, it should not exist
    """

    if should_be_installed:
        pip.run("install", some_distribution.filename)

    installed = pip_api.installed_distributions()

    if should_be_installed:
        assert some_distribution.name in installed
    else:
        assert some_distribution.name not in installed


def test_all_the_right_pips(pip):
    a = str(pip_api.PIP_VERSION)
    b = pip_api.version()
    c = pip.run("--version").split(" ")[1]

    assert a == b
    assert b == c
