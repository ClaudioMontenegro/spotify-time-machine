import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

os.environ["SPOTIPY_CLIENT_ID"] = "your-SPOTIPY_CLIENT_ID"
os.environ["SPOTIPY_CLIENT_SECRET"] = "your-SPOTIPY_CLIENT_SECRET"
os.environ["SPOTIPY_REDIRECT_URI"] = "http://example.com"


class SpotifyPlaylist:
    def __init__(self):
        self.scope = 'user-library-read'
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=self.scope))
        self.user_id = self.sp.me()['id']

    def get_artist_uri(self, artist_name):
        results = self.sp.search(q=artist_name, type='artist', limit=1)
        if results['artists']['items']:
            return results['artists']['items'][0]['uri']
        else:
            print(f"Artist '{artist_name}' not found on Spotify.")
            return None

    def search_songs(self, song_name, artist_name):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope='user-library-read'))
        results = self.sp.search(q=f'track:{song_name} artist:{artist_name}', type='track', limit=1)
        if results['tracks']['items']:
            return results['tracks']['items'][0]['uri']
        else:
            print(f"No results for track:{song_name} artist:{artist_name}")

    def create_playlist(self, name_playlist):
        scope = 'playlist-modify-public playlist-modify-private'
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
        playlist = self.sp.user_playlist_create(user=self.user_id, name=f"{name_playlist}", public=False, description='')
        playlist_id = playlist['id']
        return playlist_id
