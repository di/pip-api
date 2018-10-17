import argparse
import os
import re
import traceback
try:  # py27
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin
try:  # py27
    from urllib.request import pathname2url
except ImportError:
    from urllib import pathname2url

import packaging.requirements
import packaging.specifiers

from pip_api.exceptions import PipError

parser = argparse.ArgumentParser()
parser.add_argument("req", nargs="?")
parser.add_argument("-r", "--requirements")
parser.add_argument("-e", "--editable")

operators = packaging.specifiers.Specifier._operators.keys()


def _read_file(filename):
    with open(filename) as f:
        return f.readlines()


def _check_invalid_requirement(req):
    if os.path.sep in req:
        add_msg = "It looks like a path."
        if os.path.exists(req):
            add_msg += " It does exist."
        else:
            add_msg += " File '%s' does not exist." % (req)
    elif "=" in req and not any(op in req for op in operators):
        add_msg = "= is not a valid operator. Did you mean == ?"
    else:
        add_msg = traceback.format_exc()
    raise PipError("Invalid requirement: '%s'\n%s" % (req, add_msg))


def _strip_extras(path):
    m = re.match(r'^(.+)(\[[^\]]+\])$', path)
    extras = None
    if m:
        path_no_extras = m.group(1)
        extras = m.group(2)
    else:
        path_no_extras = path

    return path_no_extras, extras


def _egg_fragment(url):
    _egg_fragment_re = re.compile(r'[#&]egg=([^&]*)')
    match = _egg_fragment_re.search(url)
    if not match:
        return None
    return match.group(1)


def _path_to_url(path):
    path = os.path.normpath(os.path.abspath(path))
    url = urljoin('file:', pathname2url(path))
    return url


def _parse_editable(editable_req):
    url = editable_req

    # If a file path is specified with extras, strip off the extras.
    url_no_extras, extras = _strip_extras(url)

    if os.path.isdir(url_no_extras):
        if not os.path.exists(os.path.join(url_no_extras, 'setup.py')):
            raise PipError(
                "Directory %r is not installable. File 'setup.py' not found." %
                url_no_extras
            )
        # Treating it as code that has already been checked out
        url_no_extras = _path_to_url(url_no_extras)

    if url_no_extras.lower().startswith('file:'):
        return

    if '+' not in url:
        raise PipError(
            '%s should either be a path to a local project or a VCS url '
            'beginning with svn+, git+, hg+, or bzr+' %
            editable_req
        )

    package_name = _egg_fragment(url)
    if not package_name:
        raise PipError(
            "Could not detect requirement name for '%s', please specify one "
            "with #egg=your_package_name" % editable_req
        )


def _filterfalse(predicate, iterable):
    if predicate is None:
        predicate = bool
    for x in iterable:
        if not predicate(x):
            yield x


def _skip_regex(lines_enum, options):
    skip_regex = options.skip_requirements_regex if options else None
    if skip_regex:
        pattern = re.compile(skip_regex)
        lines_enum = _filterfalse(lambda e: pattern.search(e[1]), lines_enum)
    return lines_enum


def parse_requirements(filename, options=None):
    to_parse = {filename}
    parsed = set()
    name_to_req = {}

    while to_parse:
        filename = to_parse.pop()
        parsed.add(filename)

        # Combine multi-line commands
        lines = "".join(_read_file(filename)).replace("\\\n", "").splitlines()
        lines_enum = enumerate(lines, 1)
        lines_enum = _skip_regex(lines_enum, options)

        for lineno, line in lines_enum:
            known, _ = parser.parse_known_args(line.strip().split())
            if known.req:
                try:  # Try to parse this as a requirement specification
                    req = packaging.requirements.Requirement(known.req)
                except packaging.requirements.InvalidRequirement:
                    _check_invalid_requirement(known.req)

                req.comes_from = "-r {} (line {})".format(filename, lineno)
                if req.name not in name_to_req:
                    name_to_req[req.name.lower()] = req
                else:
                    raise PipError(
                        "Double requirement given: %s (already in %s, name=%r)"
                        % (req, name_to_req[req.name], req.name)
                    )
            elif known.requirements:
                if known.requirements not in parsed:
                    to_parse.add(known.requirements)
            elif known.editable:
                _parse_editable(known.editable)
            else:
                pass  # This is an invalid requirement

    return name_to_req
