from pprint import pprint
from db import repository as db
import random
import array as arr

def get_recommendations(artists, genres):
    '''
    Recommend new list of artists by list of at least 3 artists and list of at least 1 genre
    artists:
        [{'artist_id': '0nmQIMXWTXfhgOBdNzhGOs',
        'artist_name': 'Avenged Sevenfold',
        'artist_popularity': 76,
        'genres': ['metal']},
        {'artist_id': '4exLIFE8sISLr28sqG1qNX',
        'artist_name': 'Travis Barker',
        'artist_popularity': 76,
        'genres': ['hip-hop']},]

    genres: ['hip-hop', 'pop']

    '''
    count_genre_of_artists = 0
    for artist in artists:
        temp_genres = artist['genres']
        for genre in temp_genres:
            genres.append(genre)
            count_genre_of_artists += 1
    recommend_artists = []
    if(count_genre_of_artists > 0):
        number = 3
    else:
        number = 5

    for genre in genres:
        temp_artists = db.get_popular_artists_by_genre(genre,number)
        for artist in temp_artists:
            if(not check_exist_artist(recommend_artists, artist)):
                recommend_artists.append(artist)


    total = len(recommend_artists)
    if(total <= 5):
        return recommend_artists
    else:
        final_recommend_artists = []
        count = 0
        choose_array = []
        while(count < 5):

            order = random.randrange(total)
            exist = False
            for i in range(0,count):
                if (order == choose_array[i]):
                    exist = True
                    break
            if(not exist):
                choose_array.append(order)
                count += 1

        for i in range(0, count):
            final_recommend_artists.append(recommend_artists[choose_array[i]])

        return final_recommend_artists



def check_exist_artist(artists, artist):
    for i in artists:
        if(i['artist_id'] == artist['artist_id']):
            return True
    return False