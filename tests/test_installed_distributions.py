import os
import pytest

import pip_api
from pip_api._vendor.packaging.version import parse
from pip_api.exceptions import PipError


PATH_SUPPORTED = pip_api.PIP_VERSION >= parse("19.2")
PATH_UNSUPPORTED_MSG = r"pip .* does not support the `paths` argument"


def test_installed_distributions(pip, some_distribution):
    distributions = pip_api.installed_distributions()

    assert some_distribution.name not in distributions

    pip.run("install", some_distribution.filename)

    distributions = pip_api.installed_distributions()

    assert some_distribution.name in distributions

    distribution = distributions[some_distribution.name]

    assert distribution.name == some_distribution.name
    assert distribution.version == some_distribution.version

    # Various versions of `pip` have different behavior here:
    # * `pip` 10.0.0b1 and newer include the `location` key in the JSON output
    # * `pip` 9.0.0 through 10.0.0b0 support JSON, but don't include `location`
    # * `pip` versions before 9.0.0 don't support JSON and don't include
    #   any location information in the textual output that we parse
    if pip_api.PIP_VERSION >= parse("10.0.0b0"):
        # We don't know exactly where the distribution has been installed,
        # but we know it exists and therefore is editable.
        assert os.path.exists(distribution.location)
        assert distribution.editable
    else:
        assert distribution.location is None
        assert not distribution.editable


def test_installed_distributions_legacy_version(pip, data):
    distributions = pip_api.installed_distributions()

    assert "dummyproject" not in distributions

    pip.run("install", data.join("dummyproject-0.23ubuntu1.tar.gz"))

    distributions = pip_api.installed_distributions()

    assert "dummyproject" in distributions
    assert distributions["dummyproject"].version == parse("0.23ubuntu1")


def test_installed_distributions_local(monkeypatch, pip):
    # Ideally, we'd be able to compare the value of `installed_distributions`
    # with and without the `local` flag. However, to test like this, we'd need
    # to globally-install a package to observe the difference.
    #
    # This isn't practical for the purposes of a unit test, so we'll have to
    # settle for checking that the `--local` flag gets passed in to the `pip`
    # invocation.
    original_call = pip_api._installed_distributions.call

    def mock_call(*args, cwd=None):
        assert "--local" in args
        return original_call(*args, cwd=cwd)

    monkeypatch.setattr(pip_api._installed_distributions, "call", mock_call)

    _ = pip_api.installed_distributions(local=True)


def test_installed_distributions_path(pip, some_distribution, target):
    distributions = pip_api.installed_distributions()
    assert some_distribution.name not in distributions

    # No packages installed under the target directory yet
    if PATH_SUPPORTED:
        distributions = pip_api.installed_distributions(paths=[target])
        assert some_distribution.name not in distributions
    else:
        with pytest.raises(PipError, match=PATH_UNSUPPORTED_MSG):
            pip_api.installed_distributions(paths=[target])

    # Install the package under the target directory
    pip.run("install", "--target", target, some_distribution.filename)

    # If we list packages without pointing `pip-api` to the target directory, we shouldn't find the
    # installed package
    distributions = pip_api.installed_distributions()
    assert some_distribution.name not in distributions

    # If we set the path to the target directory, we should find the installed package
    if PATH_SUPPORTED:
        distributions = pip_api.installed_distributions(paths=[target])
        assert some_distribution.name in distributions
    else:
        with pytest.raises(PipError, match=PATH_UNSUPPORTED_MSG):
            pip_api.installed_distributions(paths=[target])


def test_installed_distributions_multiple_paths(
    pip, some_distribution, other_distribution, target, other_target
):
    distributions = pip_api.installed_distributions()
    assert some_distribution.name not in distributions
    assert other_distribution.name not in distributions

    # No packages installed under the target directory yet
    if PATH_SUPPORTED:
        distributions = pip_api.installed_distributions(paths=[target, other_target])
        assert some_distribution.name not in distributions
        assert other_distribution.name not in distributions
    else:
        with pytest.raises(PipError, match=PATH_UNSUPPORTED_MSG):
            pip_api.installed_distributions(paths=[target, other_target])

    # Install the packages under the two target directories
    pip.run("install", "--target", target, some_distribution.filename)
    pip.run("install", "--target", other_target, other_distribution.filename)

    # If we list packages without pointing `pip-api` to the target directory, we shouldn't find the
    # installed package
    distributions = pip_api.installed_distributions()
    assert some_distribution.name not in distributions
    assert other_distribution.name not in distributions

    # If we set the path to the target directory, we should find the installed package
    if PATH_SUPPORTED:
        distributions = pip_api.installed_distributions(paths=[target, other_target])
        assert some_distribution.name in distributions
        assert other_distribution.name in distributions
    else:
        with pytest.raises(PipError, match=PATH_UNSUPPORTED_MSG):
            pip_api.installed_distributions(paths=[target, other_target])
