import streamlit as st
import streamlit.components.v1 as components

# Streamlit app title
st.title("Embedding a Web Page in Streamlit")

# URL of the page to embed
url = st.text_input("enter url here")

# HTML for embedding the page using an iframe
iframe_html = f"""
<div id='rg_embed_link_378195' class='rg_embed_link' data-song-id='378195'>Read <a href='https://genius.com/Sia-chandelier-lyrics'>“Chandelier” by Sia</a> on Genius</div> <script crossorigin src='//genius.com/songs/378195/embed.js'></script>
"""

# Display the iframe in the Streamlit app
components.html(iframe_html, height=600)
