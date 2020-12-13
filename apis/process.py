from db import repository as data_base
from apis.recommenders.WMF import WeightedMF
from apis.recommenders import gen_history as gen_test
from apis.recommenders import utils
from apis.recommenders import evaluate
import numpy as np

dict_user = data_base.get_dict_user()
dict_item = data_base.get_dict_item()
data_base.get_R_real(dict_user, dict_item)

#gen_test.gen_R_train('../data/R_real.txt')
R = utils.load_R('../data/R_train.txt')
P, C = utils.convert(R)

wmf = WeightedMF(P, C, depth=40, early_stopping=False)
clock = evaluate.Clock()
wmf.fit()
clock.stop()
#wmf.save()

# Evaluate MAR@k of first n users
k = 20
n_users = 100
predicts = [wmf.get_recommendations(user, k) for user in range(n_users)]
with open('../data/R_real.txt', 'r') as f:
    targets = [[float(num) for num in line[:-1].split(' ')] for line in f]
    targets = [np.argsort(targets[user])[-k:] for user in range(n_users)]
print(evaluate.mark(predicts, targets, k))

def get_list_rec(user_id, n_rec_items):
    user_index = dict_user[user_id]
    recommendations = wmf.get_recommendations(user_index, n_rec_items)
    trackId_rec = utils.get_trackId_recommendation(dict_item, recommendations)
    return trackId_rec


