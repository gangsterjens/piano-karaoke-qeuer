import streamlit as st
from supabase import create_client, Client
import uuid
import datetime 
from src import upload_playlist as up

#### local
import config as sst
############

sb = up.SBClient(
        api_url = st.secrets["API_URL"],
        api_key = st.secrets["API_KEY"]
        )

current_owner = sb.get_current_owner()



if 'user_uuid' not in st.session_state:
    st.session_state['user_uuid'] = str(uuid.uuid4())

user_uuid = st.session_state['user_uuid']
request_uuid = str(uuid.uuid4())
st.markdown("# Påmelding Karaoke - Broker! ")

st.markdown(" ## Endelig kan du være den fulle jævelen som har så lyst å stjele showet fra mannen bak pianoet på pianobar, når vi kjører live-karakoe")
            
st.info("""
            Velg enten fra listen av sanger vi vet vi kan, eller kom med forslag til sanger (men er mulig vi ikke kan den) \n
            Kom gjerne opp til oss og spør om vi kan sangen!             \n
            Appen her er ganske fersk også, så om den failer, kom og si ifra!
"""
       )
            
t2, t1, t3, 4 = st.tabs(['Liste', 'Andre forslag', 'Ta sjansen!' ,'Tilbakemeldinger'])

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
    st.info("Merk, det er ingen lovnad om at vi kan sangen. Og sære sanger som ingen kan, vil ikke bli prioritert")        
    
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
            supabase.table("qeuer").insert({"uuid": request_uuid, 
                                            "name": name,
                                            "song": song,
                                            "artist": artist,
                                            "created_at": current_time,
                                            "is_custom":True,
                                            "user_uuid": user_uuid,
                                            "present_owner": current_owner
                                           }).execute()
            st.success('Rått! Du vil bli ropt opp når det er din tur!', icon="✅")

# Assuming supabase and user_uuid are already defined
# Initialize session state for text inputs and button clicks
if "submitted" not in st.session_state:
    st.session_state.submitted = {}

with t2:
    st.markdown("Her er en liste med sanger vi kan")
    
    test = supabase.table("current_playlist").select("*").eq("owner", current_owner).execute()
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
                    "uuid": request_uuid, 
                    "name": form_name,
                    "song": el['song'],
                    "artist": el['artist'],
                    "created_at": current_time,
                    "is_custom": False,
                    "user_uuid": user_uuid,
                    "present_owner": current_owner
                }).execute()
                st.session_state.submitted[button_key] = True
                st.success('Nydelig! Du vil bli ropt opp når det er din tur!', icon="✅")
            #else:
#                st.write("Request already submitted.")
with t3:
     st.markdown("# Ta sjansen! 🦄")
     st.markdown("""
             ## Kommer du ikke på en sang du vil spille? 
             Skriv inn navnet ditt her, og få en sang utdelt. Mest sannsynlig er det en allsang, og en du kjenner!
             """)
    chance_name = st.text_input('Skriv inn navnet ditt her')
    chance_butt = st.button('Send inn')
    if chance_butt and len(chance_name) == 0:
        st.error('Skriv inn navnet ditt')
    elif chance_butt and len(chance_name) > 0:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        supabase.table("qeuer").insert({
                "uuid": request_uuid, 
                "name": chance_name,
                "song": 'SJANSE',
                "artist": 'SJANSE',
                "created_at": current_time,
                "is_custom": False,
                "user_uuid": user_uuid,
                "present_owner": current_owner
        }).execute()
        st.session_state.submitted[button_key] = True
        st.success('Nydelig! Du vil bli ropt opp når det er din tur!', icon="✅")
            
        
with t4:
    st.info("Si gjerne hva du savner, hva du digger, og tja, hva du ikke liker! ")
    feedback = st.text_input('Kom med feedback her <3')
    button_feedback = st.button('Send inn!', key='feedback')
    if (len(feedback) > 0) & (len(feedback) < 200) & button_feedback:
        supabase.table("feedback").insert({"feedback_txt": feedback}).execute()
        st.success('Takk for din tilbakemelding!')

    
