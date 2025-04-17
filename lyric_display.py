import streamlit as st
import streamlit.components.v1 as components


song = st.input('Skriv inn sang')

artist = st.input('Skriv inn artist')

if st.button('Find lyrics'):
# Streamlit app ti
  text = get_g_lyrics(song, artist)
  st.markdown(text)
