from textwrap import dedent

import pytest

import pip_api
from pip_api.exceptions import PipError


def test_parse_requirements(monkeypatch):
    files = {"a.txt": ["foo==1.2.3\n"]}
    monkeypatch.setattr(pip_api._parse_requirements, "_read_file", files.get)

    result = pip_api.parse_requirements("a.txt")

    assert set(result) == {"foo"}
    assert str(result["foo"]) == "foo==1.2.3"


def test_parse_requirements_with_comments(monkeypatch):
    files = {"a.txt": ["# a comment\n", "foo==1.2.3 # this is a comment\n"]}
    monkeypatch.setattr(pip_api._parse_requirements, "_read_file", files.get)

    result = pip_api.parse_requirements("a.txt")

    assert set(result) == {"foo"}
    assert str(result["foo"]) == "foo==1.2.3"


@pytest.mark.parametrize(
    "flag", ["-i", "--index-url", "--extra-index-url", "-f", "--find-links"]
)
def test_parse_requirements_with_index_url(monkeypatch, flag):
    files = {
        "a.txt": ["{} https://example.com/pypi/simple\n".format(flag), "foo==1.2.3\n"]
    }
    monkeypatch.setattr(pip_api._parse_requirements, "_read_file", files.get)

    result = pip_api.parse_requirements("a.txt")

    assert set(result) == {"foo"}
    assert str(result["foo"]) == "foo==1.2.3"


PEP508_PIP_EXAMPLE_URL = (
    "https://github.com/pypa/pip/archive/1.3.1.zip"
    "#sha1=da9234ee9982d4bbb3c72346a6de940a148ea686"
)


@pytest.mark.parametrize(
    "line, result_set, url, string, spec",
    [
        ("pip @ {url}\n".format(url=PEP508_PIP_EXAMPLE_URL), {"pip"}, None, "pip", ""),
        (
            "pip==1.3.1 @ {url}\n".format(url=PEP508_PIP_EXAMPLE_URL),
            {"pip"},
            None,
            "pip==1.3.1",
            "==1.3.1",
        ),
        (
            "pip@{url}\n".format(url=PEP508_PIP_EXAMPLE_URL),
            {"pip"},
            PEP508_PIP_EXAMPLE_URL,
            "pip@ " + PEP508_PIP_EXAMPLE_URL,  # Note extra space after @
            "",
        ),
        (
            "pip==1.3.1@{url}\n".format(url=PEP508_PIP_EXAMPLE_URL),
            {"pip"},
            None,
            "pip==1.3.1@" + PEP508_PIP_EXAMPLE_URL,  # Note no extra space after @
            "==1.3.1@" + PEP508_PIP_EXAMPLE_URL,
        ),
    ],
)
def test_parse_requirements_PEP508(monkeypatch, line, result_set, url, string, spec):
    files = {"a.txt": [line]}
    monkeypatch.setattr(pip_api._parse_requirements, "_read_file", files.get)

    result = pip_api.parse_requirements("a.txt")

    assert set(result) == result_set
    assert result["pip"].url == url
    assert str(result["pip"]) == string
    assert result["pip"].specifier == spec


def test_parse_requirements_vcs(monkeypatch):
    requirement_text = "git+https://github.com/bar/foo"
    files = {"a.txt": [requirement_text + "\n"]}
    monkeypatch.setattr(pip_api._parse_requirements, "_read_file", files.get)

    with pytest.raises(PipError):
        pip_api.parse_requirements("a.txt")


def test_include_invalid_requirement(monkeypatch):
    requirement_text = "git+https://github.com/bar/foo"
    files = {"a.txt": [requirement_text + "\n"]}
    monkeypatch.setattr(pip_api._parse_requirements, "_read_file", files.get)

    result = pip_api.parse_requirements("a.txt", include_invalid=True)

    assert set(result) == {requirement_text}
    assert result[requirement_text].name == requirement_text
    assert (
        str(result[requirement_text])
        == dedent(
            """
        Invalid requirement: '{requirement_text}'
        It looks like a path. File '{requirement_text}' does not exist.
        """.format(
                requirement_text=requirement_text
            )
        ).strip()
    )


@pytest.mark.parametrize("flag", ["-r", "--requirements"])
def test_parse_requirements_recursive(monkeypatch, flag):
    files = {"a.txt": ["{} b.txt\n".format(flag)], "b.txt": ["foo==1.2.3\n"]}
    monkeypatch.setattr(pip_api._parse_requirements, "_read_file", files.get)

    result = pip_api.parse_requirements("a.txt")

    assert set(result) == {"foo"}
    assert str(result["foo"]) == "foo==1.2.3"


def test_parse_requirements_double_raises(monkeypatch):
    files = {"a.txt": ["foo==1.2.3\n", "foo==3.2.1\n"]}
    monkeypatch.setattr(pip_api._parse_requirements, "_read_file", files.get)

    with pytest.raises(pip_api.exceptions.PipError) as e:
        pip_api.parse_requirements("a.txt")

    assert e.value.args == (
        "Double requirement given: foo==3.2.1 (already in foo==1.2.3, name='foo')",
    )


@pytest.mark.parametrize(
    "lines",
    (["foo==1.2.3 \\\n", "    --whatever=blahblah\n"], ["-r \\\n", "    b.txt\n"]),
)
def test_parse_requirements_multiline(monkeypatch, lines):
    files = {"a.txt": lines, "b.txt": ["foo==1.2.3\n"]}
    monkeypatch.setattr(pip_api._parse_requirements, "_read_file", files.__getitem__)

    result = pip_api.parse_requirements("a.txt")

    assert set(result) == {"foo"}
    assert str(result["foo"]) == "foo==1.2.3"


def test_parse_requirements_editable(monkeypatch):
    files = {
        "a.txt": ["Django==1.11\n" "-e git+https://github.com/foo/deal.git#egg=deal\n"]
    }
    monkeypatch.setattr(pip_api._parse_requirements, "_read_file", files.get)

    result = pip_api.parse_requirements("a.txt")

    assert set(result) == {"django", "deal"}
    assert str(result["django"]) == "Django==1.11"
    assert str(result["deal"]) == "deal@ git+https://github.com/foo/deal.git#egg=deal"


def test_parse_requirements_editable_file(monkeypatch):
    files = {"a.txt": ["Django==1.11\n" "-e .\n"]}
    monkeypatch.setattr(pip_api._parse_requirements, "_read_file", files.get)

    result = pip_api.parse_requirements("a.txt")

    assert set(result) == {"django", "pip-api"}
    assert str(result["django"]) == "Django==1.11"
    assert str(result["pip-api"]).startswith("pip-api@ file:///")


def test_parse_requirements_with_relative_references(monkeypatch):
    files = {
        "reqs/base.txt": ["django==1.11\n"],
        "reqs/test.txt": ["-r base.txt\n"],
        "reqs/dev.txt": ["-r base.txt\n" "-r test.txt\n"],
    }
    monkeypatch.setattr(pip_api._parse_requirements, "_read_file", files.get)

    result = pip_api.parse_requirements("reqs/dev.txt")
    assert set(result) == {"django"}
