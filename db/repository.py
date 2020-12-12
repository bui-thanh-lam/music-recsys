import ConnectDatabase as DB


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
    historSql = "SELECT echonest_track_id, play_count FROM history WHERE user_id = %s"
    try:
        history = []
        historyCursor = connection.cursor()
        historyCursor.execute(historSql, (userId))
        for rowHistory in historyCursor:
            echonestTrackId = rowHistory['echonest_track_id']

            trackSql = "SELECT * FROM track WHERE echonest_track_id = %s"
            trackCursor = connection.cursor()
            trackCursor.execute(trackSql,(echonestTrackId))
            track = trackCursor.fetchone()
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
            track['play count'] = rowHistory['play_count']
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
