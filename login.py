import streamlit as st

# Mock database
users = {
    "user1": "password1",
    "user2": "password2"
}

def login():
    st.title("Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username] == password:
            st.success(f"Welcome, {username}!")
            user_dashboard(username)
        else:
            st.error("Invalid username or password.")

def change_password(username):
    st.title("Change Password")

    old_password = st.text_input("Old Password", type="password")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm New Password", type="password")

    if st.button("Change Password"):
        if old_password == users[username] and new_password == confirm_password:
            users[username] = new_password
            st.success("Password changed successfully.")
        else:
            st.error("Failed to change password. Please try again.")

def user_dashboard(username):
    st.title(f"{username}'s Dashboard")

    st.header("System Performance")
    # You can add system performance metrics here
    st.write("CPU Usage: 30%")
    st.write("Memory Usage: 40%")
    st.write("Disk Usage: 50%")

    st.header("Account Management")
    # You can add account management options here
    if st.button("Change Password"):
        change_password(username)

if __name__ == "__main__":
    login()
