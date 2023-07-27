from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID=""
CLIENT_SECRET=""
REDIRECT_URI="http://localhost:8888/callback"

def top_songs(date):
    response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
    web_page = response.text
    soup = BeautifulSoup(web_page, "html.parser")
    song_names_spans=soup.select("li ul li h3")
    song_names=[song.get_text().strip() for song in song_names_spans]

    #--------Spotipy----------------------------

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                   client_secret=CLIENT_SECRET,
                                                   redirect_uri=REDIRECT_URI,
                                                   scope="playlist-modify-private"))
    USER_ID = sp.current_user()['id']
    song_URLs=[]
    year = date[:4]
    #Creating Song Uri of Spotify
    for song_name in song_names:
        q=f"track: {song_name} year: {year} "
        result=sp.search(q=song_name, type="track")
        if result["tracks"]["items"]:
            song_uri = result["tracks"]["items"][0]["uri"]
            song_URLs.append(song_uri)
        else:
            print(f"Song {song_name} not found on Spotify")


    # Creating a new playlist on Spotify
    playlist_name = f"Billboard Hot 100 - {year}"
    description = "Top 100 songs on Billboard charts for the specified year."

    playlist = sp.user_playlist_create(user=USER_ID,
                                       name=playlist_name,
                                       description=description,
                                       public=False)
    # Adding songs to playlist
    sp.playlist_add_items(playlist_id=playlist["id"], items=song_URLs)


#https://open.spotify.com/track/3k79jB4aGmMDUQzEwa46Rz
if __name__ == '__main__':
    date=input("Which year do you want to travel to ? Type the date in this format YYYY-MM-DD : ")
    top_songs(date)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
