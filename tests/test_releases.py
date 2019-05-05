import pip_api


def test_get_latest():
    releases = pip_api.get_releases("tensorflow")
    assert len(releases) > 0


def test_latest_release():
    latest = pip_api.get_latest_release("tensorflow")
    releases = pip_api.get_releases("tensorflow")

    assert latest is not None
    assert releases[0] != latest or len(releases) == 0
