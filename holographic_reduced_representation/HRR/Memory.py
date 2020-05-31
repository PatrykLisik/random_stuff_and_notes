import numpy as np
from .convolution_correlation import circular_convolution_fft as cconv
from .convolution_correlation import circular_correlation_fft as ccor
from scipy.spatial.distance import cosine as cos_distance


class Memory:
    """
    Holographic reduced representations abstracted out to class
    """

    __slots__ = ['trace', 'clean_up']

    def __init__(self, memory_length):
        self.trace = np.zeros(shape=memory_length)
        self.clean_up = []

    def associate_memories(self, memory1, memory2):
        """
        Save association between two memories
        :param memory1:
        :param memory2:
        :return:
        """
        self.trace += cconv(memory1, memory2)
        self.clean_up.extend([memory2, memory1])

    def revive(self, memory):
        """
        Get memory associated with given memory
        :param memory:
        :return:
        """
        return ccor(memory, self.trace)

    def revive_cleanup(self, memory):
        """
        Get memory associated with given memory
        :param memory:
        :return:
        """
        rev = self.revive(memory)
        ret = min(self.clean_up, key=lambda vec: cos_distance(vec, rev))
        return ret
