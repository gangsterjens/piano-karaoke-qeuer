import streamlit as st
import streamlit.components.v1 as components


st.input('Skriv inn sang')

st.input('Skriv inn artist')

if st.button('Find lyrics'):
# Streamlit app ti
  text = get_g_lyrics(song, artist)
  st.markdown(text)
