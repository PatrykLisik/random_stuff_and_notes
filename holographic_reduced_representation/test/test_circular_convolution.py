import pytest
from ..src.HRR.convolution_correlation import circular_convolution, \
    circular_convolution_fft
import numpy as np

np.random.seed(2137)


def generate_arrays():
    arrays = np.random.rand(50, 3)
    for first_array in arrays:
        for second_array in arrays:
            yield first_array, second_array


def naive_convolution(array1, array2):
    """
    Naive convolution for 3-elem,nts array
    :param array1:
    :param array2:
    :return:
    """
    convolved1 = array2[0] * array1[0] + array2[1] * array1[2] + array2[2] * array1[1]
    convolved2 = array2[0] * array1[1] + array2[1] * array1[0] + array2[2] * array1[2]
    convolved3 = array2[0] * array1[2] + array2[1] * array1[1] + array2[2] * array1[0]
    return [convolved1, convolved2, convolved3]


@pytest.mark.parametrize("array1, array2", generate_arrays())
def test_circular_convolution(array1, array2):
    result = np.array(circular_convolution(array1, array2))
    expected = np.array(naive_convolution(array1, array2))
    np.testing.assert_array_almost_equal(result, expected, decimal=5)


@pytest.mark.parametrize("array1, array2", generate_arrays())
def test_circular_convolution_fft(array1, array2):
    result = np.array(circular_convolution_fft(array1, array2))
    expected = np.array(naive_convolution(array1, array2))
    np.testing.assert_array_almost_equal(result, expected, decimal=5)


@pytest.mark.parametrize("array1, array2", generate_arrays())
def test_commutativity_convolution(array1, array2):
    result = np.array(circular_convolution(array1, array2))
    expected = np.array(circular_convolution(array2, array1))
    np.testing.assert_array_almost_equal(result, expected, decimal=5)


def test_commutativity_fft_convolution():
    for array1, array2 in generate_arrays():
        result = np.array(circular_convolution_fft(array1, array2))
        expected = np.array(circular_convolution_fft(array2, array1))
        np.testing.assert_array_almost_equal(result, expected, decimal=5)
