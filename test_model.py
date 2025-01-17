import pytest
import numpy as np
from hypothesis import given
import hypothesis.strategies as st
import hypothesis.extra.numpy as hyp
from mathUtils import solve_quadratic
import readDensityDataFromFile as rddff

generic_float = st.floats(allow_nan=False, allow_infinity=False, min_value=-100000, max_value=100000)
zero_to_five = st.floats(allow_nan=False, allow_infinity=False, min_value=0, max_value=5)
zero_to_one = st.floats(allow_nan=False, allow_infinity=False, min_value=0, max_value=1)
int_particles = st.integers(min_value=700, max_value=1000)


@given(a=generic_float,
       b=generic_float,
       c=generic_float)
def test_quadratic(a, b, c):
    x_1, x_2 = solve_quadratic(a, b, c)
    if (x_1 is not None):
        assert a*x_1*x_1 + b*x_1 + c == pytest.approx(0, abs=2e-5)
        assert a*x_2*x_2 + b*x_2 + c == pytest.approx(0, abs=2e-5)


@given(r_seed=hyp.arrays(np.float, 10, elements=zero_to_five),
       e_seed=hyp.arrays(np.float, 10, elements=zero_to_five),
       volumes=hyp.arrays(np.float, 10, elements=zero_to_one),
       total_desired_num_points=int_particles)
def test_find_widths_and_nums(printer, r_seed, e_seed, volumes, total_desired_num_points):
    # densities are expressed as a percentage of the total particles
    all_particles = (np.sum(r_seed) + np.sum(e_seed))
    if (all_particles == 0):
        return
    ryds = r_seed / all_particles
    electrons = e_seed / all_particles

    shell_widths, num_points_by_shell, num_ions_by_shell = \
        rddff.find_widths_and_nums(ryds, electrons, volumes, total_desired_num_points)

    # V = 4pi/3abc = pi/3 * a^3
    produced_volumes = ((np.pi) / 3) * (shell_widths ** 3)
    prev_vol = 0
    for index, p_volume in enumerate(produced_volumes):
        assert volumes[index] == pytest.approx(p_volume - prev_vol)
        prev_vol = p_volume

    assert np.sum(num_points_by_shell) == pytest.approx(total_desired_num_points, rel=0.15)
    proportion_ions = num_ions_by_shell / np.sum(num_points_by_shell)
    for index in range(len(proportion_ions)):
        assert proportion_ions[index] == pytest.approx(electrons[index], rel=0.1)
