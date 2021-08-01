from ..src.HRR.Memory import Memory
from ..src.experiment.experiment import generate_perfect_data


def test_revive_elements():
    # Hrr memory should correctly revive
    memory_length = 2048
    memories_number = 8
    memories1 = generate_perfect_data(memory_length=memory_length, memory_number=memories_number)
    memories2 = generate_perfect_data(memory_length=memory_length, memory_number=memories_number)
    hrr = Memory(memory_length)
    for mem1, mem2 in zip(memories1, memories2):
        hrr.associate_memories(mem1, mem2)

    for mem1, mem2 in zip(memories1, memories2):
        rev = hrr.revive_cleanup(mem2)
        assert mem1.tolist() == rev.tolist()

    for mem1, mem2 in zip(memories1, memories2):
        rev = hrr.revive_cleanup(mem1)
        assert mem2.tolist() == rev.tolist()
