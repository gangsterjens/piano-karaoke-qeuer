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

if st.button('Refresh'):
    
    supabase = init_connection()
    queue_list = supabase.table("qeuer").select("*").eq("have_played", False).execute()
    
    df = pd.DataFrame(queue_list.data)
    df['created_at'] = pd.to_datetime(df['created_at'], format='%Y-%m-%dT%H:%M:%S', errors='coerce')
    df = df.sort_values('created_at')
    
    if 'buttons_clicked' not in st.session_state:
        st.session_state['buttons_clicked'] = set()
    
    df = df[['uuid', 'name', 'song', 'artist', 'have_played']]
    for index, row in df.iterrows():
        c1, c2, c3 = st.columns([5, 4, 2])
        c1.markdown(f"#### {row['name']}")
        c2.markdown(f"## {row['song']} | {row['artist']}")
    
        # Use a unique key for each button
        if c3.button('Done', key=row['uuid']):
            st.session_state.buttons_clicked.add(row['uuid'])
    
    # After the loop, check session state and update the database
    for uuid in st.session_state.buttons_clicked:
        response = supabase.table('qeuer').update({"have_played": True}).eq("uuid", uuid).execute()
        if response.error:
            st.error(f"Failed to update: {response.error.message}")
        else:
            st.success(f"Updated row with uuid {uuid}")
            # Optionally, remove uuid from session state after successful update
            st.session_state.buttons_clicked.remove(uuid)
            st.experimental_rerun()
    
        
