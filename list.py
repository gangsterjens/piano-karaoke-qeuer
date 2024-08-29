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
    df['created_at'] = pd.to_datetime(df['created_at'])
    df = df.sort_values('created_at', ascending=False)

    st.dataframe(df[['name', 'song', 'artist']])
                                              
