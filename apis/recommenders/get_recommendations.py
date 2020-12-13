from db import repository as repo
from apis.recommenders.WMF import WeightedMF
from apis.recommenders import utils

dict_user = repo.get_dict_user()
dict_item = repo.get_dict_item()
repo.get_R(dict_user, dict_item)

R = utils.load_R('../data/R.txt')
P, C = utils.convert(R)

wmf = WeightedMF(P, C)
wmf.fit()
wmf.save()


def get_list_rec(user_id, n_rec_items):
    user_index = dict_user[user_id]
    recommendations = wmf.get_recommendations(user_index, n_rec_items)
    trackId_rec = utils.get_trackId_recommendation(dict_item, recommendations)
    return trackId_rec


def get_CF_playlist(user_id, n_tracks):
    """Return a collaborative filtering based recommended playlist given a user_id. Return None if the user is new"""
    if repo.is_new_user(user_id):
        return None
    track_ids = get_list_rec(user_id, n_tracks)  # list of recommended echonest_track_id for user_id
    playlist = []
    for track_id in track_ids:
        track = repo.get_track_by_id(track_id)
        playlist.append(track)
    return playlist

