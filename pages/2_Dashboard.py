import streamlit as st
import streamlit_shadcn_ui as ui
from datetime import datetime, timedelta
from streamlit_supabase_auth import login_form, logout_button
import random
import pandas as pd
from streamlit_lightweight_charts import renderLightweightCharts
import streamlit_lightweight_charts.dataSamples as data
from menu import menu_with_redirect
# import stripe
# from server import ensure_user_in_database, fetch_user_subscription, get_user_details, fetch_user_projects, display_subscription_info

# Initialization with Supabase credentials
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

test_mode = st.secrets["testing_mode"]
# if test_mode == "true":
#     stripe.api_key = st.secrets["stripe_api_key_test"]
#     print("Testing mode.")
# elif test_mode == "false":
#     stripe.api_key = st.secrets["stripe_api_key"]
#     print("Live mode.")

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
        
        # Ensure user exists in database
        # ensure_user_in_database(user_id, user_email, user_name)

        st.header("Dashboard")

        # Toggle button to simulate subscription status
        subscribed = st.sidebar.checkbox("Toggle Subscription Status")

        if subscribed:
            st.success("User is subscribed")
            # Fetch user details and subscription info if subscribed
            # user_details = get_user_details(user_email)
            # subscription_info = fetch_user_subscription(user_email)

            # Simulate user details and subscription info
            user_details = {
                'tokenUsage': 5000,
                'storageUsed': 25.5,
            }
            subscription_info = [{
                'tokenLimit': 15000,
                'storageLimit': 100,
                'projectLimit': 20
            }]

            token_usage = user_details.get('tokenUsage', 0)
            storage_used = user_details.get('storageUsed', 0)
            projects = generate_fake_project_data(5)  # Replace with: fetch_user_projects(user_email)
            project_count = len(projects)

            max_token_usage = subscription_info[0]['tokenLimit']
            max_storage = subscription_info[0]['storageLimit']
            max_projects = subscription_info[0]['projectLimit']

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
            for project in projects:
                st.write(f"**{project['name']}** - Created at: {project['created_at']}")
            
            # display_subscription_info(user_email)
        else:
            st.warning("User is not subscribed")
            # Generate fake data if not subscribed
            token_usage, storage_used, project_count, max_token_usage, max_storage, max_projects = generate_fake_data()
            cols = st.columns(3)
            with cols[0]:
                ui.metric_card(
                    title="Token Usage",
                    content=f"25/100",
                    description="Your token consumption",
                    key="token_usage"
                )
            with cols[1]:
                ui.metric_card(
                    title="Storage Used",
                    content=f"1.7 GB / 5 GB",
                    description="Your storage usage",
                    key="storage_usage"
                )
            with cols[2]:
                ui.metric_card(
                    title="Projects",
                    content=f"2/3",
                    description="Number of projects",
                    key="project_count"
                )
                
            st.subheader("Project Details")
            projects = generate_fake_project_data(2)
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
