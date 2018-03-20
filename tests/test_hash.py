import pytest

import pip_api


@pytest.mark.parametrize('algorithm, expected', [
    (
        'sha256',
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
    ),
    (
        'sha384',
        '38b060a751ac96384cd9327eb1b1e36a21fdb71114be07434c0cc7bf63f6e1da274ed'
        'ebfe76f65fbd51ad2f14898b95b',
    ),
    (
        'sha512',
        'cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d'
        '13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e',
    ),
])
def test_hash(some_distribution, algorithm, expected):
    result = pip_api.hash(some_distribution.filename, algorithm=algorithm)

    assert result == expected


def test_hash_default_algorithm_is_256(some_distribution):
    sha256 = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'

    assert pip_api.hash(some_distribution.filename) == sha256


def test_hash_invalid_algorithm():
    with pytest.raises(Exception):
        pip_api.hash('whatever', 'invalid')
