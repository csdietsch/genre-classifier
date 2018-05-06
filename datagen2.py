# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 20:07:46 2018

@author: csdietsch
"""

import spotipy as spotipy
import spotipy.util as util
import sys
import csv
import pandas as pd

spotify = spotipy.Spotify()





#based off a spotify API application
#used for authenticating access to API
lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'
CLIENT_SECRET = '22c83157b7d849f1a668e70d293b10d5'
CLIENT_ID = '24070e2b0c0248cdbaa407672a018f83'
REDIRECT_URI = 'https://github.com/'
SCOPE = 'user-library-read'

#lists of artists of various genres 
rock = ['Led Zeppelin', 'Kings of Leon', 'The Rolling Stones', 'AC/DC', 'Guns N\' Roses', 'Aerosmith', 'Foo Fighters', 'Pearl Jam', 'Lynyd Skynyrd', 'Bon Jovi', 'Whitesnake', 'Linkin Park', 'Deep Purple', 'Foreigner', 'Journey', 'Metallica', 'Black Sabbath', 'Jimi Hendrix', 'The Doors']
alt = ['The Black Keys', 'Twenty One Pilots', 'Thirty Seconds to Mars', 'blink-182', 'Cage the Elephant', 'Portugal. The Man', 'Chvrches', 'Andrew McMahon', 'Arctic Monkeys', 'Capital Cities', 'Modest Mouse', 'Vampire Weekend', 'MGMT', 'Death Cab for Cutie', 'St. Vincent', 'Of Monsters and Men'] #R.E.M. contains invalid characters
hiphop = ['Jay-Z', 'Kayne West', 'Drake', 'Kendrick Lamar', 'Lil Wayne', 'Snoop Dogg', '50 Cent', 'J. Cole', 'Rick Ross', 'Nicki Minaj', 'Dr. Dre', 'N.W.A.', 'Cardi B', 'Kid Ink', 'Post Malone', 'Ace Hood'] #eminem: invalid characters
pop = ['Katy Perry', 'Ariana Grande', 'Britney Spears', 'Beyonce', 'Madonna', 'Lady Gaga', 'Bruno Mars', 'Mariah Carey', 'Justin Bieber', 'Sean Mendes', 'Christina Aguilera', 'Maroon 5', 'Ed Sheeran', 'Demi Lovati']
edm = ['Skrillex', 'deadmau5', 'Avicii', 'David Guetta', 'Martin Garrix', 'Steve Aoki', 'Daft Punk', 'Armin van Buuren', 'Diplo', 'Zedd', 'Marshmello', 'Calvin Harris', 'Kygo', 'DJ Snake', 'Kaskade', 'Steve Aoki', 'Hardwell', 'Swedish House Mafia', 'Afrojack', 'Bassnectar']

#a list of genre lists
genres = [rock, alt, hiphop, pop, edm]
#rock = 0, alt = 1, hiphop = 2, pop = 3, edm = 4
genre_num = 0

#authenticate
token = util.oauth2.SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
cache_token = token.get_access_token()
spotify = spotipy.Spotify(cache_token)

#open a csv
with open('audio_features_v3_3 .csv', 'w') as csvfile:
    fieldnames = ['artist', 'song', 'acousticness', 'danceability', 'duration_ms', 'energy', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence', 'genre_class']
   # fieldnames = ['acousticness', 'danceability', 'duration_ms', 'energy', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence', 'genre_class']
 
    #fieldnames = ['artist', 'song']
    writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n', fieldnames=fieldnames)
    writer.writeheader()
   

#iterate over every artist in each genre list...
    for genre in genres: 
        for artist in genre:
        #get the uri for that artist...
            results = spotify.search(q='artist:' + artist, type='artist')
            items = results['artists']['items']
            for item in items:
                uri = item['uri']
                album_results = spotify.artist_albums(uri, album_type='album', country='US', limit=5, offset=0)
                albums = album_results['items']
                for album in albums:
                    album_uri = album['uri']
           
                    track_results = spotify.album_tracks(album_uri, limit=50, offset = 0)
                    tracks = track_results['items']
              #  features = spotify.audio_features(tracks['tracks'][:25])
                    for track in tracks:
                            print('track : ' + track['name'] + " artist : " + artist)
                            features = spotify.audio_features(track['id'])
                    #df = pd.DataFrame(features)
                    #print(df)
                            for feature in features:
                       #print(feature['tempo'])
                                writer.writerow({'artist' : artist, 'song' : track['name'], 'acousticness': feature['acousticness'], 'danceability': feature['danceability'], 'duration_ms': feature['duration_ms'], 'energy': feature['energy'], 'instrumentalness': feature['instrumentalness'], 'key': feature['key'], 'liveness': feature['liveness'], 'loudness': feature['loudness'], 'mode': feature['mode'], 'speechiness': feature['speechiness'], 'tempo': feature['tempo'], 'time_signature': feature['time_signature'], 'valence': feature['valence'], 'genre_class': genre_num})
 #                      writer.writerow({'artist': artist, 'song': track['name'], 'genre_class': genre_num, 'acousticness': feature['acousticness'], 'danceability': feature['danceability'], 'duration_ms': feature['duration_ms'], 'energy': feature['energy'], 'instrumentalness': feature['instrumentalness'], 'key': feature['key'], 'liveness': feature['liveness'], 'loudness': feature['loudness'], 'mode': feature['mode'], 'speechiness': feature['speechiness'], 'tempo': feature['tempo'], 'time_signature': feature['time_signature'], 'valence': feature['valence']})
   
                    #print('features : ' + features['tempo'])
        genre_num += 1
#lz = spotify.artist_top_tracks(lz_uri)







