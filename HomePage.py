# This creates the main landing page for the Streamlit application.
# Contains an introduction to the project and guide users to other pages.

# Import Streamlit
import streamlit as st

# st.set_page_config() is used to configure the page's appearance in the browser tab.
# It's good practice to set this as the first Streamlit command in your script.
st.set_page_config(
    page_title="Homepage",  # The title that appears in the browser tab
    page_icon="🏠",         # An emoji that appears as the icon in the browser tab
)

# WELCOME PAGE TITLE
st.title("Suits by the Numbers 💼📊")

# INTRODUCTORY TEXT
st.write("""
Welcome! If you've ever watched Harvey Specter walk into a room and win an argument
without breaking a sweat, you're in the right place. This site breaks down the show
**Suits** with real data about the series *and* what actual fans think about it.

Use the sidebar on the left to get around.

### What's inside:
- **Survey**: Pick your favorite character and tell me how much of the show you've watched. Your answer gets added to the data instantly.
- **Visuals**: See how many episodes each season had, play around with the seasons, and find out who the fans' favorite character really is.

*"I don't have dreams, I have goals."* Let's see what the numbers say.

This project is part of my CS 1301 Lab 2.
""")

# OPTIONAL: ADD AN IMAGE
# 1. Navigate to the 'images' folder in your Lab02 directory.
# 2. Place your image file (e.g., 'welcome_image.png') inside that folder.
# 3. Uncomment the line below and change the filename to match yours.
#
# st.image("images/welcome_image.png")
