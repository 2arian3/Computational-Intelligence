import copy
import random
import numpy as np

from player import Player


class Evolution:
    def __init__(self):
        self.game_mode = "Neuroevolution"
        self.mutation_rate = 0.1

    def next_population_selection(self, players, num_players):
        """
        Gets list of previous and current players (μ + λ) and returns num_players number of players based on their
        fitness value.

        :param players: list of players in the previous generation
        :param num_players: number of players that we return
        """
        next_population = players[:num_players]
        next_population = self.stochastic_universal_sampling(players, num_players)

        # TODO (Additional: Learning curve)
        return next_population

    def generate_new_population(self, num_players, prev_players=None):
        """
        Gets survivors and returns a list containing num_players number of children.

        :param num_players: Length of returning list
        :param prev_players: List of survivors
        :return: A list of children
        """
        first_generation = prev_players is None
        if first_generation:
            return [Player(self.game_mode) for _ in range(num_players)]
        else:
            parents = self.q_tournament_selection(prev_players, num_players)
            random.shuffle(parents)
            
            new_players = []
            for i in range(0, len(parents), 2) :
                new_players += self.create_children(parents[i], parents[i+1])
            return new_players

    def clone_player(self, player):
        """
        Gets a player as an input and produces a clone of that player.
        """
        new_player = Player(self.game_mode)
        new_player.nn = copy.deepcopy(player.nn)
        new_player.fitness = player.fitness
        return new_player
    
    def select_top_k_players(self, players, k):
        """
        Gets a list of players and returns the top k players.
        """
        return sorted(players, key=lambda player: player.fitness, reverse=True)[:k]
    
    def roulette_wheel_selection(self, players, k):
        """
        Gets a list of players and returns the top k players.
        """
        selected_players = []
        fits = list(np.cumsum(list(map(lambda i: i.fitness, players))))
        for i in range(k):
            random_number = np.random.random() * fits[-1]
            index = fits.index(next(i for i in fits if random_number <= i))
            selected_players.append(players[index])
        return selected_players
    
    def stochastic_universal_sampling(self, players, k):
        """
        Gets a list of players and returns the top k players.
        """
        selected_players = []
        fits = list(np.cumsum(list(map(lambda i: i.fitness, players))))
        length = fits[-1] / k
        random_number = np.random.random() * length
        for i in range(k) :
            index = fits.index(next(j for j in fits if (random_number + (i * length)) <= j))
            selected_players.append(players[index])
        return selected_players
    
    def q_tournament_selection(self, players, k, q=3):
        """
        Gets a list of players and returns the top k players.
        """
        selected_players = []
        for _ in range(k) :
            random_number = round(np.random.random() * (len(players)-1))
            max = players[random_number]
            for _ in range(q - 1) :
                random_number = round(np.random.random() * (len(players)-1))
                temp = players[random_number]
                if temp.fitness > max.fitness :
                    max = temp
            selected_players.append(max)
        return selected_players
    
    def learning_curve(self, players, k):
        """
        Gets a list of players and returns the top k players.
        """
        pass
    
    def crossover(self, parent1, parent2):
        child1 = self.clone_player(parent1)
        child2 = self.clone_player(parent2)
        
        nn_layers_number = len(parent1.nn.weights)
        nn_biases_number = len(parent1.nn.biases)
        
        for i in range(nn_layers_number):
            layer1 = parent1.nn.weights[i]
            layer2 = parent2.nn.weights[i]
            length = len(layer1) * len(layer1[0])
            index = round(np.random.random() * length)
            layer3 = np.array(list(layer1.reshape(length)[:index]) + list(layer2.reshape(length)[index:])).reshape([len(layer1), len(layer1[0])])
            layer4 = np.array(list(layer2.reshape(length)[:index]) + list(layer1.reshape(length)[index:])).reshape([len(layer1), len(layer1[0])])
            child1.nn.weights[i] = layer3
            child2.nn.weights[i] = layer4
        
        for j in range(nn_biases_number):
            layer1 = parent1.nn.biases[i]
            layer2 = parent2.nn.biases[i]
            length = len(layer1) * len(layer1[0])
            index = round(np.random.random() * length)
            layer3 = np.array(list(layer1.reshape(length)[:index]) + list(layer2.reshape(length)[index:])).reshape([len(layer1), len(layer1[0])])
            layer4 = np.array(list(layer2.reshape(length)[:index]) + list(layer1.reshape(length)[index:])).reshape([len(layer1), len(layer1[0])])
            child1.nn.biases[i] = layer3
            child2.nn.biases[i] = layer4
        
        return child1, child2
    
    def mutate(self, player):
        for layer in player.nn.weights:
            chance = np.random.random()
            if chance < self.mutation_rate :
                length = len(layer) * len(layer[0])
                index = round(np.random.random() * (length-1))
                new_weight = np.random.normal(0, 1)
                layer.reshape(length)[index] = new_weight
                
        for layer in player.nn.biases:
            chance = np.random.random()
            if chance < self.mutation_rate :
                length = len(layer) * len(layer[0])
                index = round(np.random.random() * (length-1))
                new_weight = np.random.normal(0, 1)
                layer.reshape(length)[index] = new_weight
    
    def create_children(self, parent1, parent2):
        child1, child2 = self.crossover(parent1, parent2)
        self.mutate(child1)
        self.mutate(child2)
        return child1, child2
