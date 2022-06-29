import pickle
import matplotlib.pyplot as plt


def main():
    with open('learning_curve', 'rb') as f:
        result = pickle.load(f)
        maximum_fitnesses = []
        average_fitnesses = []
        minimum_fitnesses = []
        for stat in result:
            maximum_fitnesses.append(stat[0])
            average_fitnesses.append(stat[1])
            minimum_fitnesses.append(stat[2])

        plt.plot(range(len(maximum_fitnesses)), maximum_fitnesses) 
        plt.plot(range(len(average_fitnesses)), average_fitnesses) 
        plt.plot(range(len(minimum_fitnesses)), minimum_fitnesses)
        
        plt.legend(['Maximum', 'Average', 'Minimum'])
        
        plt.show()

    
if __name__ == '__main__':
    main()