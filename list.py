import streamlit as st
from supabase import create_client, Client
import datetime 
import pandas as pd

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    url = st.secrets["API_URL"]
    key = st.secrets["API_KEY"]
    return create_client(url, key)

supabase = init_connection()

if st.button('Last inn:'):
    queue_list = supabase.table("qeuer").select("*").execute()

    df = pd.DataFrame(queue_list.data).sort_values('created_at', ascending=False)

    c1, c2, c3 = st.columns(3)
    c1.text('NAVN')
    c2.text('SANG')
    c3.text('ARTIST')
    for index, row in df.head(5).iterrows():
        c1.text(row['name'])
        c2.text(row['song'])
        c3.text(row['artist'])
        c1.text('----')
        c2.text('----')
        c3.text('----')
                                              
