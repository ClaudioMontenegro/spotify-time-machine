from bs4 import BeautifulSoup
import requests
import re
from spotify_list import SpotifyPlaylist
from tkinter import messagebox


class_song = "c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only"
class_name = "c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only"
BILLBOARD = "https://www.billboard.com/charts/hot-100/"


class SongsCollect:
    def __init__(self):
        self.soup = BeautifulSoup()
        self.cleaned_song_list = []
        self.cleaned_artists_list = []
        self.track_uri = []
        self.spt = SpotifyPlaylist()

    def list_of_songs(self, ent_inp):
        self.soup = ent_inp
        songs = self.soup.find_all(name="h3", class_=class_song)
        artists = self.soup.find_all(name="span", class_=class_name)
        titles = [song.text for song in songs]
        names = [name.text for name in artists]

        self.cleaned_song_list = [re.sub(r'[\n\t]', '', s) for s in titles]
        cleaned_artists_list = [re.sub(r'[\n\t]', '', s) for s in names]
        mid_list = []
        for text in cleaned_artists_list:
            split_text = text.split('Featuring', 1)
            mid_list.append(split_text[0].strip())
        self.cleaned_artists_list = mid_list
        track_mid_list = []
        for song, artist in zip(self.cleaned_song_list, self.cleaned_artists_list):
            track_mid_list.append(self.spt.search_songs(song, artist))
        self.track_uri = [uri for uri in track_mid_list if uri is not None]

    def add_songs(self, name_playlist):
        play_id = self.spt.create_playlist(name_playlist)
        valid_track_uris = [uri for uri in self.track_uri if uri is not None]
        try:
            self.spt.sp.user_playlist_add_tracks(user=self.spt.user_id, playlist_id=play_id, tracks=valid_track_uris)
        except TypeError:
            messagebox.showinfo(title='Error', message="Try again with a new date and valid track's name")
        else:
            messagebox.showinfo(title="Done!", message="Your playlist was made. Have fun and relive your memories")


class DataCollect:
    def __init__(self, year_ent, name_plt):
        self.soup = BeautifulSoup()
        self.year_ent = year_ent
        self.name_plt = name_plt
        self.songs = SongsCollect()

    def collect_data(self):
        link = f"{BILLBOARD}{self.year_ent.get()}"
        name_of_playlist = self.name_plt.get()
        response = requests.get(link)
        web = response.text
        self.soup = BeautifulSoup(web, "html.parser")
        self.songs.list_of_songs(self.soup)
        self.songs.add_songs(name_of_playlist)
