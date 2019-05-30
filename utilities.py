from functools import wraps
import math

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

def sigmoid(x):
    '''
    Applies sigmoid function to input matrix elementwise.
    '''
    z = x
    for row in range(len(z)):
        for col in range(len(z[0])):
            z[row][col] =  1 / (1 + math.exp(-z[row][col]))
    return z
