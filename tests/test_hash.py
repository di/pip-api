import pytest

import pip_api

xfail_incompatible = pytest.mark.xfail(
    pip_api._hash.incompatible, reason="Incompatible"
)


@xfail_incompatible
@pytest.mark.parametrize(
    "algorithm, expected",
    [
        ("sha256", "c3ebc5b7bc06d4466d339f4d8d1e61d1fdc256dd913d6d5752acea9ce5581a15"),
        (
            "sha384",
            "f2cf1e1a9235568adf0bd19ea41fff179c8f3cc1155ad9f806225a9fe3ea8ba57d3bda"
            "65bd90370aa681f1d4d9251dd8",
        ),
        (
            "sha512",
            "42444c9b60c49bf932562195d2f894e3031bbb8c11a22b414d335b2c862147377ec0c4"
            "eb718ac599eff2fac7ecf8333ca5cc0efc75c12965f0386bc1f6624a01",
        ),
    ],
)
def test_hash(some_distribution, algorithm, expected):
    result = pip_api.hash(some_distribution.filename, algorithm=algorithm)

    assert result == expected


@xfail_incompatible
def test_hash_default_algorithm_is_256(some_distribution):
    sha256 = "c3ebc5b7bc06d4466d339f4d8d1e61d1fdc256dd913d6d5752acea9ce5581a15"

    assert pip_api.hash(some_distribution.filename) == sha256


@xfail_incompatible
def test_hash_invalid_algorithm():
    with pytest.raises(pip_api.exceptions.InvalidArguments):
        pip_api.hash("whatever", "invalid")
