import os
import logging
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set up logging
logging.basicConfig(level=logging.INFO)

def get_billboard_top_100(date):
    try:
        response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch Billboard data: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    song_names_spans = soup.select("li ul li h3")
    song_names = [song.getText().strip() for song in song_names_spans]
    return song_names

def authenticate_spotify():
    try:
        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                scope="playlist-modify-private",
                redirect_uri="http://example.com",
                client_id=os.getenv("SPOTIPY_CLIENT_ID"),
                client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
                show_dialog=True,
                cache_path="token.txt"
            )
        )
        return sp
    except Exception as e:
        logging.error(f"Spotify authentication failed: {e}")
        return None

def search_spotify_tracks(sp, song_names, year):
    song_uris = []
    for song in song_names:
        try:
            result = sp.search(q=f"track:{song} year:{year}", type="track")
            uri = result["tracks"]["items"][0]["uri"]
            song_uris.append(uri)
        except IndexError:
            logging.warning(f"{song} doesn't exist on Spotify. Skipped.")
        except Exception as e:
            logging.error(f"Error searching for {song} on Spotify: {e}")
    return song_uris

def create_spotify_playlist(sp, user_id, date, song_uris):
    try:
        playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
        sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
        logging.info(f"Playlist {date} Billboard 100 created successfully.")
    except Exception as e:
        logging.error(f"Failed to create playlist: {e}")

def main():
    date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

    # Validate date format
    try:
        year, month, day = map(int, date.split("-"))
    except ValueError:
        logging.error("Invalid date format. Please use YYYY-MM-DD.")
        return

    song_names = get_billboard_top_100(date)
    if not song_names:
        logging.error("No songs found for the given date.")
        return

    sp = authenticate_spotify()
    if not sp:
        return

    user_id = sp.current_user()["id"]
    year = date.split("-")[0]
    song_uris = search_spotify_tracks(sp, song_names, year)

    if song_uris:
        create_spotify_playlist(sp, user_id, date, song_uris)

if __name__ == "__main__":
    main()