import streamlit as st
import streamlit.components.v1 as components
from src.lyrics import get_g_lyrics


song = st.text_input('Skriv inn sang')

artist = st.text_input('Skriv inn artist')

if st.button('Find lyrics'):
# Streamlit app ti
  text = get_g_lyrics(song, artist)
  st.markdown(text)
