import itertools

import numpy as np
import pandas as pd

from collections.abc import Callable

from numpy import iterable

from ..HRR.Memory import Memory as HRRMemory
from ..jupyter_tools import update_progress


def generate_perfect_data(memory_length: int, memory_number: int) -> np.array:
    mean = 0
    var = 1 / np.sqrt(memory_length)
    return np.random.normal(loc=mean, scale=var, size=(memory_number, memory_length))


def _conduct_single_memorize_revive_experiment(memory_length: int, pairs_count: int,
                                               memories_generator: Callable[[int, int], iterable]) -> pd.DataFrame:
    hrr = HRRMemory(memory_length)
    memories1 = memories_generator(memory_length, pairs_count)
    memories2 = memories_generator(memory_length, pairs_count)

    # Fill hrr
    for mem1, mem2 in zip(memories1, memories2):
        hrr.associate_memories(mem1, mem2)

    # revive
    rev1_correct = [(mem1 == hrr.revive_cleanup(mem2)).all() for mem1, mem2 in zip(memories1, memories2)]
    rev2_correct = [(mem2 == hrr.revive_cleanup(mem1)).all() for mem1, mem2 in zip(memories1, memories2)]

    df2 = pd.DataFrame(columns=["correct_revive"])
    df2["correct_revive"] = rev1_correct + rev2_correct
    return df2


def conduct_experiment(paris_counts, memory_lengths, revive_number):
    df = pd.DataFrame(columns=[])
    params = list(itertools.product(paris_counts, memory_lengths))
    params_count = len(params)
    for index, param in enumerate(params):
        pairs, memory_len = param
        probe_count = int(np.ceil(revive_number / (2 * pairs)))
        for probe_id in range(probe_count):
            test_df = _conduct_single_memorize_revive_experiment(memory_len, pairs, generate_perfect_data)
            test_df["probe_id"] = probe_id
            test_df["memorized_pairs"] = pairs
            test_df["memory_length"] = memory_len
            df = df.append(test_df, ignore_index=True)
        update_progress(index / params_count)
    update_progress(1)
    return df
