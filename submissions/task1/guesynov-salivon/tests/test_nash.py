import numpy as np
from nose.tools import assert_almost_equal
from nose_parameterized import parameterized

from nash.nash_equilibrium import nash_equilibrium

PLACES = 3

@parameterized([([[4,0,6,2,2,1],
      [3,8,4,10,4,4],
      [1,2,6,5,0,0],
      [6,6,4,4,10,3],
      [10,4,6,4,0,9],
      [10,7,0,7,9,8]],
      4.8709,
      [0, 0.12903226, 0.09677419, 0.43548387, 0.33870968, 0],
      [ 0., 0., 0.69086022, 0.14516129, 0.14784946, 0.01612903]
     ),
     ([[0,1,1],
        [1,1,1],
        [1,1,1]],
        1.0,
        [0, 1, 0],
        [1, 0, 0],
     ),
     ([[3,1],
       [1,3]],
       2,
       [0.5, 0.5],
       [0.5, 0.5]
     )
])
def test_nash_equilibrium(matrix, ev, ep, eq):
    matrix = np.array(matrix)
    v, p, q = nash_equilibrium(matrix)
    p, q = np.array(p), np.array(q)
    assert_almost_equal(v, ev, PLACES)
    np.testing.assert_array_almost_equal(p, ep, decimal=PLACES)
    np.testing.assert_array_almost_equal(q, eq, decimal=PLACES)
