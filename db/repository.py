import db.ConnectDatabase as Connector
import numpy as np

connection = Connector.getConnection()
cursor = connection.cursor()


def login(username, password):
    """Return a user object if login successfully. Otherwise return None"""
    sql = "SELECT * FROM user WHERE user_name = %s AND pass_word = %s"
    try:
        cursor.execute(sql, (username, password))
        user = cursor.fetchone()
        return user
    except:
        print("Failed to login")
        return None


def get_history(userId):
    """Return user's history if they have listened to at least one song. Otherwise, return None"""
    if is_new_user(userId):
        return None
    sql = "SELECT echonest_track_id, play_count FROM history WHERE user_id = %s"
    try:
        history = []
        cursor.execute(sql, userId)
        histories = cursor.fetchall()
        for h in histories:
            echonestTrackId = histories['echonest_track_id']
            sql = "SELECT * FROM track WHERE echonest_track_id = %s"
            cursor.execute(sql, echonestTrackId)
            track = cursor.fetchone()
            add_date_time = track['add_date']
            track['add_date'] = add_date_time.strftime('%m/%d/%Y')
            artists = []
            if track['spotify_track_id']:
                sql = "SELECT * FROM track_artist WHERE echonest_track_id = %s"
                cursor.execute(sql, echonestTrackId)
                tracks_arists = cursor.fetchall()
                for tracks_arists in tracks_arists:
                    artistId = tracks_arists['artist_id']
                    artistSql = "SELECT * FROM artist WHERE artist_id = %s"
                    cursor.execute(artistSql, artistId)
                    artist = cursor.fetchone()
                    genres = []
                    sql = "SELECT * FROM artist_genre WHERE artist_id = %s"
                    cursor.execute(sql, artistId)
                    _genres = cursor.fetchall()
                    for genre in _genres:
                        genre = genre['genre']
                        genres.append(genre)
                    artist['genres'] = genres
                    artists.append(artist)
            else:
                artists = None

            track['artists'] = artists
            track['play_count'] = h['play_count']
            history.append(track)
        return history
    except:
        print("Failed to get user history")
        return None


def increase_view(userId, echonestTrackId):
    """Update view and users' history in database. Return None"""
    try:
        sql = "SELECT * FROM history WHERE user_id = %s AND echonest_track_id = %s"
        cursor.execute(sql, (userId, echonestTrackId))
        history = cursor.fetchone()
        playCount = history['play_count']
        playCount += 1

        sql = "SELECT * FROM track WHERE echonest_track_id = %s"
        cursor.execute(sql, echonestTrackId)
        track = cursor.fetchone()
        view = track['view']
        view += 1

        sql = "UPDATE history SET play_count = %s WHERE user_id = %s AND echonest_track_id = %s"
        cursor.execute(sql, (playCount, userId, echonestTrackId))
        sql = "UPDATE track SET view = %s WHERE echonest_track_id = %s"
        cursor.execute(sql, (view, echonestTrackId))
        connection.commit()
    except:
        print("Failed to update view and history")
    return None


def get_genres(artistId):
    """Return aritst's genres given their id. Return None if artist_id is invalid"""
    genres = []
    try:
        sql = "SELECT genre FROM artist_genre WHERE artist_id = %s"
        cursor.execute(sql, artistId)
        for row in cursor:
            genres.append(row)
        return genres
    except:
        print("Failed to get artist's genres")
        return None


def get_dict_user():
    """Get mapping of users and their indexes. Return a dictionary of User"""
    sql = "SELECT user_id FROM history GROUP BY user_id"
    try:
        dict_user = {}
        id = 0
        users = connection.cursor()
        users.execute(sql)
        for user in users:
            dict_user[id] = user['user_id']
            dict_user[user['user_id']] = id
            id += 1
        return dict_user
    except:
        print("Failed to create users dictionary")
        return None


def get_dict_item():
    """Get mapping of items and their indexes. Return a dictionary of Items"""
    sql = "SELECT echonest_track_id FROM history GROUP BY echonest_track_id"
    try:
        dict_item = {}
        id = 0
        cursor.execute(sql)
        items = cursor.fetchall()
        for item in items:
            dict_item[id] = item['echonest_track_id']
            dict_item[item['echonest_track_id']] = id
            id += 1
        return dict_item
    except:
        print("Failed to create items dictionary")
        return None


def get_R(dict_user, dict_item):
    """Get R_real matrix from users' history. Save R in Data file. Return None"""
    sql = "SELECT * FROM history"
    try:
        n_users = int(len(dict_user) / 2)
        n_items = int(len(dict_item) / 2)
        R = np.zeros((n_users, n_items), dtype=float)
        cursor.execute(sql)
        histories = cursor.fetchall()
        for history in histories:
            R[dict_user[history['user_id']], dict_item[history['echonest_track_id']]] = history[
                'play_count']
    except:
        print("Failed to get R")
    np.savetxt('../../data/R.txt', R, delimiter=' ', fmt='%d')
    return None


def is_new_user(user_id):
    """Check if an user is new or not given their id"""
    try:
        sql = "SELECT user_id FROM history WHERE user_id = %s"
        cursor.execute(sql, user_id)
        return False
    except:
        print("Failed to get user")
        return True


def get_track_by_id(echonest_track_id):
    """Get a track given its id. Return None if the id is invalid"""
    try:
        sql = "SELECT echonest_track_id, spotify_track_id, track_name FROM track WHERE echonest_track_id = %s"
        cursor.execute(sql, echonest_track_id)
        track = cursor.fetchone()
        artists = []
        if track['spotify_track_id']:
            sql = "SELECT artist_id FROM track_artist WHERE echonest_track_id = %s"
            cursor.execute(sql, echonest_track_id)
            artist_ids = cursor.fetchall()
            for artist_id in artist_ids:
                sql = "SELECT artist_name FROM artist WHERE artist_id = %s"
                cursor.execute(sql, artist_id['artist_id'])
                artist = cursor.fetchone()
                artists.append(artist)
        track['artists'] = artists
        return track
    except:
        print("Failed to get track")
        return None
