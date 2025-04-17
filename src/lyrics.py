import lyricsgenius

def get_g_lyrics(song, artist=None):
  # Replace this with your actual token
  genius = lyricsgenius.Genius(access_token)

  # Search and print lyrics
  if artist is not None:
    song = genius.search_song(song, artist)
  else:
    song = genius.search_song(song)

  tekst = song.lyrics.split('Lyrics')[-1]
  return tekst
