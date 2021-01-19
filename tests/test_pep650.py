import pytest

import pip_api._pep650

# Fully isolate all tests in this module
pytestmark = [pytest.mark.usefixtures("pip")]


@pytest.mark.parametrize(
    "requirements_file, dependency_group",
    [
        ("requirements.txt", None),
        ("requirements.txt", "requirements.txt"),
        ("some-other-requirements.txt", "some-other-requirements.txt"),
    ],
)
def test_invoke_install(tmpdir, some_distribution, requirements_file, dependency_group):
    tmpdir.join(requirements_file).write(some_distribution.filename)
    distributions = pip_api.installed_distributions()

    assert some_distribution.name not in distributions

    result = pip_api._pep650.invoke_install(
        str(tmpdir), dependency_group=dependency_group
    )
    distributions = pip_api.installed_distributions()

    assert result == 0
    assert some_distribution.name in distributions


def test_invoke_install_fails(tmpdir):
    tmpdir.join("requirements.txt").write("missing-distribution")

    result = pip_api._pep650.invoke_install(str(tmpdir))

    assert result == 1


@pytest.mark.parametrize(
    "requirements_file, dependency_group",
    [
        ("requirements.txt", None),
        ("requirements.txt", "requirements.txt"),
        ("some-other-requirements.txt", "some-other-requirements.txt"),
    ],
)
def test_invoke_uninstall(
    tmpdir, pip, some_distribution, requirements_file, dependency_group
):
    pip.run("install", some_distribution.filename)
    distributions = pip_api.installed_distributions()

    assert some_distribution.name in distributions

    tmpdir.join(requirements_file).write(some_distribution.name + "\n")
    result = pip_api._pep650.invoke_uninstall(
        str(tmpdir), dependency_group=dependency_group
    )
    distributions = pip_api.installed_distributions()

    assert result == 0
    assert some_distribution.name not in distributions


def test_invoke_uninstall_fails(tmpdir):
    result = pip_api._pep650.invoke_uninstall(
        str(tmpdir), dependency_group="missing.txt"
    )

    assert result == 1
