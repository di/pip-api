import pip_api
from pip_api._vendor.packaging.version import parse


def test_installed_distributions(pip, some_distribution):
    distributions = pip_api.installed_distributions()

    assert some_distribution.name not in distributions

    pip.run("install", some_distribution.filename)

    distributions = pip_api.installed_distributions()

    assert some_distribution.name in distributions

    distribution = distributions[some_distribution.name]

    assert distribution.name == some_distribution.name
    assert distribution.version == some_distribution.version
    assert distribution.location == some_distribution.location
    assert distribution.editable == some_distribution.editable


def test_installed_distributions_legacy_version(pip, data):
    distributions = pip_api.installed_distributions()

    assert "dummyproject" not in distributions

    pip.run("install", data.join("dummyproject-0.23ubuntu1.tar.gz"))

    distributions = pip_api.installed_distributions()

    assert "dummyproject" in distributions
    assert distributions["dummyproject"].version == parse("0.23ubuntu1")
