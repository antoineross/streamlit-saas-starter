from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
import streamlit_shadcn_ui as ui
from streamlit_extras.switch_page_button import switch_page 
from menu import menu_home
import requests

st.set_page_config(layout="wide",
                    page_title="Home",
                    page_icon="🌍",)

menu_home()

# --- PATH SETTINGS ---
THIS_DIR = Path(__file__).parent if "__file__" in locals() else Path.cwd()
# ASSETS_DIR = THIS_DIR / "assets"
STYLES_DIR = THIS_DIR / "styles"
CSS_FILE = STYLES_DIR / "main.css"

# Global Variables:
CONTACT_EMAIL = "developer.antoine@gmail.com"
APP_URL = "https://saas-starter.streamlit.app"
# Check if a user is logged in
if 'user' in st.session_state and st.session_state['user']:
    st.sidebar.markdown(f"*Welcome **{st.session_state['user']['email']}***")
else:
    with st.sidebar:
        st.write("User not logged in. Click the button below to log in.")
        # ui.element("link_button", key="LoginHome", text="Log In Here", variant="default", className="h-10 w-full rounded-md m-2", url="http://localhost:8501/Data_Catalog_NoAuth")
        ui.link_button("Log In", key="login", variant="default", url=APP_URL)

def load_css_file(css_file_path):
    with open(css_file_path) as f:
        return st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css_file(CSS_FILE)

# Customize the sidebar
github_link = """
GitHub Repository: <https://github.com/antoineross/streamlit-saas-starter>
"""

# Centering image and title using markdown
logo = "public/streamlit-logo.svg"

import base64
from pathlib import Path

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded
def img_to_html(img_path):
    img_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(
      img_to_bytes(img_path)
    )
    return img_html

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

# GitHub icon SVG
github_svg = """
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-github" viewBox="0 0 16 16">
  <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
</svg>
"""

# X (Twitter) icon SVG
twitter_svg = """
<svg xmlns="http://www.w3.org/2000/svg" shape-rendering="geometricPrecision" text-rendering="geometricPrecision" image-rendering="optimizeQuality" fill-rule="evenodd" clip-rule="evenodd" viewBox="0 0 512 509.64" width="16" height="16">
    <rect width="512" height="509.64" rx="115.61" ry="115.61"/>
    <path fill="#fff" fill-rule="nonzero" d="M323.74 148.35h36.12l-78.91 90.2 92.83 122.73h-72.69l-56.93-74.43-65.15 74.43h-36.14l84.4-96.47-89.05-116.46h74.53l51.46 68.04 59.53-68.04zm-12.68 191.31h20.02l-129.2-170.82H180.4l130.66 170.82z"/>
</svg>
"""

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
    st.markdown('<div style="text-align: center;">Join 10,000 others. Open source on GitHub.</div>', unsafe_allow_html=True)

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


st.header("A completely open-source Streamlit SaaS Template with a landing page, pricing, multiple-pages and authentication")


markdown = """
Streamlit SaaS Template is your all-in-one solution for creating, deploying, and managing SaaS applications with Streamlit. This completely open-source template simplifies the process of building scalable web applications with built-in authentication, API integration, and responsive design.

---

- **Want to build a SaaS product?** Dive into **Streamlit SaaS Template** and streamline your development process.
- **Looking for a customizable solution?** Discover **Streamlit SaaS Template**, an open-source platform for creating tailored applications.
- **Need seamless API integrations?** Experience **Streamlit SaaS Template**, designed to integrate effortlessly with various APIs.

Join us and take the first step towards revolutionizing your SaaS projects.

**Sign up now** to explore our template and elevate your development process!
"""

st.markdown(markdown)

ui.link_button("Get Started Now 🚀", key="get_started", variant="default", url="https://github.com/antoineross/streamlit-saas-starter")


st.write("")
st.write("---")
st.subheader("Features")

# --- Features ---
st.write("")
cols1 = st.columns(2)
with cols1[0]:
    st.markdown("#### A Good Looking Login Page")
    st.markdown("##### Secure and Easy to Use")
    st.markdown("""
Streamlit SaaS Template provides a fully-featured landing page that includes an FAQ section, a pricing table, login options, a contact form, feature highlights, and a hero section.

Key Features:
- Attractive Hero Section
- Detailed Features Overview
- Pricing Table
- FAQ Section
- Contact Form
    """)
    
with cols1[1]:
    st.image("public/demo-2.png", use_column_width=True)
    ui.link_button("Join our community on GitHub!", key="Feature2_button", variant="default", 
                    url="https://github.com/YourRepo/Streamlit-SaaS-Template")

st.write("")
st.write("---")

cols1 = st.columns(2)
with cols1[0]:
    st.markdown("#### Completely Open Source")
    st.markdown("##### Join Our Community and Contribute")
    st.markdown("""
Streamlit SaaS Template is an open-source project supported by a vibrant community of developers. We welcome contributions and encourage you to join us in improving this template.

Get involved:
- Report issues and suggest features
- Contribute code and documentation
- Share your projects and ideas
    """)
    
with cols1[1]:
    st.image("public/demo-1.png", use_column_width=True)
    ui.link_button("Start building your app today!", key="Feature3_button", variant="default",  url=f"https://github.com/antoineross/streamlit-saas-starter")

# --- DEMO ---
st.write("")
st.write("---")
st.subheader("Demo")
DEMO_VIDEO="https://www.youtube.com/watch?v=dQw4w9WgXcQ"

st.video(DEMO_VIDEO, format="video/mp4", start_time=0)

# --- Pricing ---
st.write("")
st.write("---")
st.subheader("Pricing")

stripe_link_starter = "https://buy.stripe.com/cN2eYQ7dH04e2Fq4gi"
stripe_link_teams = "https://buy.stripe.com/4gw2c4eG94ku2Fq145"
stripe_link_enterprise = "https://buy.stripe.com/28og2UbtX04e7ZK288"


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

# --- FAQ ---
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

# --- CONTACT FORM ---
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