import numpy as np
import random


def load_R(path_to_R):
    """Load R from data file"""
    with open(path_to_R, 'r') as f:
        R = [[float(num) for num in line[:-1].split(' ')] for line in f]
        R = np.array(R)

    return R


def convert(R, alpha=40):
    """Convert R into P and C"""
    P = np.zeros_like(R)
    C = np.ones_like(R)
    n_users = R.shape[0]
    n_items = R.shape[1]
    for i in range(n_users):
        for j in range(n_items):
            if R[i, j] == 0:
                continue
            P[i, j] = 1
            C[i, j] = 1 + alpha * R[i, j]
    return P, C


def get_trackId_recommendation(dict_item, recommendations):
    trackId_rec = []
    for i in recommendations:
        trackId_rec.append(dict_item[i])
    return trackId_rec


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