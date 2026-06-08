import expecttest
import pytest
from PythonSE.ExamplePrograms.simple import simple

TIMEOUT = 5

class TestGeneratedSymbolicTests(expecttest.TestCase):

    @pytest.mark.timeout(TIMEOUT)
    def test_simple_generated_0(self):
        # path constraint: [x > y]
        result = simple(-2147483647, -2147483648)
        assert result == 1

    @pytest.mark.timeout(TIMEOUT)
    def test_simple_generated_1(self):
        # path constraint: [Not(x > y)]
        result = simple(-2147483648, -2147483648)
        assert result == 2
