import os
import shutil
import subprocess

import pytest
import pretend
import virtualenv

from pip_api._vendor.packaging.version import Version

import pip_api


@pytest.yield_fixture
def some_distribution(data):
    return pretend.stub(
        name="dummyproject",
        version=Version("0.0.1"),
        location=None,
        filename=data.join("dummyproject-0.0.1.tar.gz"),
        editable=False,
    )


@pytest.yield_fixture
def tmpdir(tmpdir):
    """
    Return a temporary directory path object which is unique to each test
    function invocation, created as a sub directory of the base temporary
    directory. The returned object is a ``tests.lib.path.Path`` object.
    This uses the built-in tmpdir fixture from pytest itself but modified
    to return our typical path object instead of py.path.local as well as
    deleting the temporary directories at the end of each test case.
    """
    assert tmpdir.isdir()
    yield str(tmpdir)
    # Clear out the temporary directory after the test has finished using it.
    # This should prevent us from needing a multiple gigabyte temporary
    # directory while running the tests.
    shutil.rmtree(str(tmpdir))


class TestData:
    def __init__(self, data_location):
        self.data_location = data_location

    def join(self, *args):
        return os.path.join(self.data_location, *args)


@pytest.fixture
def data(tmpdir):
    data_location = os.path.join(tmpdir, "data")
    shutil.copytree(os.path.join(os.getcwd(), "tests", "data"), data_location)
    return TestData(data_location)


@pytest.fixture(autouse=True)
def isolate(tmpdir):
    """
    Isolate our tests so that things like global configuration files and the
    like do not affect our test results.
    We use an autouse function scoped fixture because we want to ensure that
    every test has it's own isolated home directory.
    """

    # Create a directory to use as our home location.
    home_dir = os.path.join(str(tmpdir), "home")
    os.makedirs(home_dir)

    # Set our home directory to our temporary directory, this should force
    # all of our relative configuration files to be read from here instead
    # of the user's actual $HOME directory.
    os.environ["HOME"] = home_dir

    # We want to disable the version check from running in the tests
    os.environ["PIP_DISABLE_PIP_VERSION_CHECK"] = "true"


@pytest.yield_fixture
def venv(tmpdir, isolate):
    """
    Return a virtual environment which is unique to each test function
    invocation created inside of a sub directory of the test function's
    temporary directory.
    """
    venv_location = os.path.join(str(tmpdir), "workspace", "venv")
    venv = virtualenv.create_environment(venv_location)

    os.environ["PIPAPI_PYTHON_LOCATION"] = os.path.join(venv_location, "bin", "python")

    yield venv

    del os.environ["PIPAPI_PYTHON_LOCATION"]
    shutil.rmtree(venv_location)


class PipTestEnvironment:
    def __init__(self):
        # Install the right version of pip. By default,
        # virtualenv gets the version from the wheels that
        # are bundled along with it
        self.run("install", "pip=={}".format(str(pip_api.PIP_VERSION)))

    def run(self, *args):
        python_location = os.environ["PIPAPI_PYTHON_LOCATION"]
        return subprocess.check_output(
            [python_location, "-m", "pip"] + list(args)
        ).decode("utf-8")


@pytest.fixture
def pip(tmpdir, venv):
    """
    Return a PipTestEnvironment which is unique to each test function and
    will execute all commands inside of the unique virtual environment for this
    test function. The returned object is a
    ``tests.lib.scripttest.PipTestEnvironment``.
    """
    return PipTestEnvironment()
