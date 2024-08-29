import streamlit as st
from supabase import create_client, Client
import uuid
import datetime 




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

# Assuming supabase and user_uuid are already defined
with t2:
    test = supabase.table("song_list").select("*").execute()

    for index, el in enumerate(test.data):
        col1, col2 = st.columns([7, 2])
        col1.markdown(f" ### {el['artist']} {el['song']}")

        with col2:
            with st.expander("Velg"):  # This acts like a popover
                form_name = st.text_input('Navn', key=f"text_input_{index}_{uuid.uuid4()}")
                if st.button('Send inn', key=f"button_{index}_{uuid.uuid4()}"):  
                    current_time = datetime.utcnow()
                    supabase.table("qeuer").insert({
                        "uuid": user_uuid, 
                        "name": form_name,
                        "song": el['song'],
                        "artist": el['artist'],
                        "created_at": current_time
                    }).execute()
                    st.success('Nydelig! Du vil bli ropt opp når det er din tur!', icon="✅")

      
      
  
    st.markdown("<hr>", unsafe_allow_html=True)
