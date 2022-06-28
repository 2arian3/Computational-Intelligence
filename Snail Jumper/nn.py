import numpy as np


class NeuralNetwork:
    
    ACTIVATION_FUNCTIONS = {
        'sigmoid': lambda x: 1 / (1 + np.exp(-x)),
        'relu': lambda x: np.maximum(0, x),
        'softmax': lambda x: np.exp(x) / np.sum(np.exp(x))
    }

    def __init__(self, layer_sizes):
        """
        Neural Network initialization.
        Given layer_sizes as an input, you have to design a Fully Connected Neural Network architecture here.
        :param layer_sizes: A list containing neuron numbers in each layers. For example [3, 10, 2] means that there are
        3 neurons in the input layer, 10 neurons in the hidden layer, and 2 neurons in the output layer.
        """
        self.number_of_layers = len(layer_sizes)
        self.biases = [
            np.zeros([layer_sizes[i + 1]]) for i in range(len(layer_sizes) - 1)
        ]
        self.weights = [
            np.random.normal(0, 1, [layer_sizes[i + 1], layer_sizes[i]]) for i in range(len(layer_sizes) - 1)
        ]

    def activation(self, x, function_type='sigmoid'):
        """
        The activation function of our neural network, e.g., Sigmoid, ReLU.
        :param x: Vector of a layer in our network.
        :return: Vector after applying activation function.
        """
        return NeuralNetwork.ACTIVATION_FUNCTIONS[function_type.lower()](x)

    def forward(self, x, activation_function_type='sigmoid'):
        """
        Receives input vector as a parameter and calculates the output vector based on weights and biases.
        :param x: Input vector which is a numpy array.
        :return: Output vector
        """
        result = x
        for i in range(self.number_of_layers-1):
            result = self.activation(self.weights[i] @ result + self.biases[i][0], activation_function_type)
        return result