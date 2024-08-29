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

queue_list = supabase.table("qeuer").select("*").execute()

df = pd.DataFrame(qeue_list.data).sort_values('created_at', ascending=False)

col1, col2, col3 = st.columns(3)

st.dataframe(df)
                                              
