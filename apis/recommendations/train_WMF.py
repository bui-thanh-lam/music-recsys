from apis.recommendations.WMF import WeightedMF
from apis.recommendations import utils

R = utils.load_R('../../data/R.txt')
P, C = utils.IFconvert(R)

wmf = WeightedMF(P, C)
wmf.fit()
wmf.save()
