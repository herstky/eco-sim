import numpy as np
from tools.utilities import sigmoid

class NeuralNetwork:
    def __init__(self):
        self.inputs = 9
        self.outputs = 5
        self.weights = []
        
        hiddenLayers = [50]
        layers = hiddenLayers
        layers.insert(0, self.inputs)
        layers.append(self.outputs)
        # self.weights.append(2 * np.random.rand(self.inputs + 1, hiddenLayers[0]) - 1)
        # self.weights.append(2 * np.random.rand(hiddenLayers[0] + 1, self.outputs) - 1)

        # if not len(hiddenLayers):
        #     self.weights.append(2 * np.random.rand(self.inputs, hiddenLayers[0]) - 1)
        #     self.weights.append(2 * np.random.rand(self.inputs, hiddenLayers[0]) - 1)


        for i in range(len(layers) - 1):
            self.weights.append(2 * np.random.rand(layers[i] + 1, layers[i + 1]) - 1)



    def forwardPropagate(self, X):
        X = np.array(X)
        a = np.reshape(X, (1, X.size)) 
        for theta in self.weights:
            a0 = np.array([[1]])
            a = np.hstack([a0, a])
            z = np.matmul(a, theta)
            a = sigmoid(z)
        return a[0]