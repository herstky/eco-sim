import numpy as np
from utilities import sigmoid

class NeuralNetwork:
    def __init__(self):
        self.theta1 = 2 * np.random.rand(10, 20) - 1
        self.theta2 = 2 * np.random.rand(21, 8) - 1

    def forwardPropagate(self, X):
        print(X)
        X = np.array(X)
        X = np.reshape(X, (1, X.size))
        X0 = np.array([[1]])
        X = np.hstack([X0, X])
        a1 = X
        z2 = np.matmul(a1, self.theta1)
        a2 = sigmoid(z2)
        a20 = np.array([[1]])
        a2 = np.hstack([a20, a2])
        z3 = np.matmul(a2, self.theta2)
        a3 = sigmoid(z3)
        print(a3)
        return a3