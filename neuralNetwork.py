import numpy as np
from utilities import sigmoid

class NeuralNetwork:
    def __init__(self):
        self.inputs = 10
        self.outputs = 5
        self.weights = []
        self.weights.append(2 * np.random.rand(self.inputs, 10) - 1)
        # self.weights.append(2 * np.random.rand(20, 9) - 1)
        self.weights.append(2 * np.random.rand(11, self.outputs) - 1)
        # self.weights.append(np.array(
        #     [[-0.13802866,  0.29494864, -0.57660932],
        #     [ 0.83919849,  0.13856122, -0.17898541],
        #     [-0.65025118, -0.79253393, -0.03775067],
        #     [ 0.97959768,  0.06206309,  0.18365476],
        #     [-0.92211425,  0.36653791, -0.86666298],
        #     [-0.15311869,  0.82270675,  0.74922051],
        #     [ 0.8111869 , -0.89516266, -0.3322859 ],
        #     [-0.01646472, -0.38128739, -0.2055601 ],
        #     [-0.18364351,  0.65999863, -0.08159478],
        #     [-0.84041543, -0.37056008,  0.1217021 ]]
        # ))
        # self.weights.append(np.array(
        #     [[ 0.19205304, -0.06181302,  0.01584856,  0.22501027, -0.37980217],
        #     [-0.73684511,  0.84697391, -0.5532616 , -0.27973699,  0.66414628],
        #     [-0.53436446, -0.55817449,  0.92557067,  0.44454477,  0.53866142],
        #     [-0.37249095, -0.80751129,  0.58759138,  0.33357395, -0.77225907]]
        # ))


    def forwardPropagate(self, X):
        X = np.array(X)
        a = np.reshape(X, (1, X.size)) 
        for theta in self.weights:
            a0 = np.array([[1]])
            a = np.hstack([a0, a])
            z = np.matmul(a, theta)
            a = sigmoid(z)
        return a[0]