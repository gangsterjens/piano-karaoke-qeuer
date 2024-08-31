import streamlit as st
from supabase import create_client, Client
import uuid
import datetime 

user_uuid = str(uuid.uuid4())

st.markdown("# Påmelding Karaoke/Beat for beat - Broker! ")

st.markdown(" ## Endelig kan du være den fulle jævelen som har så lyst å stjele showet fra mannen bak pianoet på pianobar, når vi kjører live-karakoe")

st.info("Ikveld kjører vi duell på grab the mic! To og to kommer opp, den som tar mic'n først og nailer sangen vinner! Men om du ikke nailer sangen, vinner du ikke og den andre kan ta over  ")
            



# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    url = st.secrets["API_URL"]
    key = st.secrets["API_KEY"]
    return create_client(url, key)

supabase = init_connection()

name = st.text_input("Hva er navnet ditt?")

if st.button("Send inn!"):
    if len(name) == 0:
        st.error("Vennligst skriv navnet ditt")
    else:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        supabase.table("duell_list").insert({
                                        "name": name}).execute()
        st.success('Rått! Du vil bli ropt opp når det er din tur!', icon="✅")

