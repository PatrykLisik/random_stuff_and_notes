import numpy as np


def pairs_to_memorize(memory_length, memory_number):
    """
    Generate random vectors of memories
    :param memory_length:
    :param memory_number: 
    :return: 
    """
    mean = 0
    var = 1 / np.sqrt(memory_length)
    mem_set1 = np.random.normal(loc=mean, scale=var, size=(memory_number * 2, memory_length))
    return mem_set1[::2], mem_set1[1::2]
