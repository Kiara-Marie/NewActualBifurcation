import pytest
from hypothesis import given
import hypothesis.strategies as st
from solveQuadratic import solve_quadratic


@given(a=st.floats(allow_nan=False, allow_infinity=False, min_value=-100000, max_value=100000),
       b=st.floats(allow_nan=False, allow_infinity=False, min_value=-100000, max_value=100000),
       c=st.floats(allow_nan=False, allow_infinity=False, min_value=-100000, max_value=100000))
def test_quadratic(a, b, c):
    x_1, x_2 = solve_quadratic(a, b, c)
    if (x_1 is not None):
        assert a*x_1*x_1 + b*x_1 + c == pytest.approx(0, abs=1e-8)
        assert a*x_2*x_2 + b*x_2 + c == pytest.approx(0, abs=1e-8)
