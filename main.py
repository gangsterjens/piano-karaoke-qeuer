import streamlit as st
from supabase import create_client, Client
import uuid
import datetime 

user_uuid = str(uuid.uuid4())

st.markdown("# Karaoke-kø")

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    url = st.secrets["API_URL"]
    key = st.secrets["API_KEY"]
    return create_client(url, key)

supabase = init_connection()

#test = supabase.table("qeuer").select("*").execute()
st.markdown("Skjema for sangforespørsel")
name = st.text_input("Hva er navnet ditt?")
song = st.text_input("Hvilken sang vil du spille?")
artist = st.text_input("Hva heter artisten?")

if button == True:
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    supabase.table("qeuer").insert({"uuid": user_uuid, 
                                    "name": name,
                                    "song": song,
                                    "artist": artist,
                                    "created_at": current_time}).execute()

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
#@st.cache_data(ttl=600)
#def run_query():
#    return supabase.table("qeuer").select("*").execute()

#rows = run_query()

# Print results.
#for row in rows.data:
#    st.write(row)
