import os

import pytest
import pretend


@pytest.yield_fixture
def some_distribution():
    return pretend.stub(
        filename=os.path.join(
            os.getcwd(),
            'tests',
            'fixtures',
            'some-distribution-0.0.1.tar.gz',
        )
    )
