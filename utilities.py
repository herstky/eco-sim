from functools import wraps

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