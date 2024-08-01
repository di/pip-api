import pytest


@pytest.mark.parametrize(
    "algorithm, expected",
    [
        ("sha256", "cce4031ec744585688ddab649427133ac22396da29ad82fdbd11692c3a26fe19"),
        (
            "sha384",
            "22101ffa84bad5c710c3b6eb719c4a2ac6546df2556bbe140e1fb4e628872af2344311662d4679088c12ab685c2e16dd",
        ),
        (
            "sha512",
            "73c8fa635bffa09eaf9ab70f22d289b3049e4906ff9e77bb24d247820f7f684c948daa77ed924e1851a71e40aea92e022fcf8092ff7c6197585289b42b60352b",
        ),
    ],
)
def test_hash(some_distribution, algorithm, expected, pip_api):
    if pip_api._hash.incompatible:
        pytest.xfail("Incompatible")

    result = pip_api.hash(some_distribution.filename, algorithm=algorithm)

    assert result == expected


def test_hash_default_algorithm_is_256(some_distribution, pip_api):
    if pip_api._hash.incompatible:
        pytest.xfail("Incompatible")

    sha256 = "cce4031ec744585688ddab649427133ac22396da29ad82fdbd11692c3a26fe19"

    assert pip_api.hash(some_distribution.filename) == sha256


def test_hash_invalid_algorithm(pip_api):
    if pip_api._hash.incompatible:
        pytest.xfail("Incompatible")

    with pytest.raises(pip_api.exceptions.InvalidArguments):
        pip_api.hash("whatever", "invalid")
