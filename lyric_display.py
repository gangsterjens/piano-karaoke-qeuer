import streamlit as st
import streamlit.components.v1 as components

# Streamlit app title
st.title("Embedding a Web Page in Streamlit")

# URL of the page to embed
url = st.text_input("enter url here)

# HTML for embedding the page using an iframe
iframe_html = f"""
<iframe src="{url}" width="100%" height="600px" frameborder="0"></iframe>
"""

# Display the iframe in the Streamlit app
components.html(iframe_html, height=600)
