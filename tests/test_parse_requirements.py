import pytest

import pip_api


def test_parse_requirements(monkeypatch):
    files = {
        'a.txt': [
            'foo==1.2.3\n',
        ],
    }
    monkeypatch.setattr(pip_api._parse_requirements, '_read_file', files.get)

    result = pip_api.parse_requirements('a.txt')

    assert set(result) == {'foo'}
    assert str(result['foo']) == 'foo==1.2.3'


def test_parse_requirements_with_comments(monkeypatch):
    files = {
        'a.txt': [
            '# a comment\n',
            'foo==1.2.3 # this is a comment\n',
        ],
    }
    monkeypatch.setattr(pip_api._parse_requirements, '_read_file', files.get)

    result = pip_api.parse_requirements('a.txt')

    assert set(result) == {'foo'}
    assert str(result['foo']) == 'foo==1.2.3'


@pytest.mark.parametrize('flag', ['-r', '--requirements'])
def test_parse_requirements_recursive(monkeypatch, flag):
    files = {
        'a.txt': [
            '{} b.txt\n'.format(flag),
        ],
        'b.txt': [
            'foo==1.2.3\n',
        ],
    }
    monkeypatch.setattr(pip_api._parse_requirements, '_read_file', files.get)

    result = pip_api.parse_requirements('a.txt')

    assert set(result) == {'foo'}
    assert str(result['foo']) == 'foo==1.2.3'


def test_parse_requirements_double_raises(monkeypatch):
    files = {
        'a.txt': [
            'foo==1.2.3\n',
            'foo==3.2.1\n',
        ],
    }
    monkeypatch.setattr(pip_api._parse_requirements, '_read_file', files.get)

    with pytest.raises(pip_api.exceptions.PipError) as e:
        pip_api.parse_requirements('a.txt')

    assert e.value.args == (
        "Double requirement given: foo==3.2.1 (already in foo==1.2.3, name='foo')",  # noqa
    )


@pytest.mark.parametrize("lines", (
    ['foo==1.2.3 \\\n', '    --whatever=blahblah\n'],
    ['-r \\\n', '    b.txt\n'],
))
def test_parse_requirements_multiline(monkeypatch, lines):
    files = {
        'a.txt': lines,
        'b.txt': [
            'foo==1.2.3\n',
        ],
    }
    monkeypatch.setattr(pip_api._parse_requirements, '_read_file', files.__getitem__)

    result = pip_api.parse_requirements('a.txt')

    assert set(result) == {'foo'}
    assert str(result['foo']) == 'foo==1.2.3'


def test_parse_requirements_editable(monkeypatch):
    files = {
        'a.txt': [
            "Django==1.11\n"
            "-e git+https://github.com/foo/deal.git#egg=deal\n"
        ],
    }
    monkeypatch.setattr(pip_api._parse_requirements, '_read_file', files.get)

    result = pip_api.parse_requirements('a.txt')

    assert set(result) == {'django', 'deal'}
    assert str(result['django']) == 'Django==1.11'
    assert str(result['deal']) == 'deal@ git+https://github.com/foo/deal.git#egg=deal'
