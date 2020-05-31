import numpy as np


def circular_convolution(first_array, second_array):
    """
    Naive implementation of circular convolution based on T.Plate article
    :param first_array:
    :param second_array:
    :return: numpy array that it convolution of first and second array
    """

    first_len = len(first_array)
    second_length = len(second_array)
    convolved_array = np.zeros(second_length)
    for j in range(second_length):
        for k in range(first_len):
            convolved_array[j] += first_array[k % second_length] * second_array[(j - k) % second_length]
    return convolved_array


def circular_correlation(first_array, second_array):
    """
    Naive implementation of circular correlation based on T.Plate article
    :param first_array:
    :param second_array:
    :return: numpy array that it convolution of first and second array
    """

    first_len = len(first_array)
    correlated_array = np.zeros(first_len)
    for j in range(first_len):
        for k in range(len(second_array)):
            correlated_array[j] += first_array[k % first_len] * second_array[(j + k) % first_len]
    return correlated_array


def circular_convolution_fft(first_array, second_array):
    """
    Circular convolution implemented with fourier transform
    :param first_array: 
    :param second_array: 
    :return: 
    """
    return np.fft.ifft(np.multiply(np.fft.fft(first_array), np.fft.fft(second_array))).real


def involution(array):
    """
    Involution of array
    :param array: array to involve
    :return:
    """
    copied = array.copy()
    copied[1:] = copied[1:][::-1]
    return copied


def circular_correlation_fft(first_array, second_array):
    """
    Circular correlation implemented with fourier transform
    :param first_array:
    :param second_array:
    :return:
    """
    return circular_convolution_fft(involution(first_array), second_array)
