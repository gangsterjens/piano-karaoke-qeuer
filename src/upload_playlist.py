import requests
from supabase import create_client, Client

class SBClient():
  def __init__(self, api_key, api_url):
    self.api_key = api_key
    self.api_url = api_url
    self.supabase = create_client(api_url, api_key)

  def get_users(self):
    users = self.supabase.table("admin_users").select("owner_name").execute()
    users = users.data
    names_list = []
    for name in users:
      names_list.append(name['owner_name'])
    return names_list
    
  def get_current_owner(self):
    current_owner = self.supabase.table("admin_users").select("owner_name").eq("current_owner", True).execute()
    if len(current_owner.data) > 0:
      current_owner = current_owner.data[0]['owner_name']
    else:
      current_owner = 'Ingen'
    return current_owner

  def set_new_owner(self, new_owner):
    former_owner = self.get_current_owner()
    new_owner_true = self.supabase.table("admin_users").update({'current_owner': True}).eq('owner_name', new_owner).execute()
    if len(new_owner_true.data) > 0 and former_owner != 'Ingen' and new_owner_true.data[0]['owner_name'] != former_owner:
      old_owner_false = self.supabase.table("admin_users").update({'current_owner': False}).eq('owner_name', former_owner).execute()


  def add_playlist_to_db(self, songs, owner):
    song_current_json = {'owner': owner, 'is_current': True}
    try:      
      update_current = self.supabase.table("song_list_current").update({'is_current': False}).eq('owner', owner).execute()
    except Exception as e:
      print(e)
    
    if len(update_current.data) > 0: # check if there was any data returned
      try:
        song_current = self.supabase.table("song_list_current").insert(song_current_json).execute()
      except Exception as e:
        print(e)
    
    if len(song_current.data) > 0:
      print(f"Successfully added {len(song_current.data)} songs to the database.")
      current_id = song_current.data[0]['id']
    else:
      print(song_current)
    if len(songs) > 0 and len(song_current.data) > 0:
      for el in songs:
        el['owner'] = owner
        el['song_list_current_id'] = current_id
      try:
        song_list = self.supabase.table("song_list").insert(songs).execute()
      except Exception as e:
        print(e)
      if len(song_list.data) > 0:
        print(f"Successfully added {len(song_list.data)} songs to the database.")
      else:
        print(song_list)

        
        
class CreatePlaylist(SBClient):
  def __init__(self, api_key, api_url, spotify_client_id, spotify_client_secret):
    super().__init__(api_key, api_url)
          # Initialize additional attributes for the CreatePlaylist class
    self.token_url = "https://accounts.spotify.com/api/token"
    self.spotify_client_id = spotify_client_id
    self.spotify_client_secret = spotify_client_secret

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": self.spotify_client_id,
        "client_secret": self.spotify_client_secret
    }

    # Make the POST request
    response = requests.post(self.token_url, headers=headers, data=data)

    # Check the response
    if response.status_code == 200:
        token_info = response.json()
        self.token = token_info['access_token']
    else:
        print(f"Error: {response.status_code}, {response.text}")


  def get_playlist_songs(self, playlist_id):
    # Define the API URL and the authorization token
    token = self.token
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }

  # Make the GET request
    response = requests.get(url, headers=headers)

  # Print the response (or handle it as needed)
    if response.status_code == 200:
        data = response.json()

    songs = []
    for track in data['tracks']['items']:
        # Skip if no track object (Spotify marks removed/unavailable tracks this way)
        if not track.get('track'):
            continue
    
        tmp_song_dict = {}
        song = track['track']['name'].replace('ae', 'æ')
        artist = track['track']['artists'][0]['name'].replace('ae', 'æ')
        song_id = track['track']['id']
    
        tmp_song_dict['artist'] = artist
        tmp_song_dict['song'] = song
        tmp_song_dict['spotify_id'] = song_id
        # tmp_song_dict['owner'] = owner
    
        songs.append(tmp_song_dict)
    
    return songs
