import streamlit as st
import re

def signup():
    st.title("Sign Up Page")

    # Get user inputs
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    # Check if passwords match
    if password != confirm_password:
        st.error("Passwords do not match.")
        return

    # Validate email
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        st.error("Invalid email address.")
        return

    # Check if the user clicked the "Sign Up" button
    if st.button("Sign Up"):
        # Perform sign-up logic (you can customize this part based on your needs)
        st.success(f"Welcome, {username}! You have successfully signed up.")

if __name__ == "__main__":
    signup()
