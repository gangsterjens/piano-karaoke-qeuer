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
    
    # Initialize a session state to track the selected song and artist
    if 'selected_song' not in st.session_state:
        st.session_state['selected_song'] = None
        st.session_state['selected_artist'] = None
        st.session_state['form_key'] = None
    
    for el in test.data:
        # Displaying the song title and artist
        col1, col2, col3 = st.columns([4, 1, 3])
        col1.markdown(f"### {el['artist']} - {el['song']}")
        
        # Create a unique key for each song item
        unique_key = str(uuid.uuid4())
        
        # If the "Velg" button is clicked, store the song and artist in session state
        if col2.button('Velg', key='button'+unique_key):
            st.session_state['selected_song'] = el['song']
            st.session_state['selected_artist'] = el['artist']
            st.session_state['form_key'] = 'form' + unique_key
    
    # Check if a song has been selected and show the form
    if st.session_state['selected_song']:
        with st.form(key=st.session_state['form_key']):
            user_name = st.text_input("Your Name")
            submit_button = st.form_submit_button("Submit")
            
            if submit_button:
                # Store the selected song, artist, and user's name
                selected_song = st.session_state['selected_song']
                selected_artist = st.session_state['selected_artist']
                user_name_input = user_name
                
                st.write(f"You selected: {selected_song} by {selected_artist}")
                st.write(f"User: {user_name_input}")
                
                # Reset the session state to allow another selection
                st.session_state['selected_song'] = None
                st.session_state['selected_artist'] = None
                st.session_state['form_key'] = None

    st.markdown("<hr>", unsafe_allow_html=True)
