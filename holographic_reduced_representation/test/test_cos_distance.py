import numpy as np
import pytest
from ..src.HRR.convolution_correlation import cosine_distance


@pytest.mark.parametrize("array1, array2, expected",
                         [
                             [[1, 0, 0], [0, 1, 0], 1.0],
                             [[100, 0, 0], [0, 1, 0], 1.0],
                             [[1, 1, 0], [0, 1, 0], 0.292893],
                             [[1, 1, 0], [1, 1, 0], 0.0],

                         ])
def test_cos_distance(array1, array2, expected):
    result = cosine_distance(array1, array2)
    np.testing.assert_array_almost_equal(expected, result)
