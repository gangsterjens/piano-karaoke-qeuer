import streamlit as st
from supabase import create_client, Client
import datetime
import time 
import pandas as pd
#import config as sst # for local dev
from src import upload_playlist as up
# Initialize connection.
# Uses st.cache_resource to only run once.
st.markdown("# Admin page <3")


sb = up.CreatePlaylist(
        api_key=st.secrets['API_KEY'],
        api_url=st.secrets['API_URL'],
        spotify_client_id=st.secrets['client_id'],
        spotify_client_secret=st.secrets['client_secret']
        )



@st.cache_resource
def init_connection():
    url = st.secrets["API_URL"]
    key = st.secrets["API_KEY"]
    return create_client(
        supabase_url=url, 
        supabase_key= key)



supabase = init_connection()
queue_list = supabase.table("qeuer").select("*").eq("have_played", False).execute()

t1, t2, t3 = st.tabs(['Kø', 'Legg til / Oppdater liste', 'Velg spilleliste'])

with t1:
    st.markdown('## Kø')

    if len(queue_list.data) > 0:
        df = pd.DataFrame(queue_list.data)
        df['created_at'] = pd.to_datetime(df['created_at'], format='%Y-%m-%dT%H:%M:%S', errors='coerce')
        df = df.sort_values('created_at')
        st.write(df.dtypes)
        
        if 'buttons_clicked' not in st.session_state:
            st.session_state['buttons_clicked'] = set()
        ### TEST ######################### Initialize session stategit 
            st.session_state.confirm_remove_all = False

    # Button to initiate the removal process

        if st.button('Fjern alle'):
            st.session_state.confirm_remove_all = True

    # If the user clicked 'Fjern alle', show confirmation
        if st.session_state.confirm_remove_all:
            r1, r2 = st.columns(2)
            r1.error("Er du sikker på at du vil fjerne alle?")
            if r2.button("YES få bort skitn"):
            # Execute the update query
                supabase.table('qeuer').update({"have_played": True}).eq("have_played", False).execute()
            # Reset confirmation state
                st.session_state.confirm_remove_all = False
                st.success("Alle oppføringer ble fjernet.")
        ### TEST ########################
        co1, co2, co3 = st.columns([3, 4, 2])
        co1.markdown('## Navn')
        co2.markdown(' ## Sang/ Artist')
        co3.write('Fjern hvis sang ferdig / ikke møtt opp')
        df = df[['uuid', 'name', 'song', 'artist', 'have_played', 'is_custom']]
        for index, row in df.iterrows():
            st.markdown("<hr>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns([3, 4, 2])
            c1.write(f"{row['name']}")
            custom_check = '✅' if row['is_custom'] == 'false' else  '❌'    
            c2.write(f" {row['song']} | {row['artist']} {custom_check}")
        
            # Use a unique key for each button
            if c3.button('Fjern', key=row['uuid']):
                st.session_state.buttons_clicked.add(row['uuid'])
        
        # After the loop, check session state and update the database
        for uuid in st.session_state.buttons_clicked:
            response = supabase.table('qeuer').update({"have_played": True}).eq("uuid", uuid).execute()
            st.success(f"Updated row with uuid {uuid}")
                # Optionally, remove uuid from session state after successful update
            st.session_state.buttons_clicked.remove(uuid)
            st.rerun()
    else:
        st.write('Ingen nummer i køen per nå')  
        
            
with t2:
    st.markdown("### Last opp / oppdater spilleliste")
    
    playlist_url = st.text_input('Legg inn delelink fra spotify her')
    owner = st.selectbox('Velg hvem som skal laste opp', ['Øystein','Martin','Vebjørn'])
    if st.button('Last opp'):
        playlist_url = playlist_url.split('/')[-1].split('?')[0]
        st.info(f'Lastet opp spilleliste med id: {playlist_url} for {owner}')
        songs = sb.get_playlist_songs(playlist_url)
        sb.add_playlist_to_db(songs, owner)
        st.info(f'Lastet opp spilleliste med id: {playlist_url} for {owner}')


with t3:
    st.markdown("### Velg hvem som spiller")
    users = sb.get_users()
    current_owner = sb.get_current_owner()
    st.markdown(f'Nåværende bruker på spilleliste er: **{current_owner}**', unsafe_allow_html=True)
    current_user = st.selectbox('Hvem spiller?', users)
    if st.button('Velg bruker'):
        sb.set_new_owner(current_user)
        st.info(f'Bruker {current_user} og dens spilleliste er valgt')
        check_user = sb.get_current_owner()
        st.success(f'✅ Nåværende bruker er {check_user}')
        time.sleep(3)
        st.rerun()
        
    



    

