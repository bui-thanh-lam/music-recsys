from db import repository as repo


def artist_similarity(a1_id, a2_id):
    """Return similarity score of two artists given their ids"""
    if a1_id == a2_id:
        return 1
    else:
        penalty = 0.8
        a1_genres = repo.get_genres(a1_id)
        a2_genres = repo.get_genres(a2_id)
        numerator = 0
        dominator = 0.5 * (len(a1_genres) + len(a2_genres))
        for genre in a1_genres:
            if genre in a2_genres:
                numerator += 1
        return penalty*numerator/dominator


def track_similarity(t1_id, t2_id):
    if t1_id == t2_id:
        return 1.0
    else:
        penalty = 0.9
        t1_artists = repo.get_track_by_id(t1_id)['artists']
        t2_artists = repo.get_track_by_id(t2_id)['artists']
        scores = []
        if len(t1_artists) == 0 or len(t2_artists) == 0:
            return 0
        for t1_a in t1_artists:
            for t2_a in t2_artists:
                scores.append(artist_similarity(t1_a['artist_id'], t2_a['artist_id']))
        return penalty * sum(scores) / len(scores)
