import streamlit as st
from supabase import create_client, Client
from streamlit_supabase_auth import login_form, logout_button
import stripe
import streamlit_shadcn_ui as ui
from datetime import datetime, timedelta
from streamlit.proto.Skeleton_pb2 import Skeleton as SkeletonProto
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
# Initialization with Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

stripe_product_id_starter = ""
stripe_product_id_teams = ""
stripe_product_id_enterprise = ""

stripe_to_supabase_mapping = {
    stripe_product_id_starter: 1,
    stripe_product_id_teams: 2,
    stripe_product_id_enterprise: 3
}

stripe_link_starter = "https://buy.stripe.com/"
stripe_link_teams = "https://buy.stripe.com/"
stripe_link_enterprise = "https://buy.stripe.com/"


def ensure_user_in_database(user_id: str, email: str, name: str = None):
    user_data = supabase.table("User").select("*").eq("id", user_id).execute()
    if not user_data.data:
        user = {
            "id": user_id,
            "email": email,
            "name": name
        }
        insert_data = supabase.table("User").insert(user).execute()
        if insert_data.data == None:
            st.error(f"Failed to create user in the database.")
        else:
            st.success("User added to the database.")
    return user_data.data

def update_user_subscription(email, subscription_id, subscription_tier_data):
    current_date = datetime.now()

    # Add 30 days to get the end date
    end_date = current_date + timedelta(days=30)

    # Convert both dates to strings in the desired format
    datetime_format = "%Y-%m-%dT%H:%M:%SZ"  # Example format
    current_date_str = current_date.strftime(datetime_format)
    end_date_str = end_date.strftime(datetime_format)
    print("START DATE", current_date_str)
    print("END DATE", end_date_str)

    update_response = supabase.table("User").update({
        "subscriptionTierId": subscription_id,
        "subscriptionStartDate": current_date_str,
        "subscriptionEndDate": end_date_str,
    }).eq("email", email).execute()

    success = update_response.data is not None
    print(f"Subscription update success: {success}, Error: {update_response.error}")
    return success

def is_active_subscriber(email: str) -> bool:
    customers = stripe.Customer.list(email=email)
    try:
        customer = customers.data[0]
    except IndexError:
        return False

    subscriptions = stripe.Subscription.list(customer=customer["id"])
    st.session_state.subscriptions = subscriptions
    # st.text(subscriptions.data[0])
    # st.text(subscriptions.data[0].plan.product)

    return len(subscriptions.data) > 0 and subscriptions.data[0].status == "active"

@st.cache_data
def fetch_user_subscription(email):
    print("Fetching user subscription for:", email)
    if is_active_subscriber(email):
        user_data = supabase.table("User").select("*").eq("email", email).execute()
        if user_data.data:
            user = user_data.data[0]
            print("User data found:", user)
            if user['subscriptionTierId'] is None:
                stripe_subscription_id = st.session_state.subscriptions.data[0].plan.product
                print("Stripe subscription ID:", stripe_subscription_id)
                if stripe_subscription_id in stripe_to_supabase_mapping:
                    supabase_subscription_id = stripe_to_supabase_mapping[stripe_subscription_id]
                    print("Mapped Supabase subscription ID:", supabase_subscription_id)
                    subscription_tier_data = supabase.table("SubscriptionTier").select("*").eq("id", supabase_subscription_id).execute().data[0]
                    if update_user_subscription(email, supabase_subscription_id, subscription_tier_data):
                        return subscription_tier_data
            else:
                return supabase.table("SubscriptionTier").select("*").eq("id", user['subscriptionTierId']).execute().data
        else:
            print("No user data found.")
    else:
        print("User is not an active subscriber.")
    return None

def get_user_details(email):
    user_data = supabase.table("User").select("*").eq("email", email).execute().data
    if user_data:
        return user_data[0]
    return None