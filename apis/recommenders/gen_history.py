import numpy as np
import random

def gen_R_train(path_to_R_full, gap_ratio=0.1):
    with open(path_to_R_full, 'r') as f:
        R = [[float(num) for num in line[:-1].split(' ')] for line in f]
        R = np.array(R)
        n_users = R.shape[0]
        n_items = R.shape[1]
        for i in range(n_users):
            for j in range(n_items):
                if R[i, j] > 0:
                    decision = random.random()
                    if decision < gap_ratio:
                        R[i, j] = 0
    np.savetxt('../data/R_train.txt', R, delimiter=' ', fmt='%d')
