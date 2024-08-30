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

    df = pd.DataFrame(queue_list.data)
    df['created_at'] = pd.to_datetime(df['created_at'], format='%Y-%m-%dT%H:%M:%S', errors='coerce')
    df = df.sort_values('created_at', ascending=False)
    
    df = df[['uuid', 'name', 'song', 'artist', 'have_played']]
    df = df[df['have_played'] == False]
    for index, row in df.iterrows():
        c1, c2, c3 = st.columns([5,4, 1])
        c1.markdown(f"#### {row['name']}")
        c2.markdown(f"## {row['song']} | {row['artist']}")
        if c3.button('Done', key=row['uuid']):
            supabase.table('qeuer').update({"have_played": True}).eq("uuid", row['uuid']).execute()
        
                                              
