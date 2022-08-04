import pytest
import inspect
import numpy as np
import control as ct

@pytest.mark.parametrize(
    "dt1, dt2, dt3", [
        (0, 0, 0),
        (0, 0.1, ValueError),
        (0, None, 0),
        (0.1, 0, ValueError),
        (0.1, 0.1, 0.1),
        (0.1, None, 0.1),
        (None, 0, 0),
        (None, 0.1, 0.1),
        (None, None, None),
        (0.2, None, 0.2),
        (0.2, 0.1, ValueError),
     ])
@pytest.mark.parametrize("op", [ct.series, ct.parallel, ct.feedback])
@pytest.mark.parametrize("type", [ct.StateSpace, ct.ss, ct.tf])
def test_composition(dt1, dt2, dt3, op, type):
    # Define the system
    A, B, C, D = [[1, 1], [0, 1]], [[0], [1]], [[1, 0]], 0
    sys1 = ct.StateSpace(A, B, C, D, dt1)
    sys2 = ct.StateSpace(A, B, C, D, dt2)

    # Convert to the desired form
    sys1 = type(sys1)
    sys2 = type(sys2)

    if inspect.isclass(dt3) and issubclass(dt3, Exception):
        with pytest.raises(dt3, match="incompatible timebases"):
            sys3 = op(sys1, sys2)
    else:
        sys3 = op(sys1, sys2)
        assert sys3.dt == dt3
