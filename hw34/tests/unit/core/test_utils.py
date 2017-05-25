import pytest
from roadmap.utils import dev


class TestDev:

    @pytest.fixture()
    def gen_5(self):
        return 5

    @pytest.fixture()
    def gen_2(self):
        return 2

    @pytest.fixture()
    def gen_1(self):
        return 1

    @pytest.fixture()
    def gen_0(self):
        return 0

    def test_zero(self):
        result = dev(5,0)
        assert result is None

    def test_success(self, gen_5, gen_2):
        result = dev(float(gen_5), float(gen_2))
        assert result == 2.5


