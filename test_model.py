import pytest
from hypothesis import given
import hypothesis.strategies as st
import hypothesis.extra.numpy as hyp
from solveQuadratic import solve_quadratic
import readDensityDataFromFile as rddff

generic_float = st.floats(allow_nan=False, allow_infinity=False, min_value=-100000, max_value=100000)
zero_to_one = st.floats(allow_nan=False, allow_infinity=False, min_value=0, max_value=1)

@given(a=generic_float,
       b=generic_float,
       c=generic_float)
def test_quadratic(a, b, c):
    x_1, x_2 = solve_quadratic(a, b, c)
    if (x_1 is not None):
        assert a*x_1*x_1 + b*x_1 + c == pytest.approx(0, abs=1e-5)
        assert a*x_2*x_2 + b*x_2 + c == pytest.approx(0, abs=1e-5)


@given(ryds=hyp.arrays(zero_to_one, 10),
       electrons=hyp.arrays(zero_to_one, 10),
       volumes=hyp.arrays(zero_to_one, 10))
def test_find_widths_and_nums(ryds, electrons, volumes, total_desired_num_points):
    x_1, x_2 = rddff.find_widths_and_nums(ryds, electrons, volumes, total_desired_num_points)
    if (x_1 is not None):
        assert a*x_1*x_1 + b*x_1 + c == pytest.approx(0, abs=1e-5)
        assert a*x_2*x_2 + b*x_2 + c == pytest.approx(0, abs=1e-5)