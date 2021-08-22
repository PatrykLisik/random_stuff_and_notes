from src.experiment.experiment import conduct_associative_memory_experiment

if __name__ == '__main__':

    print("small count")
    data_frame = conduct_associative_memory_experiment(list(range(1, 15)), list(range(10, 350, 10)), 10000)
    data_frame.to_csv('./data/hrr_small_count2.csv')

    print("big count")
    data_frame = conduct_associative_memory_experiment(list(range(100, 1000, 100)), list(range(10, 18015, 2000)), 500)
    data_frame.to_csv('./data/hrr_big_count2.csv')
