from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
import streamlit_shadcn_ui as ui
from streamlit_extras.switch_page_button import switch_page
from menu import menu_home
import requests

# --- Page Configuration ---
st.set_page_config(
    layout="wide",
    page_title="Home",
    page_icon="🌍",
)

# --- Menu ---
menu_home()

# --- Path Settings ---
THIS_DIR = Path(__file__).parent if "__file__" in locals() else Path.cwd()
STYLES_DIR = THIS_DIR / "styles"
CSS_FILE = STYLES_DIR / "main.css"

# --- Global Variables ---
CONTACT_EMAIL = "developer.antoine@gmail.com"
APP_URL = "https://saas-starter.streamlit.app"

# --- User Authentication ---
if 'user' in st.session_state and st.session_state['user']:
    st.sidebar.markdown(f"*Welcome **{st.session_state['user']['email']}***")
else:
    with st.sidebar:
        st.write("User not logged in. Click the button below to log in.")
        ui.link_button("Log In", key="login", variant="default", url=APP_URL)

# --- Load CSS ---
def load_css_file(css_file_path):
    with open(css_file_path) as f:
        return st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css_file(CSS_FILE)

# --- Helper Functions ---
def add_vertical_space(height):
    st.markdown(f'<div style="height: {height}px;"></div>', unsafe_allow_html=True)

# --- Sidebar Customization ---
github_link = """
GitHub Repository: <https://github.com/antoineross/streamlit-saas-starter>
"""

# --- Logo and Title ---
logo = "public/streamlit-logo.svg"
with st.columns(3)[1]:
    st.image(logo)

