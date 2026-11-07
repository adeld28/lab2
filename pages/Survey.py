# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("The Suits Fan Survey 📝")
st.write("Two quick questions, that's it. Who's your favorite character, and how deep into the show did you get?")
st.write("Hit submit and your answer shows up on the **Visuals** page right away. No pressure... but Harvey's watching. 😎")

# the characters people can pick from
characters = ["Harvey Specter", "Mike Ross", "Donna Paulsen", "Louis Litt", "Jessica Pearson", "Rachel Zane"]

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("survey_form"):
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
    category_input = st.selectbox("Who is your favorite Suits character?", characters)
    value_input = st.text_input("How many seasons of Suits have you watched? (0-9)")

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data")

    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
        # take out any extra spaces the user typed
        value_input = value_input.strip()

        # make sure they typed a whole number from 0 to 9
        if value_input.isdigit() and int(value_input) <= 9:
            # make the new row, like "Harvey Specter,9"
            new_row = f"{category_input},{value_input}\n"

            # open data.csv in append mode ('a') so we add to the end instead of erasing it
            with open("data.csv", "a") as file:
                file.write(new_row)

            st.success("Your data has been submitted!")
            st.write(f"You entered: **Category:** {category_input}, **Value:** {value_input}")
        else:
            st.error("Please type a whole number from 0 to 9 for the seasons.")


# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv('data.csv')
    # Display the DataFrame as a table.
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")