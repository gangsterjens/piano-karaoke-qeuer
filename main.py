import streamlit as st
from supabase import create_client, Client
import uuid
import datetime 

def send_in_from_list(user_uuid, form_name, song, artist):
                    supabase.table("qeuer").insert({"uuid": user_uuid, 
                                                "name": form_name,
                                                "song": song,
                                                "artist": artist,
                                                "created_at": current_time}).execute()
                    st.success('Nydelig! Du vil bli ropt opp når det er din tur!', icon="✅")


t1, t2 = st.tabs(['Skjema', 'Liste'])

with t1:
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
    
    if st.button("Send inn!"):
        if len(name) == 0:
            st.error("Vennligst skriv navnet ditt")
        
        elif len(song) == 0:
            st.error("Sang mangler")
        
        elif len(artist) == 0:
            st.error("Artist mangler")
        else:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            supabase.table("qeuer").insert({"uuid": user_uuid, 
                                            "name": name,
                                            "song": song,
                                            "artist": artist,
                                            "created_at": current_time}).execute()
            st.success('Rått! Du vil bli ropt opp når det er din tur!', icon="✅")
    
# Initialize a session state variable to track which form to show


with t2:
  test = supabase.table("song_list").select("*").execute()
  
  for el in test.data:
    col1, col2 = st.columns([7, 2])
    col1.markdown(f" ### {el['artist']} {el['song']}")
    unique_key = str(uuid.uuid4())
    with col2.popover('Velg'):
      form_name = st.text_input('Navn')
      if st.button('Send inn', key=unique_key):
        send_in_from_list(unique_key, form_name, el['song'], el['artist'])
      
      
  
    st.markdown("<hr>", unsafe_allow_html=True)
