import numpy as np

def random_symmetric_matrix(n, minflow, maxflow):
    _R = np.random.uniform(minflow, maxflow, int(n*(n-1)/2))
    P = np.zeros((n,n))
    P[np.triu_indices(n, 1)] = _R
    P[np.tril_indices(n, -1)] = P.T[np.tril_indices(n, -1)]
    return P

def random_matrix(n, m, max):
    return np.random.rand(n, m) * max

def random_time_matrix(number, n, m, max):
    return np.random.rand(number, n, m) * max

