import pytest

import pip_api

xfail_incompatible = pytest.mark.xfail(
    pip_api._hash.incompatible, reason="Incompatible"
)


@xfail_incompatible
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
def test_hash(some_distribution, algorithm, expected):
    result = pip_api.hash(some_distribution.filename, algorithm=algorithm)

    assert result == expected


@xfail_incompatible
def test_hash_default_algorithm_is_256(some_distribution):
    sha256 = "cce4031ec744585688ddab649427133ac22396da29ad82fdbd11692c3a26fe19"

    assert pip_api.hash(some_distribution.filename) == sha256


@xfail_incompatible
def test_hash_invalid_algorithm():
    with pytest.raises(pip_api.exceptions.InvalidArguments):
        pip_api.hash("whatever", "invalid")
