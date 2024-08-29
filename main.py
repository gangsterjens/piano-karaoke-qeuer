import streamlit as st
from supabase import create_client, Client

st.markdown("# Karaoke-kø")

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    url = st.secrets["API_URL"]
    key = st.secrets["API_KEY"]
    return create_client(url, key)

supabase = init_connection()

test = supabase.table("qeuer").select("*").execute()

print(test)

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
#@st.cache_data(ttl=600)
#def run_query():
#    return supabase.table("qeuer").select("*").execute()

#rows = run_query()

# Print results.
#for row in rows.data:
#    st.write(row)