st.markdown(
    f"""
    <div style="text-align: center;">
        <h1 style="margin-top: 10px;">SaaS Template</h1>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div style="text-align: center;">
        <h3 style="margin-top: 10px;">A completely open-source Streamlit SaaS Template with a custom Pricing Section with Landing Page, OAuth/Authentication, and Database using Supabase Postgres.</h3>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Load SVG ---
def load_svg(svg_file):
    return Path(svg_file).read_text()

github_svg = load_svg("public/github-logo.svg")
twitter_svg = load_svg("public/x-logo.svg")

# --- GitHub Stars ---
def get_github_repo_stars(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['stargazers_count']
    else:
        st.error("Failed to fetch data from GitHub API")
        return None

owner = "antoineross"
repo = "streamlit-saas-starter"

stars = get_github_repo_stars(owner, repo)

if stars is not None:
    st.markdown(f'<div style="text-align: center;">Join 10,000 others.</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="text-align: center;">Open source with {stars} ⭐ on GitHub!</div>', unsafe_allow_html=True)

    st.markdown(f"""
        <div style="display: flex; justify-content: center; gap: 10px; margin-top: 20px;">
            <a href="https://github.com/{owner}/{repo}" target="_blank" class="btn btn-default" style="display: inline-flex; align-items: center; gap: 5px; padding: 5px 10px; background-color: #24292e; color: white; text-decoration: none; border-radius: 5px;">
                {github_svg} Visit GitHub Repository
            </a>
            <a href="https://twitter.com/antoineross__" target="_blank" class="btn btn-default" style="display: inline-flex; align-items: center; gap: 5px; padding: 5px 10px; background-color: black; color: white; text-decoration: none; border-radius: 5px;">
                {twitter_svg} Follow @antoineross__ on X
            </a>
        </div>
    """, unsafe_allow_html=True)

add_vertical_space(200)

# --- Cloud Logo ---
github_svg_url = "https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg"
streamlit_svg_url = "https://streamlit.io/images/brand/streamlit-mark-color.svg"
stripe_svg_url = "https://upload.wikimedia.org/wikipedia/commons/b/ba/Stripe_Logo%2C_revised_2016.svg"
supabase_svg_url = "https://www.vectorlogo.zone/logos/supabase/supabase-icon.svg"

cloud_logo_html = f"""
<div style="display: flex; justify-content: center; align-items: center; flex-wrap: wrap; gap: 10px;">
    <div style="flex-basis: 10%; text-align: center;">
        <img src="{github_svg_url}" alt="GitHub Logo" style="width: 50px; height: auto;">
    </div>
    <div style="flex-basis: 10%; text-align: center;">
        <img src="{streamlit_svg_url}" alt="Streamlit Logo" style="width: 50px; height: auto;">
    </div>
    <div style="flex-basis: 10%; text-align: center;">
        <img src="{stripe_svg_url}" alt="Stripe Logo" style="width: 50px; height: auto;">
    </div>
    <div style="flex-basis: 10%; text-align: center;">
        <img src="{supabase_svg_url}" alt="Supabase Logo" style="width: 50px; height: auto;">
    </div>
</div>
"""

st.markdown(f'<div style="text-align: center;">Built with the following brands: </div>', unsafe_allow_html=True)
st.markdown(cloud_logo_html, unsafe_allow_html=True)

add_vertical_space(50)

# --- Features Section ---
st.write("")
st.write("---")
st.subheader("Features")

# Feature 1: Authentication and User Experience
cols1 = st.columns(2)
with cols1[0]:
    st.markdown("#### Authentication and User Experience")
    st.markdown("##### Secure and Modern Design")
    st.markdown("""
Streamlit SaaS Template offers a secure and seamless user experience, leveraging the power of Supabase for authentication and data management. 

Key Features:
- **Secure OAuth Authentication**: Integrate effortlessly with Supabase for secure user authentication and session management.
- **Modern UI with shadcn UI**: Utilize modern and attractive UI components for forms and other interactive elements.
- **User-Friendly Login Page**: A fully-featured landing page that includes an FAQ section, pricing table, login options, contact form, feature highlights, and a hero section.
- **Vertical Space Function**: Customizable vertical spacing to enhance layout and design.
    """)
with cols1[1]:
    st.image("public/demo-1.png", use_column_width=True)

add_vertical_space(50)

# Feature 2: Open Source and Community-Driven
st.write("")
st.write("---")

cols2 = st.columns(2)
with cols2[0]:
    st.markdown("#### Open Source and Community-Driven")
    st.markdown("##### Join and Contribute")
    st.markdown("""
Streamlit SaaS Template is completely open source, inviting contributions from developers around the world. Built using Supabase with Postgres functions for efficient data handling and secure storage.

Key Features:
- **Completely Open Source**: Join our vibrant community, report issues, suggest features, and contribute code and documentation.
- **Built with Supabase and Postgres**: Reliable backend infrastructure using Supabase with Postgres functions for efficient data management.
- **Logo Cloud**: Showcase technology stack or partners with a responsive and visually appealing logo cloud.
- **Github Stars**: Display the number of stars on your GitHub repository to attract more contributors.
    """)
with cols2[1]:
    st.image("public/demo-2.png", use_column_width=True)
    st.markdown(
        """
        <a href="https://github.com/antoineross/streamlit-saas-starter" target="_blank" class="btn btn-default" style="display: inline-flex; align-items: center; gap: 5px; padding: 5px 10px; background-color: #24292e; color: white; text-decoration: none; border-radius: 5px;">
            Start building your app today!
        </a>
        """,
        unsafe_allow_html=True,
    )

add_vertical_space(50)

# Feature 3: Comprehensive Dashboard and Hero Section
st.write("")
st.write("---")

cols3 = st.columns(2)
with cols3[0]:
    st.markdown("#### Comprehensive Dashboard and Hero Section")
    st.markdown("##### Monitor and Engage")
    st.markdown("""
Streamlit SaaS Template provides a comprehensive dashboard to monitor user subscriptions and a captivating hero section for better engagement.

Key Features:
- **Dashboard with Subscription Check**: Monitor user subscriptions and provide access to premium features based on subscription status.
- **Hero Section**: Engaging hero section with clear calls to action to captivate and convert visitors.
    """)
with cols3[1]:
    st.image("public/demo-3.png", use_column_width=True)
    st.markdown(
        """
        <a href="https://supabase.com" target="_blank" class="btn btn-default" style="display: inline-flex; align-items: center; gap: 5px; padding: 5px 10px; background-color: #24292e; color: white; text-decoration: none; border-radius: 5px;">
            Explore API Integrations
        </a>
        """,
        unsafe_allow_html=True,
    )


# --- Demo Section ---
st.write("")
st.write("---")
st.subheader("Demo")
DEMO_VIDEO = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

st.video(DEMO_VIDEO, format="video/mp4", start_time=0)

# --- Pricing Section ---
st.write("")
st.write("---")
st.subheader("Pricing")

stripe_link_starter = st.secrets["stripe_link_starter"]
stripe_link_teams = st.secrets["stripe_link_teams"]
stripe_link_enterprise = st.secrets["stripe_link_enterprise"]

cols = st.columns(3)
with cols[0]:
    with ui.card(key="pricing1"):
        ui.element("span", children=["Starter"], className="text-sm font-medium m-2", key="pricing_starter_0")
        ui.element("h1", children=["$0 per month"], className="text-2xl font-bold m-2", key="pricing_starter_1")
        ui.element("link_button", key="nst2_btn", text="Subscribe", variant="default", className="h-10 w-full rounded-md m-2", url=stripe_link_starter)
        ui.element("p", children=["Ideal for individual users who want to get started with the Streamlit SaaS Template."], 
                    className="text-xs font-medium m-2 mt-2 mb-2", key="pricing_starter_2")
        ui.element("p", children=["This includes: "], 
                    className="text-muted-foreground text-xs font-medium m-2", key="pricing_starter_3")
        ui.element("p", children=["- Access to all basic features."], 
                    className="text-muted-foreground text-xs font-medium m-1", key="pricing_starter_4")
        ui.element("p", children=["- Community support."], 
                    className="text-muted-foreground text-xs font-medium m-1", key="pricing_starter_5")
        ui.element("p", children=["- 1 active project."], 
                    className="text-muted-foreground text-xs font-medium m-1", key="pricing_starter_6")

with cols[1]:
    with ui.card(key="pricing2"):
        ui.element("span", children=["Teams"], className="text-sm font-medium m-2", key="pricing_pro_0")
        ui.element("h1", children=["$100 per month"], className="text-2xl font-bold m-2", key="pricing_pro_1")
        ui.element("link_button", key="nst2_btn", text="Subscribe", variant="default", className="h-10 w-full rounded-md m-2", url=stripe_link_teams)
        ui.element("p", children=["Perfect for small businesses requiring advanced features."], 
                    className="text-xs font-medium m-2 mt-2 mb-2", key="pricing_pro_2")
        ui.element("p", children=["This includes: "], 
                    className="text-muted-foreground text-xs font-medium m-2", key="pricing_pro_3")
        ui.element("p", children=["- 10GB Storage Access."], 
                    className="text-muted-foreground text-xs font-medium m-1", key="pricing_pro_4")
        ui.element("p", children=["- 625,000 API calls per month."], 
                    className="text-muted-foreground text-xs font-medium m-1", key="pricing_pro_5")
        ui.element("p", children=["- 10 active projects."], 
                    className="text-muted-foreground text-xs font-medium m-1", key="pricing_pro_6")
        ui.element("p", children=["- Priority email support."], 
                    className="text-muted-foreground text-xs font-medium m-1", key="pricing_pro_7")

with cols[2]:
    with ui.card(key="pricing3"):
        ui.element("span", children=["Enterprise"], className="text-sm font-medium m-2", key="pricing_enterprise_0")
        ui.element("h1", children=["$500 per month"], className="text-2xl font-bold m-2", key="pricing_enterprise_1")
        ui.element("link_button", key="nst2_btn", text="Subscribe", variant="default", className="h-10 w-full rounded-md m-2", url=stripe_link_enterprise)
        ui.element("p", children=["Designed for large companies and teams with specific needs."], 
                    className="text-xs font-medium m-2", key="pricing_enterprise_2")
        ui.element("p", children=["This includes: "], 
                    className="text-muted-foreground text-xs font-medium m-2", key="pricing_enterprise_3")        
        ui.element("p", children=["- 50GB Storage Access."], 
                    className="text-muted-foreground text-xs font-medium m-1", key="pricing_enterprise_4")
        ui.element("p", children=["- Unlimited API calls per month."], 
                    className="text-muted-foreground text-xs font-medium m-1", key="pricing_enterprise_5")
        ui.element("p", children=["- Unlimited active projects."], 
                    className="text-muted-foreground text-xs font-medium m-1", key="pricing_enterprise_6")
        ui.element("p", children=["- Dedicated account manager."], 
                    className="text-muted-foreground text-xs font-medium m-1", key="pricing_enterprise_7")
        ui.element("p", children=["- 24/7 priority support."], 
                    className="text-muted-foreground text-xs font-medium m-1", key="pricing_enterprise_8")

# --- FAQ Section ---
st.write("")
st.write("---")
st.subheader("FAQ")

faq = {
    "What is the Streamlit SaaS Template?": "Streamlit SaaS Template is your comprehensive solution for building, deploying, and managing SaaS applications with Streamlit. This open-source template simplifies the development process with built-in authentication, API integration, and responsive design.",
    "How can I customize the Streamlit SaaS Template?": "The Streamlit SaaS Template is highly customizable. You can easily modify the UI components, integrate various APIs, and adjust the design to match your brand's identity.",
    "What features does the Streamlit SaaS Template include?": "The template includes a landing page with FAQ, pricing table, login page, contact form, feature highlights, and a hero section. It also offers a modern, user-friendly login page, and it's completely open-source for community contributions."
}
for question, answer in faq.items():
    with st.expander(question):
        st.write(answer)

# --- Contact Form ---
# video tutorial: https://youtu.be/FOULV9Xij_8
st.write("")
st.write("---")
st.subheader(":mailbox: Have A Question? Ask Away!")
# Create the form using ui.input and ui.textarea
name_input = ui.input(default_value="", placeholder="Your name", key="name_input")
email_input = ui.input(default_value="", placeholder="Your email", key="email_input")
message_input = ui.textarea(default_value="", placeholder="Your Message Here", key="message_input")

st.write("---")  # Separator
submit_button = st.button("Submit")

# Check if the submit button is clicked
if submit_button:
    st.write("Message sent!")
    # st.write("Name:", name_input)
    # st.write("Email:", email_input)
    # st.write("Message:", message_input)

    # JavaScript to dynamically create a hidden form and submit it
    st.markdown(
        f"""
        <script>
        // Create a hidden form
        var form = document.createElement("form");
        form.setAttribute("method", "post");
        form.setAttribute("action", "https://formsubmit.co/{CONTACT_EMAIL}");

        // Add hidden input fields
        var inputName = document.createElement("input");
        inputName.setAttribute("type", "hidden");
        inputName.setAttribute("name", "name");
        inputName.setAttribute("value", "{name_input}");
        form.appendChild(inputName);

        var inputEmail = document.createElement("input");
        inputEmail.setAttribute("type", "hidden");
        inputEmail.setAttribute("name", "email");
        inputEmail.setAttribute("value", "{email_input}");
        form.appendChild(inputEmail);

        var inputMessage = document.createElement("input");
        inputMessage.setAttribute("type", "hidden");
        inputMessage.setAttribute("name", "message");
        inputMessage.setAttribute("value", "{message_input}");
        form.appendChild(inputMessage);

        // Add the hidden form to the body and submit it
        document.body.appendChild(form);
        form.submit();
        </script>
        """,
        unsafe_allow_html=True
    )