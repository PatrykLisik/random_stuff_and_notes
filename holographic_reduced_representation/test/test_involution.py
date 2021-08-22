from ..src.HRR.convolution_correlation import involution
import numpy as np

np.random.seed(2137)


def naive_involution(c):
    length = len(c)
    return [c[-i] for i in range(length)]


def test_small_array():
    array = np.array([0, 1, 2, 3])
    result = involution(array)
    expected = np.array([0, 3, 2, 1])
    assert ((expected == result).all())


def test_randomized_arrays():
    for _ in range(100):
        rand_len = np.random.randint(2, 2 ** 15)
        rand_vec = np.random.rand(rand_len)
        expected = np.array(naive_involution(rand_vec))
        result = involution(rand_vec)

        np.testing.assert_array_almost_equal(result, expected, decimal=5)


def test_no_side_effect():
    array1 = np.array([0, 1, 2, 3])
    array2 = array1.copy()
    involution(array1)
    assert (array1 == array2).all()
