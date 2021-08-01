from src.experiment.experiment import conduct_associative_memory_experiment

if __name__ == '__main__':

    data_frame = conduct_associative_memory_experiment(list(range(1, 15)), list(range(10, 350, 10)), 100)
    data_frame.to_csv('./data/hrr_small_count.csv')
