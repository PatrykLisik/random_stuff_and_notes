import numpy as np
from .convolution_correlation import circular_convolution_fft as cconv
from .convolution_correlation import circular_correlation_fft as ccor
from .convolution_correlation import cosine_distance as cos_distance


# from scipy.spatial.distance import cosine as cos_distance


class Memory:
    """
    Holographic reduced representations abstracted out to class
    """

    __slots__ = ['trace', 'clean_up']

    def __init__(self, memory_length: int):
        self.trace = np.zeros(shape=memory_length)
        self.clean_up = []

    def associate_memories(self, memory1: list, memory2: list):
        """
        Save association between two memories
        :param memory1: list of floats that represents memory
        :param memory2: list of floats that represents memory
        """
        self.trace += cconv(memory1, memory2)
        self.clean_up.extend([memory2, memory1])

    def revive(self, memory: list) -> list:
        """
        Get memory associated with given memory.
        :param memory: list of floats that represents memory
        :return: list of floats that should be the closest cosine distance to
        """
        return ccor(memory, self.trace)

    def revive_cleanup(self, memory: list) -> list:
        """
        Get memory associated with given memory.
        :param memory: list of floats that represents memory
        :return: list of floats that represents reviewed memory
        """
        revived = self.revive(memory)
        ret = min(self.clean_up, key=lambda vec: cos_distance(vec, revived))
        return ret
