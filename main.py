import streamlit as st
from supabase import create_client, Client
import uuid
import datetime 

user_uuid = str(uuid.uuid4())
            
t2, t1, t3 = st.tabs(['Liste', 'Andre forslag', 'tilbakemeldinger'])

with t1:
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
# Initialize session state for text inputs and button clicks
if "submitted" not in st.session_state:
    st.session_state.submitted = {}

with t2:
    st.markdown("Her er en liste med sanger vi kan")
    
    test = supabase.table("song_list").select("*").execute()
    search_query = st.text_input("Søk etter sang eller artist")
    filtered_data = [el for el in test.data if search_query.lower() in el['artist'].lower() or search_query.lower() in el['song'].lower()]


    for index, el in enumerate(filtered_data):
        st.markdown("<hr>", unsafe_allow_html=True)
        col1, col2 = st.columns([7, 2])
        col1.markdown(f" ### {el['artist']} |     {el['song']}")

        with col2:
            # Unique keys for each input and button
            text_input_key = f"text_input_{index}"
            button_key = f"button_{index}"

            # Check if form has been submitted for this song
            if button_key not in st.session_state.submitted:
                st.session_state.submitted[button_key] = False

        #if not st.session_state.submitted[button_key]:
            form_name = st.text_input('Skriv inn navnet ditt her', key=text_input_key)
            button_send = st.button('Send inn', key=button_key)
            if button_send and len(form_name) == 0:
                st.error('Skriv inn navnet ditt')
            elif button_send and len(form_name) > 0:
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                supabase.table("qeuer").insert({
                    "uuid": user_uuid, 
                    "name": form_name,
                    "song": el['song'],
                    "artist": el['artist'],
                    "created_at": current_time
                }).execute()
                st.session_state.submitted[button_key] = True
                st.success('Nydelig! Du vil bli ropt opp når det er din tur!', icon="✅")
            #else:
#                st.write("Request already submitted.")

with t3:
    st.info("Siden dette er første gang vi kjører dette, tar vi gjerne tilbakemeldinger!")
    feedback = st.text_input('Kom med feedback her <3')
    button_feedback = st.button('Send inn!', key='feedback')
    if (len(feedback) > 0) & (len(feedback) < 200) & button_feedback:
        supabase.table("feedback").insert({"feedback_txt": feedback}).execute()
        st.success('Takk for din tilbakemelding!')

    
