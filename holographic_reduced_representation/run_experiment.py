from src.experiment.experiment import conduct_associative_memory_experiment

if __name__ == '__main__':
    data_frame = conduct_associative_memory_experiment([x ** 5 for x in range(1, 3)], [x ** 2 for x in range(1, 12)], 10)
    data_frame.to_csv('./data/hrr.csv')
