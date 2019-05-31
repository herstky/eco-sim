from functools import wraps
import numpy as np

def functionTimer(func):
    import time
    @wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        t1 = time.time()
        print("{} ran in {} seconds".format(func.__name__, t1 - t0))
        return result
    return wrapper

def sigmoid(z):
    '''
    Applies sigmoid function to input matrix elementwise.
    '''
    for row in range(len(z)):
        for col in range(len(z[0])):
            z[row][col] = np.clip(z[row][col], -500, 500) # prevents precision overflow
            z[row][col] =  1 / (1 + np.exp(-z[row][col]))
    return z
