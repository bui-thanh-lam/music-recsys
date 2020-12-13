import db.ConnectDatabase as DB
import numpy as np
import apis.process as Process


#Query user
def login(username, password):
    connection = DB.getConnection()
    sql = "SELECT * FROM user WHERE user_name = %s AND pass_word = %s"
    try:
        cursor = connection.cursor()
        cursor.execute(sql, (username,password))
        user = cursor.fetchone()
        return user
    finally:
        connection.close()

#Query history
def getHistory(userId):
    connection = DB.getConnection()
    historySql = "SELECT echonest_track_id, play_count FROM history WHERE user_id = %s"
    try:
        history = []
        historyCursor = connection.cursor()
        historyCursor.execute(historySql, (userId))
        for rowHistory in historyCursor:
            echonestTrackId = rowHistory['echonest_track_id']
            trackSql = "SELECT * FROM track WHERE echonest_track_id = %s"
            trackCursor = connection.cursor()
            trackCursor.execute(trackSql,(echonestTrackId))
            track = trackCursor.fetchone()
            addDateTime = track['add_date']
            track['add_date'] = addDateTime.strftime('%m/%d/%Y')
            artists = []
            if(track['spotify_track_id'] != None):
                trackArtistSql = "SELECT * FROM track_artist WHERE echonest_track_id = %s"
                trackArtistCursor = connection.cursor()
                trackArtistCursor.execute(trackArtistSql,(echonestTrackId))
                for rowTrackArtist in trackArtistCursor:
                    artistId = rowTrackArtist['artist_id']
                    artistSql = "SELECT * FROM artist WHERE artist_id = %s"
                    artistCursor = connection.cursor()
                    artistCursor.execute(artistSql, (artistId))
                    artist = artistCursor.fetchone()

                    genres = []
                    artistGenresSql = "SELECT * FROM artist_genre WHERE artist_id = %s"
                    artistGenreCursor = connection.cursor()
                    artistGenreCursor.execute(artistGenresSql, (artistId))
                    for rowGenre in artistGenreCursor:
                        genre = rowGenre['genre']
                        genres.append(genre)
                    artist['genres'] = genres
                    artists.append(artist)
            else:
                artists = None

            track['artists'] = artists
            track['play_count'] = rowHistory['play_count']
            history.append(track)
        return history
    finally:
        connection.close()

def increaseView(userId, echonestTrackId):
    connection = DB.getConnection()
    try:
        historySql = "SELECT * FROM history WHERE user_id = %s AND echonest_track_id = %s"
        historyCursor = connection.cursor()
        historyCursor.execute(historySql, (userId, echonestTrackId))
        history = historyCursor.fetchone()
        playCount = history['play_count']
        playCount += 1

        trackSql = "SELECT * FROM track WHERE echonest_track_id = %s"
        trackCursor = connection.cursor()
        trackCursor.execute(trackSql, (echonestTrackId))
        track = trackCursor.fetchone()
        view = track['view']
        view += 1

        updateHistorySql = "UPDATE history SET play_count = %s WHERE user_id = %s AND echonest_track_id = %s"
        updateHistoryCursor = connection.cursor()
        updateHistoryCursor.execute(updateHistorySql, (playCount, userId, echonestTrackId))
        updateTrackSql = "UPDATE track SET view = %s WHERE echonest_track_id = %s"
        updateTrackCursor = connection.cursor()
        updateTrackCursor.execute(updateTrackSql, (view, echonestTrackId))
        connection.commit()
    finally:
        connection.close()
    return None

def getGenres(artistId):
    genres = []
    connection = DB.getConnection()
    try:
        sql = "SELECT genre FROM artist_genre WHERE artist_id = %s"
        cursor = connection.cursor()
        cursor.execute(sql, (artistId))
        for row in cursor:
            genres.append(row)
    finally:
        connection.close()
    return genres

# Get mapping of users and their indexes. Return Dictionary of User
def get_dict_user():
    connection = DB.getConnection()
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
    finally:
        connection.close()

    return dict_user

# Get mapping of items and their indexes. Return Dictionary of Items
def get_dict_item():
    connection = DB.getConnection()
    sql = "SELECT echonest_track_id FROM history GROUP BY echonest_track_id"
    try:
        dict_item = {}
        id = 0
        items = connection.cursor()
        items.execute(sql)
        for item in items:
            dict_item[id] = item['echonest_track_id']
            dict_item[item['echonest_track_id']] = id
            id += 1
    finally:
        connection.close()

    return dict_item

# Get R_real matrix. Save R in Data file
def get_R_real(dict_user, dict_item):
    connection = DB.getConnection()
    sql = "SELECT * FROM history"
    try:
        n_users = int(len(dict_user) / 2)
        n_items = int(len(dict_item) / 2)
        R = np.zeros((n_users, n_items), dtype=float)
        history = connection.cursor()
        history.execute(sql)
        for row_history in history:
            R[dict_user[row_history['user_id']], dict_item[row_history['echonest_track_id']]] = row_history['play_count']
    finally:
        connection.close()

    np.savetxt('../data/R_real.txt', R, delimiter=' ', fmt='%d')

# Get playlist recommended for user_id. If it is new user, return []
def get_playlist_1(user_id, n_songs):
    connection = DB.getConnection()
    user_sql = "SELECT echonest_track_id FROM history WHERE user_id = %s"
    user_cursor = connection.cursor()
    user_cursor.execute(user_sql, (user_id))
    if not user_cursor:  # user was not in history
        return []

    list = Process.get_list_rec(user_id, 10)  # list of echonest_track_id recommended for user_id
    try:
        play_list1 = []
        for song in list:
            trackSql = "SELECT spotify_track_id, track_name FROM track WHERE echonest_track_id = %s"
            trackCursor = connection.cursor()
            trackCursor.execute(trackSql, (song))
            track = trackCursor.fetchone()
            artists = []
            if track['spotify_track_id'] != None:
                trackArtistSql = "SELECT * FROM track_artist WHERE echonest_track_id = %s"
                trackArtistCursor = connection.cursor()
                trackArtistCursor.execute(trackArtistSql, (song))
                for rowTrackArtist in trackArtistCursor:
                    artistId = rowTrackArtist['artist_id']
                    artistSql = "SELECT artist_name FROM artist WHERE artist_id = %s"
                    artistCursor = connection.cursor()
                    artistCursor.execute(artistSql, (artistId))
                    artist = artistCursor.fetchone()
                    artists.append(artist)
            else:
                artists = None

            track['artists'] = artists
            play_list1.append(track)
        return play_list1
    finally:
        connection.close()



