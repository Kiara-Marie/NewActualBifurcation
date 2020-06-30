import numpy as np


def load_from_binary(filename):
    f_id = open(filename, "rb")
    dims = np.fromfile(f_id, dtype=int, count=2)
    mat = np.array([0])
    mat = np.append(mat, np.fromfile(f_id, offset=8))
    mat = np.reshape(mat, (dims[0], dims[1]))
    f_id.close()
    return mat
