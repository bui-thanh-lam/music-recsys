from pprint import pprint
from db import repository as db

def get_recommendations_by_artists(artists):
    '''
    Recommend new list of artists by list of at least 3 artists
    artists format :
        [{'artist_id': '0nmQIMXWTXfhgOBdNzhGOs',
        'artist_name': 'Avenged Sevenfold',
        'artist_popularity': 76,
        'genres': ['metal']},
        {'artist_id': '4exLIFE8sISLr28sqG1qNX',
        'artist_name': 'Travis Barker',
        'artist_popularity': 76,
        'genres': ['hip-hop']},]
    '''
    genres = []
    for artist in artists:
        temp_genres = artist['genres']
    return None
