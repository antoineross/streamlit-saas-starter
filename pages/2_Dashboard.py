import streamlit as st
import streamlit_shadcn_ui as ui
from datetime import datetime, timedelta
from streamlit_supabase_auth import login_form, logout_button

import random
import pandas as pd
from streamlit_lightweight_charts import renderLightweightCharts
import streamlit_lightweight_charts.dataSamples as data
from menu import menu_with_redirect

# Initialization with Supabase credentials
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

test_mode = st.secrets["testing_mode"]

if test_mode == "true":
    print("Testing mode.")
elif test_mode == "false":
    print("Live mode.")

st.set_page_config(
    page_title="User Dashboard",
    page_icon="🧑🏻‍💻",
    layout="centered"
)

menu_with_redirect()


def generate_fake_data():
    token_usage = random.randint(1000, 10000)
    storage_used = round(random.uniform(10.0, 50.0), 2)
    project_count = random.randint(1, 10)
    max_token_usage = 15000
    max_storage = 100
    max_projects = 20
    return token_usage, storage_used, project_count, max_token_usage, max_storage, max_projects

def generate_fake_project_data(num_projects):
    projects = []
    for i in range(num_projects):
        project = {
            'name': f'Project {i+1}',
            'created_at': datetime.now() - timedelta(days=random.randint(1, 100))
        }
        projects.append(project)
    return projects

def main():
    # Configure Supabase authentication
    session = login_form(url=SUPABASE_URL, apiKey=SUPABASE_KEY, providers=["github", "google"])

    if session:
        user_id = session['user']['id']
        user_email = session['user']['email']
        user_name = session['user']['user_metadata']['name']
        
        st.header("Dashboard")

        token_usage, storage_used, project_count, max_token_usage, max_storage, max_projects = generate_fake_data()

        cols = st.columns(3)
        with cols[0]:
            ui.metric_card(
                title="Token Usage",
                content=f"{token_usage}/{max_token_usage}",
                description="Your token consumption",
                key="token_usage"
            )
        with cols[1]:
            ui.metric_card(
                title="Storage Used",
                content=f"{storage_used} GB / {max_storage} GB",
                description="Your storage usage",
                key="storage_usage"
            )
        with cols[2]:
            ui.metric_card(
                title="Projects",
                content=f"{project_count}/{max_projects}",
                description="Number of projects",
                key="project_count"
            )

        st.subheader("Project Details")
        projects = generate_fake_project_data(project_count)
        for project in projects:
            st.write(f"**{project['name']}** - Created at: {project['created_at']}")

        st.subheader("Token Usage Chart")
        chartOptions = {
            "layout": {
                "textColor": 'black',
                "background": {
                    "type": 'solid',
                    "color": 'white'
                }
            }
        }

        renderLightweightCharts([
            {
                "chart": chartOptions,
                "series": [{
                    "type": 'Area',
                    "data": data.seriesMultipleChartArea01,
                    "options": {}
                }],
            }
        ], 'area')

        st.subheader("Data Tables")
        token_usage_data = {
            'Token Usage': [token_usage],
            'Max Token Usage': [max_token_usage]
        }
        storage_data = {
            'Storage Used (GB)': [storage_used],
            'Max Storage (GB)': [max_storage]
        }
        projects_data = {
            'Project Count': [project_count],
            'Max Projects': [max_projects]
        }

        st.table(pd.DataFrame(token_usage_data))
        st.table(pd.DataFrame(storage_data))
        st.table(pd.DataFrame(projects_data))

        # Sidebar with logout
        with st.sidebar:
            st.markdown(f"*Welcome **{session['user']['email']}***")
            if logout_button(url=SUPABASE_URL, apiKey=SUPABASE_KEY):
                st.session_state['user'] = None
                st.experimental_rerun()

if __name__ == "__main__":
    main()
