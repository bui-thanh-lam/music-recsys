import numpy as np
from db import repository as repo
from apis.recommendations.WMF import WeightedMF
from apis.recommendations import utils, similarity
from pprint import pprint

dict_user = repo.get_dict_user()
dict_item = repo.get_dict_item()
wmf = WeightedMF()
wmf.load()


def get_list_rec(user_id, dict_user, dict_item, wmf):
    user_index = dict_user[user_id]
    recommendations = wmf.get_recommendations(user_index)
    track_id_rec = utils.get_trackId_recommendation(dict_item, recommendations)
    return track_id_rec


def get_CF_playlist(user_id, n_tracks):
    """Return a collaborative filtering based recommended playlist given a user_id. Return None if the user is new"""
    if repo.is_new_user(user_id):
        return None
    track_ids = get_list_rec(user_id, dict_user, dict_item, wmf)  # list of recommended echonest_track_id for user_id
    playlist = []
    for track_id in track_ids:
        track = repo.get_track_by_id(track_id)
        if track['spotify_track_id']:
            playlist.append(track)
        if len(playlist) > n_tracks:
            return playlist


def get_nextup_tracks(user_id, seed_track_id, n_tracks):
    """Return top n most similar tracks to a seed track given the user's id"""
    candidates = repo.get_history(user_id)
    scores = []
    for track in candidates:
        scores.append(similarity.track_similarity(seed_track_id, track['echonest_track_id']))
    scores = np.argsort(scores)
    next_up_tracks = []
    for i in range(n_tracks):
        next_up_tracks.append(candidates[scores[-(i+1)]])
    return next_up_tracks


# # Test
pprint(get_CF_playlist("45a768612381c7dd8d50484f45f5f1ca2ed5d021", 10))
# pprint(get_nextup_tracks("000ebc858861aca26bac9b49f650ed424cf882fc", "SONMINI12AB0180DCE", 5))
# pprint(repo.get_history("000ebc858861aca26bac9b49f650ed424cf882fc"))
