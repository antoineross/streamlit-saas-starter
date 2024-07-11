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

# test_mode = os.getenv("testing_mode")
# print("testing mode?", test_mode)
# if test_mode == "true":
#     stripe.api_key = os.getenv("stripe_api_key_test")

#     stripe_product_id_starter = os.getenv("stripe_product_id_starter_test")
#     stripe_product_id_teams = os.getenv("stripe_product_id_teams_test")
#     stripe_product_id_enterprise = os.getenv("stripe_product_id_enterprise_test")
#     print("Testing mode.")

# elif test_mode == "false":
#     stripe.api_key = os.getenv("stripe_api_key")

#     stripe_product_id_starter = os.getenv("stripe_product_id_starter")
#     stripe_product_id_teams = os.getenv("stripe_product_id_teams")
#     stripe_product_id_enterprise = os.getenv("stripe_product_id_enterprise")
#     print("Live mode.")

stripe_product_id_starter = "prod_PvKiYmxG9ClAK9"
stripe_product_id_teams = "prod_PvKiQbeE4tPVRV"
stripe_product_id_enterprise = "prod_PvKhUNRY3qPRbr"

stripe_to_supabase_mapping = {
    stripe_product_id_starter: 1,
    stripe_product_id_teams: 2,
    stripe_product_id_enterprise: 3
}

# stripe_link_starter = os.getenv("stripe_link_starter")
# stripe_link_teams = os.getenv("stripe_link_teams")
# stripe_link_enterprise = os.getenv("stripe_link_enterprise")

stripe_link_starter = "https://buy.stripe.com/cN2eYQ7dH04e2Fq4gi"
stripe_link_teams = "https://buy.stripe.com/4gw2c4eG94ku2Fq145"
stripe_link_enterprise = "https://buy.stripe.com/28og2UbtX04e7ZK288"


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
        "storageLimit": subscription_tier_data["storageLimit"],
        "tokenLimit": subscription_tier_data["tokenLimit"],
        "projectLimit": subscription_tier_data["projectLimit"]
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


def display_subscription_info(email):
    subscription_info = fetch_user_subscription(email)
    if subscription_info:
        # Fetch additional user details including the end date
        user_details = get_user_details(email)
        if user_details and 'subscriptionEndDate' in user_details:
            end_date = user_details['subscriptionEndDate']
            # Format the end date for display
            end_date_formatted = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S").strftime("%B %d, %Y")
            subscription_summary = f"Your current subscription is: {subscription_info[0]['name']}."
            description = f"Your current subscription ends on {end_date_formatted}."

        else:
            subscription_summary = f"Your current subscription is: {subscription_info[0]['name']}."
            description = f"End date is currently not available. Please check back later or contact support."

        cols = st.columns(3)
        ui.metric_card(
            title="Subscription Summary",
            content=subscription_summary,
            description=description,
            key="SubscriptionSummary"
        )
    else:
        st.markdown("You are not yet subscribed. Subscribe below: ")

        st.write("")
        st.write("---")
        st.subheader("Pricing")
        cols = st.columns(3)
        with cols[0]:
            with ui.card(key="pricing1"):
                ui.element("span", children=["Starter"], className="text-sm font-medium m-2", key="pricing_starter_0")

                ui.element("h1", children=["$0 per month"], className="text-2xl font-bold m-2", key="pricing_starter_1")

                ui.element("link_button", key="nst2_btn", text="Subscribe", variant="default", className="h-10 w-full rounded-md m-2", url=stripe_link_starter)
                
                ui.element("p", children=["Ideal for individual users who want to get started with Kawnix."], 
                            className="text-xs font-medium m-2 mt-2 mb-2", key="pricing_starter_2")

                ui.element("p", children=["This includes: "], 
                            className="text-muted-foreground text-xs font-medium m-2", key="pricing_enterprise_3") 
                ui.element("p", children=["- 1GB Storage Access."], 
                            className="text-muted-foreground text-xs font-medium m-1", key="pricing_starter_3")
                ui.element("p", children=["- 62,500 tokens per month."], 
                            className="text-muted-foreground text-xs font-medium m-1", key="pricing_starter_4")
                ui.element("p", children=["- 1 active project."], 
                            className="text-muted-foreground text-xs font-medium m-1", key="pricing_starter_5")
                
        with cols[1]:
            with ui.card(key="pricing2"):
                ui.element("span", children=["Teams"], className="text-sm font-medium m-2", key="pricing_pro_0")

                ui.element("h1", children=["$100 per month"], className="text-2xl font-bold m-2", key="pricing_pro_1")

                ui.element("link_button", key="nst2_btn", text="Subscribe", variant="default", className="h-10 w-full rounded-md m-2", url=stripe_link_teams)
                
        
                ui.element("p", children=["Perfect for small businesses requiring advanced features."], 
                            className="text-xs font-medium m-2 mt-2 mb-2", key="pricing_pro_2")
                
                ui.element("p", children=["This includes: "], 
                            className="text-muted-foreground text-xs font-medium m-2", key="pricing_enterprise_3")
                ui.element("p", children=["- 10GB Storage Access."], 
                            className="text-muted-foreground text-xs font-medium m-1", key="pricing_pro_3")
                ui.element("p", children=["- 625,000 tokens per month."], 
                            className="text-muted-foreground text-xs font-medium m-1", key="pricing_pro_4")
                ui.element("p", children=["- 10 active projects."], 
                            className="text-muted-foreground text-xs font-medium m-1", key="pricing_pro_5")
                

        with cols[2]:
            with ui.card(key="pricing3"):
                ui.element("h1", children=["Enterprise"], className="text-sm font-medium m-20 m-2", key="pricing_enterprise_0")

                ui.element("h1", children=["$500 per month"], className="text-2xl font-bold m-2", key="pricing_enterprise_1")
                ui.element("link_button", key="nst2_btn", text="Subscribe", variant="default", className="h-10 w-full rounded-md m-2", url=stripe_link_enterprise)

                ui.element("h2", children=["Designed for large companies and teams with specific needs."], 
                            className="text-xs font-medium m-2", key="pricing_enterprise_2")
                
                ui.element("p", children=["This includes: "], 
                            className="text-muted-foreground text-xs font-medium m-2", key="pricing_enterprise_3")        
                ui.element("p", children=["- 50GB Storage Access."], 
                            className="text-muted-foreground text-xs font-medium m-1", key="pricing_enterprise_3")
                ui.element("p", children=["- Unlimited tokens per month."], 
                            className="text-muted-foreground text-xs font-medium m-1", key="pricing_enterprise_4")
                ui.element("p", children=["- Unlimited active projects."], 
                            className="text-muted-foreground text-xs font-medium m-1", key="pricing_enterprise_5")



@st.cache_data
def fetch_user_projects(email):
    user_data = supabase.table("User").select("id").eq("email", email).execute()
    if user_data.data:
        user_id = user_data.data[0]['id']
        projects = supabase.table("Project").select("*").eq("ownerId", user_id).execute().data
        return projects
    return []

def get_user_details(email):
    user_data = supabase.table("User").select("*").eq("email", email).execute().data
    if user_data:
        return user_data[0]
    return None