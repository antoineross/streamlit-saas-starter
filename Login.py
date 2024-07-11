import streamlit as st
from menu import menu, menu_with_redirect, unauthenticated_menu
from streamlit_supabase_auth import login_form, logout_button
from supabase import create_client, Client
import streamlit_shadcn_ui as ui
import os
from dotenv import find_dotenv, load_dotenv
import shutil
import logging
from bs4 import BeautifulSoup
import pathlib

load_dotenv(find_dotenv())
st.set_option("client.showSidebarNavigation", False)
st.set_page_config(
    page_title="Streamlit SaaS Starter",
    page_icon="🌍",
    layout="centered"
)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("Streamlit SaaS Starter Login Page")

def main():
    # Configure Supabase authentication
    logo = "public/logo.png"

    left_co, cent_co,last_co = st.columns(3)

    with cent_co:
        st.image(logo)

    session = login_form(
        url=SUPABASE_URL,
        apiKey=SUPABASE_KEY,
        providers=["github", "google"]
    )
    if session:
        menu()
        # Store user session in Streamlit session state
        st.session_state['user'] = session['user']

        # Perform checks of user session here. 
        st.session_state.role = "user"

        # # Update query param to reset url fragments
        st.query_params.login = ["success"]

        with st.sidebar:
            st.markdown(f"**Logged in as: *{session['user']['email']}***")
            if logout_button(url=SUPABASE_URL,apiKey=SUPABASE_KEY):
                print("Logging out.")

    if not session:
        unauthenticated_menu()

if __name__ == "__main__":
    main()


