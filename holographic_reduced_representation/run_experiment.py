from src.experiment.experiment import conduct_experiment

if __name__ == '__main__':
    conduct_experiment(list(range(1,10)), [2, 4, 8, 512], 10)
