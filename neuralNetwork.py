class NeuralNetwork:
    def __init__(self):
        theta1 = np.array([[0.1, 0.3, 0.5], [0.2, 0.4, 0.6]])
        theta2 = np.array([[0.7, 1.1, 1.5], [.8, 1.2, 1.6], [.9, 1.3, 1.7], [1, 1.4, 1.8]])

    def forwardPropagate(self, X):
        X0 = np.array([[1]])
        X = np.hstack([X0, X])
        a1 = X
        z2 = np.matmul(theta1, a1.T)
        a2 = sigmoid(z2)
        a20 = np.array([[1]])
        a2 = np.vstack([a20, a2])
        z3 = np.matmul(theta2, a2)
        a3 = sigmoid(z3)
        return a3